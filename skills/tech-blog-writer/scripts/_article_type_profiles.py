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
    # NOTE: profile cta_patterns are matched against the whole body (legacy) AND,
    # together with CTA_GENERIC_PATTERNS, against the closing section only.

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
    "unprecedented",
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
    "pivotal",
    "crucial",
    "multifaceted",
    "paradigm shift",
    "symphony",
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

# Translationese: phrasing typical of Chinese-to-English transfer (writing_style_guide
# "Native American English" section). Substring match, warn only.
TRANSLATIONESE_PHRASES = [
    "with the development of",
    "with the rapid development",
    "in recent years",
    "more and more",
    "play an important role",
    "plays an important role",
    "played an important role",
    "pay attention to",
    "it is worth mentioning",
    "as we all know",
    "as is known to all",
    "attach great importance to",
    "has become a hot topic",
    "in our daily life",
    "last but not least",
    "generally speaking",
    "to some extent",
    "the above-mentioned",
    "under the background of",
    "it can be seen that",
    "there is no denying",
    "every coin has two sides",
    "a double-edged sword",
    "give full play to",
    "vigorously promote",
]

# Mass/count-noun errors typical of Chinese-transfer English (writing_style_guide
# Rule 22 self-check zones). Warn only; "researches"/"trainings" omitted (valid verbs/plurals).
MASS_NOUN_PLURALS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bequipments\b", re.IGNORECASE), "equipments -> equipment"),
    (re.compile(r"\bfeedbacks\b", re.IGNORECASE), "feedbacks -> feedback"),
    (re.compile(r"\binformations\b", re.IGNORECASE), "informations -> information"),
    (re.compile(r"\badvices\b", re.IGNORECASE), "advices -> advice"),
    (re.compile(r"\bsoftwares\b", re.IGNORECASE), "softwares -> software"),
    (re.compile(r"\bhardwares\b", re.IGNORECASE), "hardwares -> hardware"),
    (re.compile(r"\bevidences\b", re.IGNORECASE), "evidences -> evidence"),
    (re.compile(r"\bknowledges\b", re.IGNORECASE), "knowledges -> knowledge"),
    (re.compile(r"\bfurnitures\b", re.IGNORECASE), "furnitures -> furniture"),
    (re.compile(r"\bmachineries\b", re.IGNORECASE), "machineries -> machinery"),
]

# Hedged definition openers (writing_style_guide Rule 15: definitions go straight
# to the bridge verb — "X is Y"). Warn only.
DEFINITION_HEDGE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bcan be considered\b", re.IGNORECASE), "can be considered"),
    (re.compile(r"\b(?:may|can) be regarded as\b", re.IGNORECASE), "may/can be regarded as"),
    (re.compile(r"\bcould be described as\b", re.IGNORECASE), "could be described as"),
    (re.compile(r"\bcan be thought of as\b", re.IGNORECASE), "can be thought of as"),
    (re.compile(r"\bis a kind of\b", re.IGNORECASE), "is a kind of"),
]

# Pronoun openers that violate entity echo (writing_style_guide Rule 16): the first
# sentence answering a question H2 must repeat the question's subject entity.
PRONOUN_OPENER = re.compile(r"^(?:It|This|That|These|They|该|它|这)\b")

# Generic closing-CTA signals, matched only against the final H2 section
# (in addition to the per-profile cta_patterns).
CTA_GENERIC_PATTERNS = [
    r"next steps?",
    r"contact",
    r"learn more",
    r"get started",
    r"\btry\b",
    r"start with",
    r"start by",
    r"download",
    r"subscribe",
    r"reach out",
    r"talk to",
    r"book a",
    r"schedule",
    r"sign up",
    r"run the numbers",
    r"request",
    r"^spec\b",
]

