#!/usr/bin/env python3
"""Pure helpers for installing managed session hooks."""

from __future__ import annotations

import copy
import difflib
import json
from typing import Any


MANAGED_BY = "blog-writing-skill"
SESSION_MATCHERS = ("startup", "clear", "compact")


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


def merge_block(config: dict[str, Any], block: list[dict[str, Any]]) -> dict[str, Any]:
    merged = remove_block(config)
    hooks = merged.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        hooks = {}
        merged["hooks"] = hooks
    session_start = hooks.setdefault("SessionStart", [])
    if not isinstance(session_start, list):
        session_start = []
        hooks["SessionStart"] = session_start
    session_start.extend(copy.deepcopy(block))
    return merged


def remove_block(config: dict[str, Any]) -> dict[str, Any]:
    cleaned = copy.deepcopy(config)
    hooks = cleaned.get("hooks")
    if not isinstance(hooks, dict):
        return cleaned
    session_start = hooks.get("SessionStart")
    if not isinstance(session_start, list):
        return cleaned
    hooks["SessionStart"] = [entry for entry in session_start if not _is_managed(entry)]
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
