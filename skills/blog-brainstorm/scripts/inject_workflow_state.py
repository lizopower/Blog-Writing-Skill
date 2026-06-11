#!/usr/bin/env python3
"""Per-turn UserPromptSubmit breadcrumb for Blog-Writing-Skill.

Mirrors Trellis's inject-workflow-state hook: on every user turn, emit a short
``<workflow-state>`` block so the active article/phase stays in the attention
window as the conversation grows and the one-time SessionStart context decays.

Stays silent (exit 0, no output) when:
- the turn looks like a spawned sub-agent (avoid yanking it back to the main
  workflow);
- no project root with an article workspace can be found;
- there is no actionable in-progress article.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def installed_project_root() -> Path | None:
    """Project root inferred from this script's installed location.

    When running as the managed runtime copy at
    ``<root>/.trellis-writing/runtime/scripts/inject_workflow_state.py`` this is
    the most reliable signal — independent of the process CWD, and in a monorepo
    it cannot select an unrelated nested workspace. Returns ``None`` when running
    from the source tree (e.g. tests), where CWD-based discovery applies instead.
    """
    if (
        SCRIPT_DIR.name == "scripts"
        and SCRIPT_DIR.parent.name == "runtime"
        and SCRIPT_DIR.parent.parent.name == ".trellis-writing"
    ):
        return SCRIPT_DIR.parent.parent.parent
    return None


def find_project_root(start: Path) -> Path | None:
    """Walk up from ``start`` to the first dir owning an article workspace.

    CWD-robust: handles sub-directory launches and monorepo packages instead of
    assuming the hook runs from the project root.
    """
    current = start.resolve()
    while True:
        if (current / "content" / "articles").is_dir() or (current / ".trellis-writing").is_dir():
            return current
        if current == current.parent:
            return None
        current = current.parent


def resolve_root(payload: dict) -> Path | None:
    """Most reliable project root first: installed-script location, then the
    host-provided payload ``cwd``, then the process CWD."""
    installed = installed_project_root()
    if installed is not None:
        return installed
    starts: list[Path] = []
    payload_cwd = payload.get("cwd")
    if isinstance(payload_cwd, str) and payload_cwd:
        starts.append(Path(payload_cwd))
    starts.append(Path.cwd())
    for start in starts:
        root = find_project_root(start)
        if root is not None:
            return root
    return None


def read_payload() -> dict:
    """Best-effort parse of the host's JSON hook payload from stdin."""
    try:
        raw = sys.stdin.read()
    except (OSError, ValueError):
        return {}
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def is_subagent(payload: dict) -> bool:
    """Defensive sub-agent detection.

    UserPromptSubmit normally fires only for the main interactive session, but if
    a host ever routes a spawned agent's turn here, re-anchoring it to the main
    article workflow would derail its delegated task. Strict boolean check only:
    these keys are not in Claude Code's documented UserPromptSubmit payload today,
    so a loose truthy test could false-positive on a string field that happens to
    be non-empty.
    """
    return payload.get("isSubagent") is True or payload.get("is_subagent") is True


def main() -> int:
    payload = read_payload()
    if is_subagent(payload):
        return 0

    root = resolve_root(payload)
    if root is None:
        return 0

    from resume_context import render_breadcrumb

    breadcrumb = render_breadcrumb(root)
    if not breadcrumb:
        return 0

    envelope = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": breadcrumb,
        }
    }
    print(json.dumps(envelope, ensure_ascii=False), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
