"""Machine-readable article type profiles for check_draft.py.

Human-readable spec: standards/article_type_profiles.md
"""

from __future__ import annotations

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

AI_CLICHES_EN = [
    "in today's fast-paced",
    "ever-evolving",
    "rapidly changing world",
    "it's worth noting",
    "it's important to note",
    "needless to say",
    "when it comes to",
    "in the realm of",
    "in the world of",
    "at the end of the day",
    "in essence",
    "simply put",
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

UNIT_INCONSISTENCIES = [
    (r"\bKW\b", "kW", "Use kW not KW"),
    (r"\bkw\b", "kW", "Use kW not kw"),
    (r"°C", "℃", "Mixed Celsius symbols (°C vs ℃)"),
    (r"℃", "°C", "Mixed Celsius symbols (℃ vs °C)"),
]
