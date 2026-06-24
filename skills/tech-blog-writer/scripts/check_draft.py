#!/usr/bin/env python3
"""
Mechanical draft quality checks for content/articles/<slug>/draft.md.

Outputs passes / warns / issues (Casting-style). Exit 1 when any issue exists.

Usage:
    python check_draft.py path/to/draft.md
    python check_draft.py path/to/content/articles/<slug> --workspace
    python check_draft.py path/to/draft.md --article-type case-study
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _article_type_profiles import (
    AI_CLICHES_EN,
    AI_CLICHES_ZH,
    ARTICLE_TYPE_PROFILES,
    MARKETING_WORDS,
    PLACEHOLDER_PATTERNS,
    UNIT_INCONSISTENCIES,
    VALID_ARTICLE_TYPES,
)


class DraftCheckResult:
    def __init__(self) -> None:
        self.passes: list[str] = []
        self.warns: list[str] = []
        self.issues: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.issues


def _strip_front_matter(content: str) -> str:
    if content.startswith("---"):
        match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
        if match:
            return content[match.end() :]
    return content


def _h2_sections(body: str) -> list[tuple[str, str]]:
    parts = re.split(r"^(## [^\n]+)\n", body, flags=re.MULTILINE)
    sections: list[tuple[str, str]] = []
    if len(parts) < 2:
        return sections
    for index in range(1, len(parts), 2):
        title = parts[index].strip()
        text = parts[index + 1] if index + 1 < len(parts) else ""
        sections.append((title, text))
    return sections


def _count_data_points(content: str) -> int:
    patterns = [
        r"\d+%",
        r"\d+\s*°[CF]",
        r"\d+\.\d+",
        r"\|\s*[^|]+\s*\|",
        r"\(PDF",
        r"\(Sheet:",
        r"\(Source:",
    ]
    hits = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            hits.add(match.start())
    return len(hits)


def _resolve_paths(
    target: Path, workspace_mode: bool
) -> tuple[Path, Path | None, str | None]:
    if workspace_mode or (target.is_dir() and (target / "draft.md").exists()):
        workspace = target.resolve()
        draft_path = workspace / "draft.md"
        article_path = workspace / "article.json"
        return draft_path, article_path, None
    return target.resolve(), None, None


def _load_article_type(article_path: Path | None, override: str | None) -> str:
    if override:
        return override
    if article_path and article_path.exists():
        try:
            data = json.loads(article_path.read_text(encoding="utf-8"))
            article_type = data.get("articleType") or "blog"
            return str(article_type)
        except (json.JSONDecodeError, OSError):
            pass
    return "blog"


def check_draft(
    content: str,
    *,
    article_type: str = "blog",
    strict_final: bool = False,
) -> DraftCheckResult:
    result = DraftCheckResult()
    body = _strip_front_matter(content)

    if not body.strip():
        result.issues.append("[P0-empty] draft body is empty")
        return result

    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", body))
    word_count = len(re.findall(r"\b\w+\b", body)) + zh_chars
    result.passes.append(f"[OK] approximate length: {word_count} words/chars")

    if article_type not in VALID_ARTICLE_TYPES:
        result.issues.append(f"[P0-type] unknown articleType {article_type!r}")
        article_type = "blog"
    profile = ARTICLE_TYPE_PROFILES[article_type]

    h2_count = len(re.findall(r"^## [^#]", body, re.MULTILINE))
    if h2_count < profile["min_h2"]:
        result.issues.append(
            f"[P0-structure] H2 count {h2_count} below minimum {profile['min_h2']} for {article_type}"
        )
    elif h2_count > profile["max_h2"]:
        result.warns.append(
            f"[structure] H2 count {h2_count} above recommended max {profile['max_h2']} for {article_type}"
        )
    else:
        result.passes.append(f"[OK] H2 count {h2_count} within {article_type} range")

    sections = _h2_sections(body)
    for title, text in sections:
        section_words = len(re.findall(r"\b\w+\b", text)) + len(re.findall(r"[\u4e00-\u9fff]", text))
        if section_words < 40 and text.strip():
            result.warns.append(f"[section-balance] short section {title!r} (~{section_words} words)")
        if section_words > 1200:
            result.warns.append(f"[section-balance] long section {title!r} (~{section_words} words)")

    keywords = profile.get("section_keywords") or []
    if keywords:
        lower = body.lower()
        if not any(keyword in lower for keyword in keywords):
            result.warns.append(
                f"[profile] no section keyword matched for {article_type}: {', '.join(keywords[:5])}"
            )
        else:
            result.passes.append(f"[OK] {article_type} section keywords present")

    data_points = _count_data_points(body)
    if data_points < profile["min_data_points"]:
        result.issues.append(
            f"[P0-data] found ~{data_points} data signals; {article_type} expects >= {profile['min_data_points']}"
        )
    else:
        result.passes.append(f"[OK] data-point signals: {data_points}")

    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            result.issues.append(f"[P0-placeholder] unresolved placeholder {pattern} ({len(matches)}x)")

    for word in MARKETING_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", body, re.IGNORECASE):
            result.warns.append(f"[marketing] detected: {word!r}")

    for phrase in AI_CLICHES_EN:
        if phrase.lower() in body.lower():
            result.warns.append(f"[AI-cliche] English: {phrase!r}")

    for phrase in AI_CLICHES_ZH:
        if phrase in body:
            result.warns.append(f"[AI-cliche] Chinese: {phrase!r}")

    celsius_variants = set()
    if "°C" in body:
        celsius_variants.add("°C")
    if "℃" in body:
        celsius_variants.add("℃")
    if len(celsius_variants) > 1:
        result.issues.append("[P0-units] mixed Celsius symbols (°C and ℃)")

    if re.search(r"\bKW\b", body):
        result.warns.append("[units] use kW not KW")
    if re.search(r"\bkw\b", body) and not re.search(r"\bkW\b", body):
        result.warns.append("[units] use kW not kw")

    cta_patterns = profile.get("cta_patterns") or []
    if cta_patterns and not any(re.search(p, body, re.IGNORECASE) for p in cta_patterns):
        result.warns.append(f"[profile] no CTA pattern matched for {article_type}")

    if strict_final:
        if "TL;DR" not in body and "tl;dr" not in body.lower():
            result.issues.append("[P0-final] missing TL;DR section")
        if not re.search(r"##\s+FAQ", body, re.IGNORECASE):
            result.issues.append("[P0-final] missing FAQ section")

    if not result.issues and not result.warns:
        result.passes.append("[OK] no mechanical issues or warnings")

    return result


def print_report(result: DraftCheckResult, *, label: str) -> None:
    print(f"Checking: {label}")
    print("=" * 50)
    if result.passes:
        print("\n[PASSES]")
        for item in result.passes:
            print(f"  + {item}")
    if result.warns:
        print(f"\n[WARNS] ({len(result.warns)})")
        for item in result.warns:
            print(f"  ! {item}")
    if result.issues:
        print(f"\n[ISSUES] ({len(result.issues)})")
        for item in result.issues:
            print(f"  x {item}")
    print("\n" + "=" * 50)
    status = "PASS" if result.ok else "FAIL"
    print(f"Status: {status} | passes={len(result.passes)} warns={len(result.warns)} issues={len(result.issues)}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Mechanical draft quality checks.")
    parser.add_argument("target", help="Path to draft.md or article workspace directory")
    parser.add_argument(
        "--workspace",
        action="store_true",
        help="Treat target as content/articles/<slug> workspace",
    )
    parser.add_argument("--article-type", choices=sorted(VALID_ARTICLE_TYPES))
    parser.add_argument(
        "--strict-final",
        action="store_true",
        help="Apply final_article-style requirements (TL;DR, FAQ)",
    )
    args = parser.parse_args()

    target = Path(args.target)
    draft_path, article_path, _ = _resolve_paths(target, args.workspace)
    if not draft_path.exists():
        print(f"Error: draft not found: {draft_path}", file=sys.stderr)
        return 1

    article_type = _load_article_type(article_path, args.article_type)
    content = draft_path.read_text(encoding="utf-8")
    result = check_draft(content, article_type=article_type, strict_final=args.strict_final)
    print_report(result, label=str(draft_path))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
