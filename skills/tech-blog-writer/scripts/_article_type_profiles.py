"""Machine-readable article type profiles for check_draft.py.

Human-readable spec: standards/article_type_profiles.md
Lint guide: standards/draft_lint_guide.md
"""

from __future__ import annotations

import re
from typing import Any

VALID_ARTICLE_TYPES = frozenset(
    {"blog", "how-to", "case-study", "comparison", "white-paper"}
)

ARTICLE_TYPE_PROFILES: dict[str, dict[str, Any]] = {
    "blog": {
        "label": "Technical blog",
        "min_h2": 3,
        "max_h2": 20,
        "min_data_points": 2,
        "section_keywords": [],
        "cta_patterns": [r"next steps", r"contact", r"learn more", r"get started"],
    },
    "how-to": {
        "label": "How-to guide",
        "min_h2": 4,
        "max_h2": 18,
        "min_data_points": 1,
        "section_keywords": ["step", "how", "guide", "procedure", "checklist"],
        "cta_patterns": [r"try", r"start", r"download", r"template"],
    },
    "case-study": {
        "label": "Case study",
        "min_h2": 4,
        "max_h2": 15,
        "min_data_points": 3,
        "section_keywords": ["challenge", "problem", "solution", "result", "outcome", "lesson"],
        "cta_patterns": [r"contact", r"discuss", r"similar"],
    },
    "comparison": {
        "label": "Comparison article",
        "min_h2": 4,
        "max_h2": 16,
        "min_data_points": 3,
        "section_keywords": ["comparison", "versus", "criteria", "recommendation", "trade"],
        "cta_patterns": [r"choose", r"evaluate", r"decision"],
    },
    "white-paper": {
        "label": "White paper",
        "min_h2": 5,
        "max_h2": 25,
        "min_data_points": 5,
        "section_keywords": ["executive", "summary", "methodology", "finding", "conclusion"],
        "cta_patterns": [r"download", r"contact", r"request"],
    },
}

MARKETING_WORDS = [
    "revolutionary",
    "amazing",
    "incredible",
    "best in class",
    "game-changing",
    "game changer",
    "breakthrough",
    "unparalleled",
    "unmatched",
    "leading provider",
    "industry leader",
    "cutting-edge",
    "state-of-the-art",
    "transformative",
    "supercharge",
    "unlock",
    "elevate",
]

HEDGE_WORDS = [
    "very",
    "really",
    "just",
    "actually",
    "basically",
    "essentially",
    "quite",
    "rather",
    "somewhat",
    "arguably",
    "potentially",
    "presumably",
    "seemingly",
]

AI_CLICHES_EN = [
    "in today's fast-paced",
    "ever-evolving",
    "rapidly changing world",
    "in a world of",
    "in today's fast-paced digital world",
    "it's worth noting",
    "it's important to note",
    "needless to say",
    "when it comes to",
    "in the realm of",
    "in the world of",
    "at the end of the day",
    "in essence",
    "simply put",
    "in summary",
    "to sum up",
    "in conclusion",
    "let's dive in",
    "let's explore",
    "buckle up",
    "delve into",
    "leverage",
    "utilize",
    "seamless",
    "seamlessly",
    "robust",
    "harness",
    "navigate",
    "landscape",
    "ecosystem",
    "tapestry",
    "testament to",
    "foster",
    "bolster",
    "underscore",
    "meticulous",
    "nuanced",
    "intricate",
    "furthermore",
    "moreover",
    "consequently",
    "it is evident that",
    "here's the thing",
    "but here's the thing",
    "let me be direct",
]

AI_CLICHES_ZH = [
    "在当今快节奏",
    "随着时代的发展",
    "众所周知",
    "不言而喻",
    "值得一提的是",
    "综上所述",
    "总而言之",
    "深入探讨",
    "赋能",
    "助力",
    "全方位",
    "一站式",
]

# Keep technical terms when used as terms of art (writing_style_guide Rule 9).
AI_TERM_ALLOWLIST_PATTERNS = [
    re.compile(r"\brobust\s+regression\b", re.IGNORECASE),
    re.compile(r"\brobust\s+statistics\b", re.IGNORECASE),
    re.compile(r"\bcable\s+harness\b", re.IGNORECASE),
    re.compile(r"\bwiring\s+harness\b", re.IGNORECASE),
    re.compile(r"\bharness\s+connector\b", re.IGNORECASE),
]

CONTRAST_REFRAME_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"it['']s not (?:about|just)\s+[^,.]{3,80},?\s+it['']s\b", re.IGNORECASE),
        "it's not X, it's Y",
    ),
    (
        re.compile(r"this isn['']t [^,.]{3,80},?\s+it['']s\b", re.IGNORECASE),
        "this isn't X, it's Y",
    ),
    (
        re.compile(
            r"the (?:problem|goal|answer) isn['']t [^,.]{3,80}\.\s+the (?:problem|goal|answer) is\b",
            re.IGNORECASE,
        ),
        "the problem isn't X. The problem is Y",
    ),
    (
        re.compile(r"stop [^.!?]{3,60}\.\s+start\b", re.IGNORECASE),
        "Stop X. Start Y",
    ),
    (
        re.compile(r"most people think [^.!?]{3,120}\.\s+the truth is\b", re.IGNORECASE),
        "Most people think X. The truth is Y",
    ),
    (
        re.compile(r"not only [^,]{3,80},\s+but also\b", re.IGNORECASE),
        "Not only X but also Y",
    ),
]

PLACEHOLDER_PATTERNS = [
    r"\[TODO\]",
    r"\[todo\]",
    r"\[citation needed\]",
    r"\[Citation needed\]",
    r"\[N\]",
    r"\[Entity TBD\]",
    r"\[TBD\]",
    r"\[待补充\]",
    r"\[待核实\]",
]

NUMBER_PATTERNS = [
    re.compile(r"\d+%"),
    re.compile(r"\d+\s*°[CF]"),
    re.compile(r"\d+\.\d+\s*[A-Za-z]+"),
    re.compile(r"\$\d+"),
    re.compile(r"\d+\s*cycles", re.IGNORECASE),
    re.compile(r"\d+-\d+%"),
]

SOURCE_PATTERNS = [
    re.compile(r"\(PDF p\.\d+", re.IGNORECASE),
    re.compile(r"\(Sheet:", re.IGNORECASE),
    re.compile(r"\(Word:", re.IGNORECASE),
    re.compile(r"\(Source:", re.IGNORECASE),
    re.compile(r"Source:", re.IGNORECASE),
    re.compile(r"https?://"),
    re.compile(r"\[[^\]]+\]\([^)]+\)"),
]

EM_DASH_WARN_PER_1000_WORDS = 15
EM_DASH_ISSUE_PER_1000_WORDS = 30
OPENING_MAX_SENTENCES = 3
