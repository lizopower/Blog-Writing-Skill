#!/usr/bin/env python3
"""
Mechanical cross-article voice checks for a cluster of drafts.

The per-article linter (check_draft.py) and the taste review both look at one
article at a time, so three articles can each pass individually and still read
like the same voice when published together: identical opening formulas, the
same AI cliches, repeated multi-word phrases, and matching sentence cadence.

This script compares 2+ cluster drafts against EACH OTHER and reports shared
voice tells (Casting-style passes / warns / issues). Exit 1 when any issue
exists.

Usage:
    python cluster_voice_check.py content/articles/a content/articles/b content/articles/c
    python cluster_voice_check.py --root <project-root> --slugs a,b,c
    python cluster_voice_check.py a/draft.md b/draft.md --write-report
    python cluster_voice_check.py --root . --slugs a,b,c --allow "digital twin,ACME" --write-report

See standards/cluster_voice_guide.md for thresholds and workflow.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _article_type_profiles import (  # noqa: E402
    AI_CLICHES_EN,
    AI_CLICHES_ZH,
    CONTRAST_REFRAME_PATTERNS,
)
from check_draft import (  # noqa: E402
    _lint_lines,
    _opening_paragraph,
    _strip_code_fences,
    _strip_front_matter,
)

# --- Thresholds (documented in standards/cluster_voice_guide.md) ------------
NGRAM_SIZE = 5                     # shingle length for phrase-overlap check
LONG_NGRAM_SIZE = 8               # a shared gram this long = near-identical sentence
OPENING_JACCARD_SIMILAR = 0.6    # first-sentence token overlap that counts as "same opener"
OPENING_LEAD_TOKENS = 4          # identical leading tokens that count as "same opener"
SHARED_NGRAM_ISSUE = 6           # this many distinct shared phrases across the cluster = systemic
CADENCE_SPREAD_WORDS = 1.5       # max-min of mean sentence length below this = same rhythm
SAMPLE_LIMIT = 8                 # cap how many examples we print per finding

STOPWORDS = frozenset(
    """
    a an and are as at be but by for from had has have he her his in into is it
    its of on or so that the their them then there these they this to was were
    what when which who will with you your our we us if not no can also more most
    """.split()
)

_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")
_SENT_SPLIT = re.compile(r"[.!?。！？]+")


@dataclass
class Article:
    label: str
    body: str
    prose: str
    primary_keyword: str = ""

    opening_first_sentence: str = field(default="")
    tokens: list[str] = field(default_factory=list)
    sentence_lengths: list[int] = field(default_factory=list)
    h2_titles: list[str] = field(default_factory=list)


class ClusterCheckResult:
    def __init__(self) -> None:
        self.passes: list[str] = []
        self.warns: list[str] = []
        self.issues: list[str] = []

    @property
    def ok(self) -> bool:
        return not self.issues

    def render_markdown(self, *, labels: list[str]) -> str:
        lines = [
            "# Cluster Voice Report",
            "",
            f"Articles compared: {len(labels)}",
            *[f"- `{label}`" for label in labels],
            "",
            f"Status: **{'PASS' if self.ok else 'FAIL'}**",
            "",
        ]
        for title, items in (
            ("Passes", self.passes),
            ("Warnings", self.warns),
            ("Issues", self.issues),
        ):
            if items:
                lines.extend([f"## {title}", ""])
                lines.extend(f"- {item}" for item in items)
                lines.append("")
        lines.append(
            f"Summary: passes={len(self.passes)} warns={len(self.warns)} issues={len(self.issues)}"
        )
        return "\n".join(lines) + "\n"


# --- Parsing ----------------------------------------------------------------

def _sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]


def _word_tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def _first_sentence(paragraph: str) -> str:
    sents = _sentences(paragraph)
    return sents[0] if sents else ""


def build_article(label: str, content: str, primary_keyword: str = "") -> Article:
    body = _strip_front_matter(content)
    prose = _strip_code_fences(body)
    lint_text = "\n".join(_lint_lines(body))
    art = Article(label=label, body=body, prose=prose, primary_keyword=primary_keyword)
    art.opening_first_sentence = _first_sentence(_opening_paragraph(body))
    art.tokens = _word_tokens(lint_text)
    art.sentence_lengths = [len(_word_tokens(s)) for s in _sentences(prose)]
    art.h2_titles = [m.strip() for m in re.findall(r"^##\s+([^\n#][^\n]*)$", body, re.MULTILINE)]
    return art


# --- Individual cross-article checks ----------------------------------------

def _ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _is_exempt_gram(gram: tuple[str, ...], exempt_tokens: frozenset[str]) -> bool:
    # Skip grams that are pure filler or made only of exempt terms (keywords, brands).
    if all(tok in STOPWORDS for tok in gram):
        return True
    if all(tok in exempt_tokens or tok in STOPWORDS for tok in gram):
        return True
    return False


def check_shared_phrases(
    result: ClusterCheckResult, articles: list[Article], exempt_tokens: frozenset[str]
) -> None:
    n_articles = len(articles)
    gram_sets = [_ngrams(a.tokens, NGRAM_SIZE) for a in articles]
    long_sets = [_ngrams(a.tokens, LONG_NGRAM_SIZE) for a in articles]

    shared: list[tuple[tuple[str, ...], int]] = []
    seen: set[tuple[str, ...]] = set()
    for i, gset in enumerate(gram_sets):
        for gram in gset:
            if gram in seen or _is_exempt_gram(gram, exempt_tokens):
                continue
            count = sum(1 for other in gram_sets if gram in other)
            if count >= 2:
                shared.append((gram, count))
                seen.add(gram)

    if not shared:
        result.passes.append(
            f"[OK] no distinctive {NGRAM_SIZE}-word phrase repeated across articles"
        )
    else:
        shared.sort(key=lambda x: (-x[1], " ".join(x[0])))
        severity = result.issues if len(shared) >= SHARED_NGRAM_ISSUE else result.warns
        tag = "P1-cross-phrase" if severity is result.issues else "cross-phrase"
        severity.append(
            f"[{tag}] {len(shared)} distinctive {NGRAM_SIZE}-word phrase(s) shared by >=2 articles"
        )
        for gram, count in shared[:SAMPLE_LIMIT]:
            result.warns.append(f"[cross-phrase] {count}x: \"{' '.join(gram)}\"")

    # Any long shared gram = near-identical sentence, always an issue.
    long_seen: set[tuple[str, ...]] = set()
    for lset in long_sets:
        for gram in lset:
            if gram in long_seen or _is_exempt_gram(gram, exempt_tokens):
                continue
            if sum(1 for other in long_sets if gram in other) >= 2:
                long_seen.add(gram)
    for gram in list(long_seen)[:SAMPLE_LIMIT]:
        result.issues.append(
            f"[P1-duplicate-line] near-identical {LONG_NGRAM_SIZE}+-word run: \"{' '.join(gram)}\""
        )


def check_shared_cliches(result: ClusterCheckResult, articles: list[Article]) -> None:
    n_articles = len(articles)
    lowers = [a.prose.lower() for a in articles]

    def report(term: str, label: str, hits: int) -> None:
        if hits >= n_articles and n_articles >= 2:
            result.issues.append(f"[P1-shared-cliche] every article uses {label}: {term!r}")
        elif hits >= 2:
            result.warns.append(f"[shared-cliche] {hits} articles use {label}: {term!r}")

    for phrase in AI_CLICHES_EN:
        hits = sum(1 for text in lowers if phrase.lower() in text)
        report(phrase, "English cliche", hits)
    for phrase in AI_CLICHES_ZH:
        hits = sum(1 for a in articles if phrase in a.prose)
        report(phrase, "Chinese cliche", hits)

    for pattern, label in CONTRAST_REFRAME_PATTERNS:
        hits = sum(1 for a in articles if pattern.search(a.prose))
        report(label, "contrast-reframe", hits)

    if not result.warns and not result.issues:
        result.passes.append("[OK] no AI cliche or reframe pattern shared across articles")


def _lead_tokens(sentence: str, k: int) -> tuple[str, ...]:
    return tuple(_word_tokens(sentence)[:k])


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def check_opening_formulas(result: ClusterCheckResult, articles: list[Article]) -> None:
    flagged = False
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            s1, s2 = articles[i].opening_first_sentence, articles[j].opening_first_sentence
            if not s1 or not s2:
                continue
            lead1, lead2 = _lead_tokens(s1, OPENING_LEAD_TOKENS), _lead_tokens(s2, OPENING_LEAD_TOKENS)
            set1, set2 = set(_word_tokens(s1)), set(_word_tokens(s2))
            jac = _jaccard(set1, set2)
            same_lead = len(lead1) == OPENING_LEAD_TOKENS and lead1 == lead2
            if same_lead or jac >= OPENING_JACCARD_SIMILAR:
                flagged = True
                why = "identical opening words" if same_lead else f"{jac:.0%} first-sentence overlap"
                result.issues.append(
                    f"[P1-opener] {articles[i].label} & {articles[j].label} open the same way ({why})"
                )

    # Shared opening MOVE (all questions, all same first word) = softer signal.
    firsts = [a.opening_first_sentence for a in articles if a.opening_first_sentence]
    if len(firsts) >= 2:
        if all(s.rstrip().endswith("?") for s in firsts):
            result.warns.append("[opener-move] every article opens with a question")
        first_words = {_word_tokens(s)[0] for s in firsts if _word_tokens(s)}
        if len(first_words) == 1 and len(firsts) >= 2:
            result.warns.append(
                f"[opener-move] every article's first sentence starts with {next(iter(first_words))!r}"
            )

    if not flagged:
        result.passes.append("[OK] opening sentences are distinct across articles")


def check_cadence(result: ClusterCheckResult, articles: list[Article]) -> None:
    means = []
    for a in articles:
        if a.sentence_lengths:
            means.append(sum(a.sentence_lengths) / len(a.sentence_lengths))
    if len(means) < 2:
        return
    spread = max(means) - min(means)
    if spread < CADENCE_SPREAD_WORDS:
        result.warns.append(
            f"[cadence] articles share near-identical sentence rhythm "
            f"(mean sentence length spread {spread:.1f} words < {CADENCE_SPREAD_WORDS})"
        )
    else:
        result.passes.append(
            f"[OK] sentence-length rhythm varies across articles (spread {spread:.1f} words)"
        )


def check_skeletons(result: ClusterCheckResult, articles: list[Article]) -> None:
    withh2 = [a for a in articles if a.h2_titles]
    if len(withh2) < 2:
        return
    parallel = 0
    total_pairs = 0
    for i in range(len(withh2)):
        for j in range(i + 1, len(withh2)):
            total_pairs += 1
            a, b = withh2[i], withh2[j]
            if len(a.h2_titles) != len(b.h2_titles):
                continue
            sims = [
                _jaccard(set(_word_tokens(t1)), set(_word_tokens(t2)))
                for t1, t2 in zip(a.h2_titles, b.h2_titles)
            ]
            if sims and sum(sims) / len(sims) > 0.5:
                parallel += 1
                result.warns.append(
                    f"[skeleton] {a.label} & {b.label} use parallel section structures "
                    f"({len(a.h2_titles)} H2s, matching order)"
                )
    if total_pairs and parallel == 0:
        result.passes.append("[OK] section skeletons differ across articles")


# --- Orchestration ----------------------------------------------------------

def run_cluster_check(articles: list[Article], extra_allow: frozenset[str]) -> ClusterCheckResult:
    result = ClusterCheckResult()
    exempt_tokens = set(extra_allow)
    for a in articles:
        exempt_tokens.update(_word_tokens(a.primary_keyword))
    exempt = frozenset(exempt_tokens)

    check_opening_formulas(result, articles)
    check_shared_cliches(result, articles)
    check_shared_phrases(result, articles, exempt)
    check_cadence(result, articles)
    check_skeletons(result, articles)
    return result


def print_report(result: ClusterCheckResult, *, labels: list[str]) -> None:
    print(f"Comparing {len(labels)} articles:")
    for label in labels:
        print(f"  - {label}")
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
    print(
        f"Status: {status} | passes={len(result.passes)} "
        f"warns={len(result.warns)} issues={len(result.issues)}"
    )


def _resolve_targets(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    if args.slugs:
        root = Path(args.root or ".")
        for slug in [s.strip() for s in args.slugs.split(",") if s.strip()]:
            paths.append(root / "content" / "articles" / slug)
    paths.extend(Path(t) for t in args.targets)
    return paths


def _load_article(path: Path) -> Article | None:
    if path.is_dir():
        draft = path / "draft.md"
        meta = path / "article.json"
        primary = ""
        if meta.exists():
            try:
                primary = str(json.loads(meta.read_text(encoding="utf-8")).get("primaryKeyword", ""))
            except (json.JSONDecodeError, OSError):
                pass
        label = path.name
    else:
        draft, primary, label = path, "", path.parent.name if path.name == "draft.md" else path.stem
    if not draft.exists():
        print(f"Error: draft not found: {draft}", file=sys.stderr)
        return None
    return build_article(label, draft.read_text(encoding="utf-8"), primary)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Mechanical cross-article voice checks for a cluster.")
    parser.add_argument("targets", nargs="*", help="Workspace dirs or draft.md paths (2+)")
    parser.add_argument("--root", help="Project root, used with --slugs")
    parser.add_argument("--slugs", help="Comma-separated slugs under <root>/content/articles/")
    parser.add_argument("--allow", default="", help="Comma-separated phrases exempt from phrase overlap")
    parser.add_argument(
        "--write-report",
        nargs="?",
        const="",
        default=None,
        help="Write cluster_voice_report.md (optional explicit path)",
    )
    args = parser.parse_args()

    target_paths = _resolve_targets(args)
    if len(target_paths) < 2:
        parser.error("provide at least 2 articles (via positional paths or --slugs)")

    articles: list[Article] = []
    for path in target_paths:
        art = _load_article(path)
        if art is None:
            return 1
        articles.append(art)

    allow_tokens = frozenset(
        tok for phrase in args.allow.split(",") if phrase.strip() for tok in _word_tokens(phrase)
    )
    result = run_cluster_check(articles, allow_tokens)
    labels = [a.label for a in articles]
    print_report(result, labels=labels)

    if args.write_report is not None:
        if args.write_report:
            report_path = Path(args.write_report)
        else:
            common = Path(target_paths[0]).resolve().parent
            report_path = common / "cluster_voice_report.md"
        report_path.write_text(result.render_markdown(labels=labels), encoding="utf-8")
        print(f"Report written: {report_path}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
