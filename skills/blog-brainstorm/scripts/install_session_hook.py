#!/usr/bin/env python3
"""Install or uninstall optional session-start context hooks."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

from _hookinstaller import build_session_start_entries, merge_block, remove_block, render_diff


HARNESS_CONFIG = {
    "claude": (".claude", "settings.json", 30),
    "codex": (".codex", "hooks.json", 10),
}


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
    directory, filename, _timeout = HARNESS_CONFIG[harness]
    return root / directory / filename


def command_for(root: Path) -> str:
    script = Path(__file__).resolve().with_name("resume_context.py")
    return f"python {shlex.quote(str(script))} --root {shlex.quote(str(root))}"


def prompt_confirm() -> bool:
    reply = input("Apply this change? [y/N] ").strip().lower()
    return reply in {"y", "yes"}


def cmd_install(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    path = config_path(root, args.harness)
    try:
        old = load_json(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    _directory, _filename, timeout = HARNESS_CONFIG[args.harness]
    block = build_session_start_entries(command_for(root), timeout=timeout)
    new = merge_block(old, block)
    why = (
        "Install Blog-Writing-Skill session context injection so new sessions receive the current "
        "article target, lifecycle gates, and project writing specs."
    )
    print(render_diff(old, new, why), end="")
    if not args.yes and not prompt_confirm():
        print("Cancelled.")
        return 1

    save_json(path, new)
    print(f"Installed {args.harness} session hook at {path}")
    print(
        "Uninstall with: "
        f"python {shlex.quote(str(Path(__file__).resolve()))} "
        f"--harness {args.harness} --uninstall --root {shlex.quote(str(root))}"
    )
    print("First run may ask you to trust this hook. Review and approve it in your host; do not bypass hook trust.")
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    path = config_path(root, args.harness)
    try:
        old = load_json(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    new = remove_block(old)
    why = "Remove only Blog-Writing-Skill managed session context hooks and preserve all host hooks."
    print(render_diff(old, new, why), end="")
    if not args.yes and not prompt_confirm():
        print("Cancelled.")
        return 1
    save_json(path, new)
    print(f"Uninstalled {args.harness} session hook from {path}")
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