# American English enforcement: flag British spellings (warn only).
BRITISH_SPELLING_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\borganis(?:e|es|ed|ing|ation|ations)\b", re.IGNORECASE), "organise -> organize"),
    (re.compile(r"\bcolour\w*\b", re.IGNORECASE), "colour -> color"),
    (re.compile(r"\bbehaviour\w*\b", re.IGNORECASE), "behaviour -> behavior"),
    (re.compile(r"\bfavour\w*\b", re.IGNORECASE), "favour -> favor"),
    (re.compile(r"\bflavour\w*\b", re.IGNORECASE), "flavour -> flavor"),
    (re.compile(r"\banalys(?:e|es|ed|ing)\b", re.IGNORECASE), "analyse -> analyze"),
    (re.compile(r"\boptimis(?:e|es|ed|ing|ation|ations)\b", re.IGNORECASE), "optimise -> optimize"),
    (re.compile(r"\bminimis(?:e|es|ed|ing)\b", re.IGNORECASE), "minimise -> minimize"),
    (re.compile(r"\bmaximis(?:e|es|ed|ing)\b", re.IGNORECASE), "maximise -> maximize"),
    (re.compile(r"\butilis(?:e|es|ed|ing|ation)\b", re.IGNORECASE), "utilise -> utilize (or better: use)"),
    (re.compile(r"\bcentre\w*\b", re.IGNORECASE), "centre -> center"),
    (re.compile(r"\bfibre\w*\b", re.IGNORECASE), "fibre -> fiber"),
    (re.compile(r"\blitres?\b", re.IGNORECASE), "litre -> liter"),
    (re.compile(r"\bmetres?\b", re.IGNORECASE), "metre -> meter"),
    (re.compile(r"\bwhilst\b", re.IGNORECASE), "whilst -> while"),
    (re.compile(r"\bamongst\b", re.IGNORECASE), "amongst -> among"),
    (re.compile(r"\blearnt\b", re.IGNORECASE), "learnt -> learned"),
    (re.compile(r"\blicence\b", re.IGNORECASE), "licence -> license"),
    (re.compile(r"\bdefence\b", re.IGNORECASE), "defence -> defense"),
    (re.compile(r"\bpractise\w*\b", re.IGNORECASE), "practise -> practice"),
    (re.compile(r"\bprogrammes?\b", re.IGNORECASE), "programme -> program"),
    (re.compile(r"\bcatalogue\w*\b", re.IGNORECASE), "catalogue -> catalog"),
    (re.compile(r"\baluminium\b", re.IGNORECASE), "aluminium -> aluminum"),
    (re.compile(r"\bartefacts?\b", re.IGNORECASE), "artefact -> artifact"),
    (re.compile(r"\btravell(?:ing|ed|er|ers)\b", re.IGNORECASE), "travelling -> traveling"),
    (re.compile(r"\bmodell(?:ing|ed)\b", re.IGNORECASE), "modelling -> modeling"),
    (re.compile(r"\blabell(?:ing|ed)\b", re.IGNORECASE), "labelled -> labeled"),
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

# Rule 11 / writing-plain-language.md: no em dashes in English prose.
# Any em dash warns; density above ISSUE still escalates to P0.
EM_DASH_WARN_PER_1000_WORDS = 0
EM_DASH_ISSUE_PER_1000_WORDS = 15

# Label lines repealed by content/specs/writing-plain-language.md
LABEL_LINE_PATTERN = re.compile(
    r"(?im)^\s*\*{0,2}("
    r"Key Insight|Non-negotiable|Common Mistake|Trade-off|Selection Criteria|"
    r"Key takeaway|Bottom line|Pro tip|Takeaway"
    r")\*{0,2}\s*:\s*"
)

READY_TO_CTA_PATTERN = re.compile(
    r"(?im)^\s*#{1,3}\s*Ready to\b|^\s*\*{0,2}Ready to\b.{0,80}\?",
)
OPENING_MAX_SENTENCES = 3

# Rhythm thresholds (writing_style_guide Rules 1-3; draft_lint_guide appendix A.2).
RHYTHM_MIN_SENTENCES = 10
RHYTHM_MEAN_WARN = 25.0
RHYTHM_MEAN_HARD = 35.0
RHYTHM_STDEV_WARN = 6.0
RHYTHM_MONOTONE_RUN = 4
RHYTHM_MONOTONE_BAND = 3
RHYTHM_PUNCH_MAX_WORDS = 6
RHYTHM_PUNCH_MIN_BODY_WORDS = 300
RHYTHM_MAX_ZH_RATIO = 0.2

