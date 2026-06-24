#!/usr/bin/env python3
"""Normalize draft.md formatting (tables, links, glossary hints)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _normalize_links(text: str) -> tuple[str, list[str]]:
    messages: list[str] = []
    bare_urls = re.findall(r"(?<!\]\()(?<!\<)https?://[^\s)>]+", text)
    if bare_urls:
        messages.append(f"found {len(bare_urls)} bare URL(s); wrap in markdown links")
    return text, messages


def _check_glossary_terms(text: str, glossary: list) -> list[str]:
    messages: list[str] = []
    for entry in glossary:
        if not isinstance(entry, dict):
            continue
        term = entry.get("term") or entry.get("name")
        if not term or not isinstance(term, str):
            continue
        if term.lower() in text.lower():
            messages.append(f"glossary term present: {term}")
    return messages


def _align_table_row(row: str) -> str:
    if not row.strip().startswith("|"):
        return row
    cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
    return "| " + " | ".join(cells) + " |"


def _normalize_tables(text: str) -> tuple[str, list[str]]:
    lines = text.splitlines()
    changed = False
    output: list[str] = []
    for line in lines:
        if line.strip().startswith("|"):
            normalized = _align_table_row(line)
            changed = changed or normalized != line
            output.append(normalized)
        else:
            output.append(line)
    messages = ["normalized markdown table spacing"] if changed else []
    return "\n".join(output), messages


def normalize_draft(
    text: str,
    *,
    glossary: list | None = None,
    apply: bool = False,
) -> tuple[str, list[str], list[str]]:
    passes: list[str] = []
    warns: list[str] = []

    text, link_msgs = _normalize_links(text)
    warns.extend(link_msgs)

    text, table_msgs = _normalize_tables(text)
    if table_msgs:
        passes.extend(table_msgs)

    if glossary:
        passes.extend(_check_glossary_terms(text, glossary))

    if not apply:
        warns.append("check-only mode; pass --apply to write normalized draft")
    return text, passes, warns


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Normalize draft.md formatting.")
    parser.add_argument("target", help="draft.md path or article workspace")
    parser.add_argument("--workspace", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Write normalized content back to draft.md")
    parser.add_argument("--check-only", action="store_true", help="Alias for default non-apply mode")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if args.workspace or (target.is_dir() and (target / "draft.md").exists()):
        workspace = target
        draft_path = workspace / "draft.md"
        context_path = workspace / "context_pack.json"
    else:
        workspace = None
        draft_path = target
        context_path = None

    if not draft_path.exists():
        print(f"Error: {draft_path} not found", file=sys.stderr)
        return 1

    glossary: list = []
    if context_path and context_path.exists():
        try:
            pack = json.loads(context_path.read_text(encoding="utf-8"))
            glossary = pack.get("glossary") or []
        except json.JSONDecodeError:
            pass

    original = draft_path.read_text(encoding="utf-8")
    normalized, passes, warns = normalize_draft(original, glossary=glossary, apply=args.apply)

    print(f"Target: {draft_path}")
    for item in passes:
        print(f"  + {item}")
    for item in warns:
        print(f"  ! {item}")

    if args.apply and normalized != original:
        draft_path.write_text(normalized, encoding="utf-8")
        print("Applied normalization.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
