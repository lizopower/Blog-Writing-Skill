#!/usr/bin/env python3
"""Extract genre conventions from content/reference benchmark articles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


VALID_TYPES = {"blog", "how-to", "case-study", "comparison", "white-paper"}
CONVENTION_THRESHOLD = 3


def _h2_titles(text: str) -> list[str]:
    return [line[3:].strip().lower() for line in text.splitlines() if line.startswith("## ") and not line.startswith("### ")]


def _table_count(text: str) -> int:
    return len(re.findall(r"^\|.+\|$", text, re.MULTILINE))


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text)) + len(re.findall(r"[\u4e00-\u9fff]", text))


def _has_cta(text: str) -> bool:
    return bool(re.search(r"(contact|next steps|learn more|download|get started)", text, re.IGNORECASE))


def _has_tldr(text: str) -> bool:
    return "tl;dr" in text.lower()


def analyze_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(path),
        "h2_titles": _h2_titles(text),
        "table_count": _table_count(text),
        "word_count": _word_count(text),
        "has_cta": _has_cta(text),
        "has_tldr": _has_tldr(text),
    }


def extract_conventions(analyses: list[dict], article_type: str, topic: str) -> dict:
    sample_count = len(analyses)
    h2_counter: Counter[str] = Counter()
    for item in analyses:
        h2_counter.update(item["h2_titles"])

    conventions: list[dict] = []
    optional_styles: list[str] = []

    for title, freq in h2_counter.most_common():
        if not title:
            continue
        classification = "convention" if freq >= CONVENTION_THRESHOLD else "optional_style"
        entry = {
            "trait": f"h2_section:{title}",
            "frequency": freq,
            "classification": classification,
            "detail": f"Section heading '{title}' appears in {freq}/{sample_count} benchmarks",
        }
        if classification == "convention":
            conventions.append(entry)
        else:
            optional_styles.append(title)

    avg_tables = sum(item["table_count"] for item in analyses) / sample_count
    if avg_tables >= 1 and sum(1 for item in analyses if item["table_count"] >= 1) >= CONVENTION_THRESHOLD:
        conventions.append(
            {
                "trait": "includes_tables",
                "frequency": sum(1 for item in analyses if item["table_count"] >= 1),
                "classification": "convention",
                "detail": f"Benchmarks average {avg_tables:.1f} markdown tables",
            }
        )

    tldr_freq = sum(1 for item in analyses if item["has_tldr"])
    if tldr_freq >= CONVENTION_THRESHOLD:
        conventions.append(
            {
                "trait": "includes_tldr",
                "frequency": tldr_freq,
                "classification": "convention",
                "detail": "TL;DR block present in majority of benchmarks",
            }
        )

    cta_freq = sum(1 for item in analyses if item["has_cta"])
    if cta_freq >= CONVENTION_THRESHOLD:
        conventions.append(
            {
                "trait": "includes_cta",
                "frequency": cta_freq,
                "classification": "convention",
                "detail": "Call-to-action language in majority of benchmarks",
            }
        )

    avg_h2 = sum(len(item["h2_titles"]) for item in analyses) / sample_count
    common_h2 = [title for title, freq in h2_counter.most_common(8) if freq >= CONVENTION_THRESHOLD]

    return {
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "article_type": article_type,
        "topic": topic,
        "sample_count": sample_count,
        "conventions": conventions,
        "optional_styles": sorted(set(optional_styles)),
        "structure": {
            "avg_h2_count": round(avg_h2, 1),
            "avg_table_count": round(avg_tables, 1),
            "common_h2_patterns": common_h2,
        },
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Extract genre conventions from reference corpus.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--topic", required=True, help="Topic slug under content/reference/")
    parser.add_argument("--type", required=True, choices=sorted(VALID_TYPES), help="Article type folder")
    parser.add_argument("--slug", help="Article slug; writes genre_conventions.json into workspace")
    parser.add_argument("--output", help="Explicit output JSON path")
    parser.add_argument("--max-samples", type=int, default=5)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    corpus_dir = root / "content" / "reference" / args.topic / args.type
    if not corpus_dir.is_dir():
        print(f"Error: reference corpus not found: {corpus_dir}", file=sys.stderr)
        return 1

    files = sorted(path for path in corpus_dir.glob("*.md") if path.name.lower() != "readme.md")
    if not files:
        print(f"Error: no .md benchmarks in {corpus_dir}", file=sys.stderr)
        return 1

    selected = files[: args.max_samples]
    analyses = [analyze_file(path) for path in selected]
    payload = extract_conventions(analyses, args.type, args.topic)

    if args.output:
        out_path = Path(args.output).resolve()
    elif args.slug:
        out_path = root / "content" / "articles" / args.slug / "genre_conventions.json"
    else:
        out_path = root / ".trellis-writing" / "conventions" / f"{args.topic}-{args.type}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({payload['sample_count']} samples, {len(payload['conventions'])} conventions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
