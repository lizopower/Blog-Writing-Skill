#!/usr/bin/env python3
"""Assert routers and slash commands stay synchronized with sub-skills.

The bundle ships two routers on purpose:
  - SKILL.md
  - skills/blog-writing-skills/SKILL.md

They are intentionally NOT byte-identical. The invariants that must hold are:
  - both routers mention every routable sub-skill
  - both routers keep the core workflow guardrails
  - router descriptions are host-neutral
  - commands/ contains one slash command for every routable sub-skill
  - each command invokes its matching namespaced skill

Exit 0 if synchronized, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
COMMANDS_DIR = ROOT / "commands"

ROUTERS = [
    ROOT / "SKILL.md",
    SKILLS_DIR / "blog-writing-skills" / "SKILL.md",
]

# The router itself is not a routable target.
SELF = "blog-writing-skills"

REQUIRED_ROUTER_GUARDRAILS = {
    "complete workflow default": r"complete\s+`?blog-writing-workflow`?\s+pipeline",
    "execution contract": r"execution contract",
    "rich input is not a waiver": r"rich input is not a waiver",
    "pre-draft gate": r"pre-draft gate|before any article body text",
    "workflow receipts": r"workflow receipts? (are mandatory|after every stage)|emit a receipt",
    "explicit skip waiver": r"skip a step.{0,100}(explicitly asks|explicit user request|explicit request)",
    "no direct topic-to-writer shortcut": r"(do not|never).{0,80}(shortcut|jump).{0,80}`tech-blog-writer`",
}

HOST_SPECIFIC_DESCRIPTION_PATTERNS = [
    r"\bcodex user\b",
    r"\bclaude user\b",
]


def routable_skills() -> set[str]:
    return {
        p.name
        for p in SKILLS_DIR.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists() and p.name != SELF
    }


def mentioned(text: str, skills: set[str]) -> set[str]:
    found = set()
    for name in skills:
        # Match the skill name as a backticked token or bare word boundary.
        if re.search(rf"`{re.escape(name)}`|\b{re.escape(name)}\b", text):
            found.add(name)
    return found


def frontmatter_description(text: str) -> str:
    match = re.match(r"---\s*\n(?P<body>.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return ""

    for line in match.group("body").splitlines():
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            return value.strip("\"'")
    return ""


def check_routers(expected: set[str]) -> bool:
    ok = True
    for router in ROUTERS:
        if not router.exists():
            print(f"FAIL: router missing: {router.relative_to(ROOT)}")
            ok = False
            continue

        router_ok = True
        text = router.read_text(encoding="utf-8")
        rel = router.relative_to(ROOT)

        missing = sorted(expected - mentioned(text, expected))
        if missing:
            print(f"FAIL: {rel} does not mention: {', '.join(missing)}")
            router_ok = False
        else:
            print(f"OK: {rel} covers all {len(expected)} sub-skills")

        desc = frontmatter_description(text).lower()
        host_specific = [
            pattern
            for pattern in HOST_SPECIFIC_DESCRIPTION_PATTERNS
            if re.search(pattern, desc)
        ]
        if host_specific:
            print(f"FAIL: {rel} description is host-specific: {', '.join(host_specific)}")
            router_ok = False
        else:
            print(f"OK: {rel} description is host-neutral")

        for label, pattern in REQUIRED_ROUTER_GUARDRAILS.items():
            if not re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                print(f"FAIL: {rel} missing guardrail: {label}")
                router_ok = False
        if router_ok:
            print(f"OK: {rel} includes required workflow guardrails")
        ok = router_ok and ok

    return ok


def check_commands(expected: set[str]) -> bool:
    if not COMMANDS_DIR.exists():
        print("FAIL: commands/ directory missing")
        return False

    ok = True
    command_files = {p.stem: p for p in COMMANDS_DIR.glob("*.md")}

    missing = sorted(expected - set(command_files))
    extra = sorted(set(command_files) - expected)

    if missing:
        print(f"FAIL: commands/ missing: {', '.join(missing)}")
        ok = False
    else:
        print(f"OK: commands/ covers all {len(expected)} sub-skills")

    if extra:
        print(f"FAIL: commands/ has no matching sub-skill: {', '.join(extra)}")
        ok = False

    for name in sorted(expected & set(command_files)):
        text = command_files[name].read_text(encoding="utf-8")
        expected_invocation = f"blog-writing-skills:{name}"
        if expected_invocation not in text:
            print(
                f"FAIL: commands/{name}.md does not invoke {expected_invocation}"
            )
            ok = False

    if ok:
        print("OK: every command invokes its matching namespaced skill")

    return ok


def main() -> int:
    expected = routable_skills()
    if not expected:
        print("ERROR: no routable sub-skills found under skills/")
        return 1

    ok = check_routers(expected)
    ok = check_commands(expected) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
