#!/usr/bin/env python3
"""Pure helpers for installing managed session hooks."""

from __future__ import annotations

import copy
import difflib
import json
from typing import Any


MANAGED_BY = "blog-writing-skill"
# Mirror Trellis's SessionStart matcher set exactly. `resume` is intentionally
# omitted: a resumed session already carries the original startup injection in
# its restored transcript, and the per-turn UserPromptSubmit breadcrumb re-anchors
# workflow state on the next prompt, so re-injecting the heavyweight SessionStart
# block on resume would only duplicate context.
SESSION_MATCHERS = ("startup", "clear", "compact")
PRE_TOOL_USE_MATCHER = "Write|Edit"
MANAGED_EVENTS = ("SessionStart", "PreToolUse", "UserPromptSubmit")


def build_session_start_entries(command: str, *, timeout: int) -> list[dict[str, Any]]:
    return [
        {
            "_managed_by": MANAGED_BY,
            "matcher": matcher,
            "hooks": [
                {
                    "type": "command",
                    "command": command,
                    "timeout": timeout,
                }
            ],
        }
        for matcher in SESSION_MATCHERS
    ]


def build_pre_tool_use_entries(command: str, *, timeout: int) -> list[dict[str, Any]]:
    return [
        {
            "_managed_by": MANAGED_BY,
            "matcher": PRE_TOOL_USE_MATCHER,
            "hooks": [
                {
                    "type": "command",
                    "command": command,
                    "timeout": timeout,
                }
            ],
        }
    ]


def build_user_prompt_submit_entries(command: str, *, timeout: int) -> list[dict[str, Any]]:
    # UserPromptSubmit fires on every user turn and is matcher-less in Claude
    # Code (Trellis registers it without a `matcher` key). This per-turn
    # breadcrumb is what keeps the agent anchored to the workflow as the
    # conversation grows and the one-time SessionStart context decays.
    return [
        {
            "_managed_by": MANAGED_BY,
            "hooks": [
                {
                    "type": "command",
                    "command": command,
                    "timeout": timeout,
                }
            ],
        }
    ]


def merge_block(config: dict[str, Any], block: list[dict[str, Any]], event: str = "SessionStart") -> dict[str, Any]:
    merged = remove_block(config, (event,))
    hooks = merged.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        merged["hooks"] = hooks
    entries = hooks.setdefault(event, [])
    if not isinstance(entries, list):
        entries = []
        hooks[event] = entries
    entries.extend(copy.deepcopy(block))
    return merged


def remove_block(config: dict[str, Any], events: tuple[str, ...] = MANAGED_EVENTS) -> dict[str, Any]:
    cleaned = copy.deepcopy(config)
    hooks = cleaned.get("hooks")
    if not isinstance(hooks, dict):
        return cleaned
    for event in events:
        entries = hooks.get(event)
        if isinstance(entries, list):
            hooks[event] = [entry for entry in entries if not _is_managed(entry)]
    return cleaned


def render_diff(old: dict[str, Any], new: dict[str, Any], why: str) -> str:
    old_lines = _render_json(old).splitlines()
    new_lines = _render_json(new).splitlines()
    diff = "\n".join(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="before",
            tofile="after",
            lineterm="",
        )
    )
    return f"Why: {why}\n\n{diff}\n"


def _is_managed(entry: Any) -> bool:
    return isinstance(entry, dict) and entry.get("_managed_by") == MANAGED_BY


def _render_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
