#!/usr/bin/env python3
"""Assert both routers reference every routable sub-skill.

The bundle ships two routers on purpose:
  - SKILL.md                         (root, Claude Code entry — full prose)
  - skills/blog-writing-skills/SKILL.md  (Codex plugin router — condensed)

They are intentionally NOT identical text. The invariant that must hold is
coverage parity: whenever a sub-skill is added or renamed, BOTH routers must
still mention it by name. This catches the real drift risk (a router silently
omitting a skill) without forcing the two files to be byte-identical.

Exit 0 if both routers cover every sub-skill, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

ROUTERS = [
    ROOT / "SKILL.md",
    SKILLS_DIR / "blog-writing-skills" / "SKILL.md",
]

# The Codex router itself is not a routable target.
SELF = "blog-writing-skills"


def routable_skills() -> set[str]:
    return {
        p.name
        for p in SKILLS_DIR.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists() and p.name != SELF
    }


def mentioned(text: str, skills: set[str]) -> set[str]:
    found = set()
    for name in skills:
        # match the skill name as a backticked token or bare word boundary
        if re.search(rf"`{re.escape(name)}`|\b{re.escape(name)}\b", text):
            found.add(name)
    return found


def main() -> int:
    expected = routable_skills()
    if not expected:
        print("ERROR: no routable sub-skills found under skills/")
        return 1

    ok = True
    for router in ROUTERS:
        if not router.exists():
            print(f"FAIL: router missing: {router.relative_to(ROOT)}")
            ok = False
            continue
        text = router.read_text(encoding="utf-8")
        missing = sorted(expected - mentioned(text, expected))
        rel = router.relative_to(ROOT)
        if missing:
            print(f"FAIL: {rel} does not mention: {', '.join(missing)}")
            ok = False
        else:
            print(f"OK: {rel} covers all {len(expected)} sub-skills")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
