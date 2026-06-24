#!/usr/bin/env python3
"""Detect near-duplicate passages between draft.md and source/reference texts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MIN_SUBSTRING_LEN = 16


def _normalize(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    return re.sub(r"[^\u4e00-\u9fff\w]", "", text, flags=re.UNICODE)


def _substrings(text: str, min_len: int = MIN_SUBSTRING_LEN) -> set[str]:
    normalized = _normalize(text)
    if len(normalized) < min_len:
        return set()
    return {normalized[index : index + min_len] for index in range(len(normalized) - min_len + 1)}


def _line_hits(draft: str, fragment: str) -> list[int]:
    lines = draft.splitlines()
    hits: list[int] = []
    for index, line in enumerate(lines, start=1):
        if fragment in _normalize(line):
            hits.append(index)
    return hits


def load_source_texts(workspace: Path, root: Path, include_reference: bool) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []
    sources_path = workspace / "sources.jsonl"
    if sources_path.exists():
        for line in sources_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            for key in ("local_path", "extract_path", "cache_path"):
                rel = record.get(key)
                if not rel:
                    continue
                path = Path(rel)
                if not path.is_absolute():
                    path = root / path
                if path.exists() and path.is_file():
                    sources.append((path.name, path.read_text(encoding="utf-8", errors="replace")))
                    break
            notes = record.get("notes")
            if isinstance(notes, str) and len(notes) >= MIN_SUBSTRING_LEN:
                sources.append((f"notes:{record.get('id', 'source')}", notes))

    if include_reference:
        reference_root = root / "content" / "reference"
        if reference_root.exists():
            for path in reference_root.rglob("*.md"):
                if path.name.lower() == "readme.md":
                    continue
                sources.append((f"reference:{path.relative_to(reference_root)}", path.read_text(encoding="utf-8", errors="replace")))
    return sources


def audit(draft: str, sources: list[tuple[str, str]]) -> list[dict]:
    findings: list[dict] = []
    draft_subs = _substrings(draft)
    if not draft_subs:
        return findings

    for label, source_text in sources:
        source_subs = _substrings(source_text)
        overlap = draft_subs & source_subs
        if not overlap:
            continue
        sample = sorted(overlap, key=len, reverse=True)[0]
        line_numbers = _line_hits(draft, sample)
        findings.append(
            {
                "source": label,
                "match_length": len(sample),
                "sample": sample[:40],
                "draft_lines": line_numbers[:5],
                "match_count": len(overlap),
            }
        )
    return findings


def render_report(findings: list[dict]) -> str:
    lines = ["# Near-Duplicate Audit", ""]
    if not findings:
        lines.append("No 16+ character contiguous matches against sources or reference corpus.")
        lines.append("")
        lines.append("Status: PASS")
        return "\n".join(lines) + "\n"

    lines.append(f"Found {len(findings)} source(s) with overlapping substrings.")
    lines.append("")
    for item in findings:
        lines.append(f"## {item['source']}")
        lines.append(f"- Match count: {item['match_count']}")
        lines.append(f"- Sample fragment: `{item['sample']}`")
        if item["draft_lines"]:
            lines.append(f"- Draft lines: {', '.join(str(n) for n in item['draft_lines'])}")
        lines.append("")
    lines.append("Status: WARN")
    lines.append("")
    lines.append("Rewrite or attribute matching passages before publish.")
    return "\n".join(lines) + "\n"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Audit draft for near-duplicate source text.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--slug", required=True, help="Article slug")
    parser.add_argument("--include-reference", action="store_true", help="Also scan content/reference/")
    parser.add_argument("--output", help="Report path (default: workspace near_duplicate_report.md)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    workspace = root / "content" / "articles" / args.slug
    draft_path = workspace / "draft.md"
    if not draft_path.exists():
        print(f"Error: missing {draft_path}", file=sys.stderr)
        return 1

    draft = draft_path.read_text(encoding="utf-8")
    sources = load_source_texts(workspace, root, args.include_reference)
    findings = audit(draft, sources)
    report = render_report(findings)

    out_path = Path(args.output) if args.output else workspace / "near_duplicate_report.md"
    out_path.write_text(report, encoding="utf-8")
    print(report)
    return 0 if not findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
