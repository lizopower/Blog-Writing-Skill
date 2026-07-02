#!/usr/bin/env python3
"""Quantitative scorer for native-voice evals.

Reuses check_draft's lint plus rhythm stats and emits JSON per draft.

Usage:
    python evals/score_draft.py path/to/draft.md --article-type comparison
    python evals/score_draft.py evals/runs/2026-07-02-baseline --all
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "tech-blog-writer" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_draft import check_draft, _lint_lines, _split_sentences  # noqa: E402

WARN_CATEGORIES = [
    "translationese",
    "spelling",
    "AI-cliche",
    "AI-pattern",
    "hedge",
    "marketing",
    "rhythm",
    "punctuation",
    "sources",
    "structure",
    "section-balance",
    "profile",
    "units",
]

# Weights: how badly each category hurts "reads like a native" (0-10).
WEIGHTS = {
    "translationese": 8,
    "AI-cliche": 6,
    "AI-pattern": 6,
    "spelling": 5,
    "rhythm": 5,
    "hedge": 3,
    "marketing": 3,
    "punctuation": 3,
    "sources": 2,
    "structure": 2,
    "section-balance": 1,
    "profile": 1,
    "units": 1,
}

ARTICLE_TYPE_GUESS = re.compile(r"task-0?(\d+)")
TASK_TYPES = {"1": "comparison", "2": "how-to", "3": "case-study"}


def _rhythm_stats(body: str) -> dict:
    counts = _split_sentences(_lint_lines(body))
    if not counts:
        return {"sentences": 0}
    mean = sum(counts) / len(counts)
    variance = sum((c - mean) ** 2 for c in counts) / len(counts)
    return {
        "sentences": len(counts),
        "mean_len": round(mean, 1),
        "stdev_len": round(variance ** 0.5, 1),
        "punch_count": sum(1 for c in counts if c < 6),
        "max_len": max(counts),
    }


def score_file(path: Path, article_type: str) -> dict:
    body = path.read_text(encoding="utf-8")
    result = check_draft(body, article_type=article_type)

    by_category = {cat: 0 for cat in WARN_CATEGORIES}
    for warn in result.warns:
        match = re.match(r"\[([\w-]+)\]", warn)
        if match and match.group(1) in by_category:
            by_category[match.group(1)] += 1

    penalty = sum(WEIGHTS.get(cat, 1) * n for cat, n in by_category.items())
    penalty += 15 * len(result.issues)
    native_score = max(0, 100 - penalty)

    return {
        "file": str(path),
        "article_type": article_type,
        "native_score": native_score,
        "issues": len(result.issues),
        "warns_total": len(result.warns),
        "warns_by_category": {k: v for k, v in by_category.items() if v},
        "rhythm": _rhythm_stats(body),
        "issue_lines": result.issues,
        "warn_lines": result.warns,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score eval drafts.")
    parser.add_argument("target", help="Draft file or run directory")
    parser.add_argument("--article-type", default="blog")
    parser.add_argument("--all", action="store_true", help="Score every *.md in a run dir")
    args = parser.parse_args()

    target = Path(args.target)
    if args.all or target.is_dir():
        reports = []
        for md in sorted(target.glob("*.md")):
            guess = ARTICLE_TYPE_GUESS.search(md.name)
            atype = TASK_TYPES.get(guess.group(1), args.article_type) if guess else args.article_type
            report = score_file(md, atype)
            reports.append(report)
            out = md.with_suffix(".score.json")
            out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"{md.name}: native_score={report['native_score']} warns={report['warns_total']} issues={report['issues']}")
        if reports:
            summary = {
                "run": str(target),
                "drafts": len(reports),
                "mean_native_score": round(sum(r["native_score"] for r in reports) / len(reports), 1),
                "total_issues": sum(r["issues"] for r in reports),
                "total_warns": sum(r["warns_total"] for r in reports),
            }
            (target / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
            print(f"summary: mean_native_score={summary['mean_native_score']}")
        return 0

    report = score_file(target, args.article_type)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
