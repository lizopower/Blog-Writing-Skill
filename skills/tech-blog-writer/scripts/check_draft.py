#!/usr/bin/env python3
"""
Mechanical draft quality checks for content/articles/<slug>/draft.md.

Outputs passes / warns / issues (Casting-style). Exit 1 when any issue exists.

Usage:
    python check_draft.py path/to/draft.md
    python check_draft.py path/to/content/articles/<slug> --workspace
    python check_draft.py path/to/draft.md --article-type case-study
    python check_draft.py path/to/content/articles/<slug> --workspace --write-report

See standards/draft_lint_guide.md for the full checklist and workflow.
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
    AI_TERM_ALLOWLIST_PATTERNS,
    ARTICLE_TYPE_PROFILES,
    CONTRAST_REFRAME_PATTERNS,
    EM_DASH_ISSUE_PER_1000_WORDS,
    EM_DASH_WARN_PER_1000_WORDS,
    HEDGE_WORDS,
    MARKETING_WORDS,
    NUMBER_PATTERNS,
    OPENING_MAX_SENTENCES,
    PLACEHOLDER_PATTERNS,
    SOURCE_PATTERNS,
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

    def render_markdown(self, *, label: str) -> str:
        lines = [
            "# Draft Lint Report",
            "",
            f"Target: `{label}`",
            f"Status: **{'PASS' if self.ok else 'FAIL'}**",
            "",
        ]
        if self.passes:
            lines.extend(["## Passes", ""])
            lines.extend(f"- {item}" for item in self.passes)
            lines.append("")
        if self.warns:
            lines.extend(["## Warnings", ""])
            lines.extend(f"- {item}" for item in self.warns)
            lines.append("")
        if self.issues:
            lines.extend(["## Issues", ""])
            lines.extend(f"- {item}" for item in self.issues)
            lines.append("")
        lines.append(
            f"Summary: passes={len(self.passes)} warns={len(self.warns)} issues={len(self.issues)}"
        )
        return "\n".join(lines) + "\n"


def _strip_front_matter(content: str) -> str:
    if content.startswith("---"):
        match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
        if match:
            return content[match.end() :]
    return content


def _strip_code_fences(body: str) -> str:
    return re.sub(r"```.*?```", "", body, flags=re.DOTALL)


def _lint_lines(body: str) -> list[str]:
    """Lines used for line-based checks; skips code fences and table rows."""
    lines: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.startswith("|") or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def _word_count(body: str) -> int:
    zh_chars = len(re.findall(r"[\u4e00-\u9fff]", body))
    return len(re.findall(r"\b\w+\b", body)) + zh_chars


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
    hits: set[int] = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            hits.add(match.start())
    return len(hits)


def _line_has_source(line: str, next_line: str = "") -> bool:
    combined = f"{line}\n{next_line}"
    if "**Assumption" in line or "To Verify" in line or "[Entity TBD]" in line:
        return True
    return any(pattern.search(combined) for pattern in SOURCE_PATTERNS)


def _find_unsourced_numbers(body: str, *, limit: int = 5) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    lines = body.splitlines()
    in_fence = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("---") or stripped.startswith("|") or stripped.startswith("#"):
            continue
        if not any(pattern.search(line) for pattern in NUMBER_PATTERNS):
            continue
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if _line_has_source(line, next_line):
            continue
        findings.append((index + 1, line.strip()[:100]))
        if len(findings) >= limit:
            break
    return findings


def _ai_term_allowed(line: str, term: str) -> bool:
    if term.lower() not in {"robust", "harness"}:
        return False
    return any(pattern.search(line) for pattern in AI_TERM_ALLOWLIST_PATTERNS)


def _count_em_dashes(body: str) -> int:
    return len(re.findall(r"—|\u2014", body))


def _opening_paragraph(body: str) -> str:
    chunks = re.split(r"\n\s*\n", body.strip())
    for chunk in chunks:
        text = chunk.strip()
        if not text or text.startswith("#"):
            continue
        return text
    return ""


def _sentence_count(paragraph: str) -> int:
    parts = re.split(r"[.!?。！？]+", paragraph)
    return len([part for part in parts if part.strip()])


def _resolve_paths(
    target: Path, workspace_mode: bool
) -> tuple[Path, Path | None, Path | None]:
    if workspace_mode or (target.is_dir() and (target / "draft.md").exists()):
        workspace = target.resolve()
        draft_path = workspace / "draft.md"
        article_path = workspace / "article.json"
        return draft_path, article_path, workspace
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
    prose = _strip_code_fences(body)

    if not body.strip():
        result.issues.append("[P0-empty] draft body is empty")
        return result

    words = _word_count(body)
    result.passes.append(f"[OK] approximate length: {words} words/chars")

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
        section_words = _word_count(text)
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

    lint_lines = _lint_lines(body)
    lint_text = "\n".join(lint_lines)

    for word in MARKETING_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lint_text, re.IGNORECASE):
            result.warns.append(f"[marketing] detected: {word!r}")

    for word in HEDGE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lint_text, re.IGNORECASE):
            result.warns.append(f"[hedge] detected: {word!r}")

    for phrase in AI_CLICHES_EN:
        if phrase.lower() not in lint_text.lower():
            continue
        if phrase in {"robust", "harness"}:
            if all(_ai_term_allowed(line, phrase) for line in lint_lines if phrase.lower() in line.lower()):
                continue
        result.warns.append(f"[AI-cliche] English: {phrase!r}")

    for phrase in AI_CLICHES_ZH:
        if phrase in lint_text:
            result.warns.append(f"[AI-cliche] Chinese: {phrase!r}")

    for pattern, label in CONTRAST_REFRAME_PATTERNS:
        if pattern.search(prose):
            result.warns.append(f"[AI-pattern] contrast reframe: {label}")

    em_dashes = _count_em_dashes(prose)
    if words > 0:
        per_1000 = em_dashes * 1000 / words
        if per_1000 > EM_DASH_ISSUE_PER_1000_WORDS:
            result.issues.append(
                f"[P0-punctuation] em-dash density {per_1000:.1f}/1000 words (>{EM_DASH_ISSUE_PER_1000_WORDS})"
            )
        elif per_1000 > EM_DASH_WARN_PER_1000_WORDS:
            result.warns.append(
                f"[punctuation] em-dash density {per_1000:.1f}/1000 words (>{EM_DASH_WARN_PER_1000_WORDS})"
            )
        elif em_dashes:
            result.passes.append(f"[OK] em-dash count {em_dashes} within density target")

    if re.search(r"—.*—", prose) or re.search(r"\u2014.*\u2014", prose):
        result.warns.append("[punctuation] multiple em-dashes in one sentence")

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

    unsourced = _find_unsourced_numbers(body)
    if unsourced:
        result.warns.append(f"[sources] {len(unsourced)}+ potentially unsourced quantitative line(s)")
        for line_no, snippet in unsourced:
            result.warns.append(f"[sources] line {line_no}: {snippet}")
    else:
        result.passes.append("[OK] no obvious unsourced quantitative lines")

    opening = _opening_paragraph(body)
    if opening:
        opening_sentences = _sentence_count(opening)
        if opening_sentences > OPENING_MAX_SENTENCES:
            result.warns.append(
                f"[structure] opening block has {opening_sentences} sentences; target <= {OPENING_MAX_SENTENCES}"
            )
        else:
            result.passes.append(f"[OK] opening block sentence count: {opening_sentences}")

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
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write draft_lint.md beside draft.md when target is a workspace",
    )
    args = parser.parse_args()

    target = Path(args.target)
    draft_path, article_path, workspace = _resolve_paths(target, args.workspace)
    if not draft_path.exists():
        print(f"Error: draft not found: {draft_path}", file=sys.stderr)
        return 1

    article_type = _load_article_type(article_path, args.article_type)
    content = draft_path.read_text(encoding="utf-8")
    result = check_draft(content, article_type=article_type, strict_final=args.strict_final)
    print_report(result, label=str(draft_path))

    if args.write_report and workspace is not None:
        report_path = workspace / "draft_lint.md"
        report_path.write_text(result.render_markdown(label=str(draft_path)), encoding="utf-8")
        print(f"Report written: {report_path}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
