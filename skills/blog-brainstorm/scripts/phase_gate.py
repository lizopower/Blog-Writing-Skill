#!/usr/bin/env python3
"""PreToolUse gate: deny writes to lifecycle artifacts before their phase.

Installed into ``.trellis-writing/runtime/scripts/`` and wired as a Claude
Code PreToolUse hook for Write|Edit. Reads the hook payload from stdin and
prints a deny envelope when the target file is a gated workspace artifact
whose lifecycle phase has not been reached. Errors fail open: the gate must
never break the host session, only withhold a deny.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


GATED_TOOLS = {"Write", "Edit"}

ARTIFACT_MIN_PHASE = {
    "outline.md": "outlining",
    "draft.md": "drafting",
    "fact_check.md": "fact_checking",
    "editorial_review.md": "editorial_review",
}


def project_root() -> Path:
    # <root>/.trellis-writing/runtime/scripts/phase_gate.py
    return Path(__file__).resolve().parents[3]


def workspace_parts(root: Path, raw_path: str) -> tuple[str, str] | None:
    """Return (slug, artifact name) when raw_path targets a live workspace file."""
    try:
        relative = Path(raw_path).resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    parts = relative.parts
    if len(parts) != 4:
        return None
    if parts[0].lower() != "content" or parts[1].lower() != "articles":
        return None
    slug, name = parts[2], parts[3]
    if slug == "_archive":
        return None
    return slug, name.lower()


def deny_reason(root: Path, tool_name: str, tool_input: dict[str, Any]) -> str | None:
    if tool_name not in GATED_TOOLS:
        return None
    raw_path = tool_input.get("file_path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    located = workspace_parts(root, raw_path)
    if located is None:
        return None
    slug, name = located
    min_phase = ARTIFACT_MIN_PHASE.get(name)
    if min_phase is None:
        return None

    article_path = root / "content" / "articles" / slug / "article.json"
    if not article_path.exists():
        return None

    from _statemachine import PHASES, migrate

    try:
        article = json.loads(article_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"article '{slug}': article.json is unreadable ({exc}); repair lifecycle state before editing {name}"
    if not isinstance(article, dict):
        return f"article '{slug}': article.json root must be an object; repair lifecycle state before editing {name}"

    article = migrate(article)
    current = str(article.get("currentPhase", ""))
    if current not in PHASES:
        return f"article '{slug}': unknown phase {current!r} in article.json; repair lifecycle state before editing {name}"
    if PHASES.index(current) >= PHASES.index(min_phase):
        return None

    article_cli = root / ".trellis-writing" / "runtime" / "scripts" / "article.py"
    return (
        f"{name} is gated to lifecycle phase '{min_phase}' or later, but article '{slug}' is in phase "
        f"'{current}'. Complete the upstream stages, then advance with: python {article_cli} advance "
        f"--slug {slug} --to <next-phase> --root {root}. A failed artifact gate may be waived only with "
        "explicit user approval via --waive; do not work around this gate by writing elsewhere."
    )


def deny_envelope(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict):
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    try:
        reason = deny_reason(project_root(), str(payload.get("tool_name", "")), tool_input)
    except Exception:  # noqa: BLE001 - fail open: the gate must never break the session
        return 0
    if reason:
        print(json.dumps(deny_envelope(reason), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
