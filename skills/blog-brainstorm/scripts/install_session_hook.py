#!/usr/bin/env python3
"""Install or uninstall optional session-start context hooks."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from _agentsmd import (
    PRELUDE_FILENAME,
    MARKER_BEGIN,
    remove_prelude,
    render_prelude,
    upsert_prelude,
)
from _hookinstaller import (
    build_pre_tool_use_entries,
    build_session_start_entries,
    build_user_prompt_submit_entries,
    merge_block,
    remove_block,
    render_diff,
)
from _runtimeinstaller import RUNTIME_ROOT, ensure_runtime


# directory, filename, session timeout, PreToolUse phase gate, UserPromptSubmit breadcrumb.
# The last two are independent capabilities: Codex has neither verified on a real host,
# but a future harness could support one without the other.
HARNESS_CONFIG = {
    "claude": (".claude", "settings.json", 30, True, True),
    "codex": (".codex", "hooks.json", 10, False, False),
}

PHASE_GATE_TIMEOUT = 10
BREADCRUMB_TIMEOUT = 5


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def config_path(root: Path, harness: str) -> Path:
    directory, filename, _timeout, _gate, _breadcrumb = HARNESS_CONFIG[harness]
    return root / directory / filename


def command_for(root: Path, harness: str) -> str:
    script = f"{RUNTIME_ROOT}/runtime/scripts/session_start.py"
    return shell_command(["python", script, "--harness", harness])


def gate_command_for(root: Path) -> str:
    script = f"{RUNTIME_ROOT}/runtime/scripts/phase_gate.py"
    return shell_command(["python", script])


def breadcrumb_command_for(root: Path) -> str:
    script = f"{RUNTIME_ROOT}/runtime/scripts/inject_workflow_state.py"
    return shell_command(["python", script])


def write_prelude(root: Path) -> Path:
    """Insert/refresh the managed Codex lifecycle prelude in AGENTS.md."""
    path = root / PRELUDE_FILENAME
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(upsert_prelude(existing, render_prelude()), encoding="utf-8")
    return path


def clear_prelude(root: Path) -> Path | None:
    """Strip the managed prelude block, preserving any user content.

    Returns the path when a managed block was present, else ``None``. Removes
    the file only when stripping the block leaves it empty.
    """
    path = root / PRELUDE_FILENAME
    if not path.exists():
        return None
    existing = path.read_text(encoding="utf-8")
    if MARKER_BEGIN not in existing:
        return None
    remaining = remove_prelude(existing)
    if remaining.strip():
        path.write_text(remaining, encoding="utf-8")
    else:
        path.unlink()
    return path


def shell_command(args: list[object]) -> str:
    parts = [str(arg) for arg in args]
    if sys.platform == "win32":
        return subprocess.list2cmdline(parts)
    return shlex.join(parts)


def prompt_confirm() -> bool:
    reply = input("Apply this change? [y/N] ").strip().lower()
    return reply in {"y", "yes"}


def cmd_install(args: argparse.Namespace) -> int:
    return install_hook(Path(args.root).resolve(), args.harness, assume_yes=args.yes, print_diff=True)


def install_hook(root: Path, harness: str, *, assume_yes: bool, print_diff: bool = True) -> int:
    root = root.resolve()
    ensure_runtime(root)
    path = config_path(root, harness)
    try:
        old = load_json(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _directory, _filename, timeout, gate_supported, breadcrumb_supported = HARNESS_CONFIG[harness]
    block = build_session_start_entries(command_for(root, harness), timeout=timeout)
    new = merge_block(old, block, "SessionStart")
    if gate_supported:
        gate_block = build_pre_tool_use_entries(gate_command_for(root), timeout=PHASE_GATE_TIMEOUT)
        new = merge_block(new, gate_block, "PreToolUse")
    if breadcrumb_supported:
        # Re-anchoring every turn is what stops the workflow from being ignored as the
        # one-time SessionStart context decays. Claude-only for now: the UserPromptSubmit
        # envelope/event name is unverified on a real Codex host, so Codex keeps
        # SessionStart + AGENTS.md prelude only.
        breadcrumb_block = build_user_prompt_submit_entries(breadcrumb_command_for(root), timeout=BREADCRUMB_TIMEOUT)
        new = merge_block(new, breadcrumb_block, "UserPromptSubmit")
    why = (
        "Install Blog-Writing-Skill session context injection so new sessions receive the current "
        "article target, lifecycle gates, and project writing specs. On Claude, also install the "
        "PreToolUse phase gate that blocks writes to lifecycle artifacts before their phase, and the "
        "UserPromptSubmit breadcrumb that re-anchors the active article/phase on every turn."
    )
    if print_diff:
        print(render_diff(old, new, why), end="")
    if not assume_yes and not prompt_confirm():
        print("Cancelled.")
        return 1

    save_json(path, new)
    print(f"Installed {harness} session hook at {path}")
    if not gate_supported:
        prelude_path = write_prelude(root)
        print(
            f"Wrote lifecycle prelude to {prelude_path} - {harness} has no PreToolUse gate, "
            "so this managed AGENTS.md block enforces the workflow by convention."
        )
    print(
        "Uninstall with: "
        f"{shell_command(['python', Path(__file__).resolve(), '--harness', harness, '--uninstall', '--root', root])}"
    )
    print("First run may ask you to trust this hook. Review and approve it in your host; do not bypass hook trust.")
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    return uninstall_hook(Path(args.root).resolve(), args.harness, assume_yes=args.yes, print_diff=True)


def uninstall_hook(root: Path, harness: str, *, assume_yes: bool, print_diff: bool = True) -> int:
    root = root.resolve()
    path = config_path(root, harness)
    try:
        old = load_json(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    new = remove_block(old)
    why = "Remove only Blog-Writing-Skill managed session context hooks and preserve all host hooks."
    if print_diff:
        print(render_diff(old, new, why), end="")
    if not assume_yes and not prompt_confirm():
        print("Cancelled.")
        return 1
    save_json(path, new)
    print(f"Uninstalled {harness} session hook from {path}")
    _directory, _filename, _timeout, gate_supported, _breadcrumb = HARNESS_CONFIG[harness]
    if not gate_supported:
        cleared = clear_prelude(root)
        if cleared is not None:
            print(f"Removed managed lifecycle prelude block from {cleared} (user content preserved)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install optional Blog-Writing-Skill session hooks.")
    parser.add_argument("--harness", choices=sorted(HARNESS_CONFIG), required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--install", action="store_true")
    action.add_argument("--uninstall", action="store_true")
    parser.add_argument("--root", default=".", help="Project root whose host hook config should be changed.")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt. Intended for tests/automation.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.install:
        return cmd_install(args)
    return cmd_uninstall(args)


if __name__ == "__main__":
    raise SystemExit(main())
