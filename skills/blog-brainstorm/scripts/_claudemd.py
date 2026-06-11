#!/usr/bin/env python3
"""Pure helpers for the Claude ``CLAUDE.md`` project prelude.

Scaffold-only installs do not make Blog-Writing-Skill discoverable as a global
Claude skill. The project therefore needs a small managed instruction block
that tells Claude where the scaffold lives and which workflow files to read
before handling article requests.
"""

from __future__ import annotations

from pathlib import Path


PRELUDE_FILENAME = "CLAUDE.md"
MARKER_BEGIN = "<!-- BEGIN blog-writing-skill claude (managed) -->"
MARKER_END = "<!-- END blog-writing-skill claude (managed) -->"


def render_prelude(scaffold_root: Path) -> str:
    """Render the managed Claude project prelude block."""
    scaffold = scaffold_root.resolve()
    root_skill = scaffold / "SKILL.md"
    router_skill = scaffold / "skills" / "blog-writing-skills" / "SKILL.md"
    workflow_skill = scaffold / "skills" / "blog-writing-workflow" / "SKILL.md"
    brainstorm_skill = scaffold / "skills" / "blog-brainstorm" / "SKILL.md"
    article_cli = scaffold / "skills" / "blog-brainstorm" / "scripts" / "article.py"
    return (
        f"{MARKER_BEGIN}\n"
        "## Blog-Writing-Skill project instructions (Claude)\n"
        "\n"
        "This project uses Blog-Writing-Skill from this scaffold checkout:\n"
        "\n"
        f"`{scaffold}`\n"
        "\n"
        "Claude plugin/skill discovery is not required for this scaffold-only setup.\n"
        "For any request to brainstorm, plan, write, draft, outline, research,\n"
        "fact-check, or review a technical/B2B article, first read and follow the\n"
        "workflow instructions from the scaffold:\n"
        "\n"
        f"- Root router: `{root_skill}`\n"
        f"- Codex/router mirror: `{router_skill}`\n"
        f"- Full article workflow: `{workflow_skill}`\n"
        f"- Brainstorm/workspace creation: `{brainstorm_skill}`\n"
        "\n"
        "Important workflow rules:\n"
        "- A complete article request must go through `blog-writing-workflow`; do\n"
        "  not draft directly from the chat prompt.\n"
        "- Rich input is not a waiver. Title, audience, keywords, source links,\n"
        "  pasted notes, desired structure, CTA, tone, and word count are raw\n"
        "  workflow material, not a validated Context Pack or approved outline.\n"
        "- Do not manually create `content/articles/<slug>/` with shell commands.\n"
        "  Use the lifecycle CLI instead:\n"
        "\n"
        "```\n"
        f"python {article_cli} create \"<Working Title>\" --root .\n"
        "```\n"
        "\n"
        "- The main session is the only orchestrator, canonical writer, and phase\n"
        "  advancer. Spawned workers, if any, may write scratch outputs only.\n"
        "- Never edit `article.json.currentPhase` by hand; use `article.py advance`.\n"
        "- Respect the installed PreToolUse phase gate. Do not work around it by\n"
        "  writing gated artifacts elsewhere.\n"
        f"{MARKER_END}\n"
    )


def upsert_prelude(existing: str, block: str) -> str:
    """Return ``existing`` with the managed ``block`` inserted or refreshed."""
    block = block.strip("\n")
    if MARKER_BEGIN in existing and MARKER_END in existing:
        start = existing.index(MARKER_BEGIN)
        end = existing.index(MARKER_END) + len(MARKER_END)
        return existing[:start] + block + existing[end:]
    base = existing.rstrip("\n")
    if not base.strip():
        return block + "\n"
    return f"{base}\n\n{block}\n"


def remove_prelude(existing: str) -> str:
    """Return ``existing`` with the managed block stripped, user content kept."""
    if MARKER_BEGIN not in existing or MARKER_END not in existing:
        return existing
    start = existing.index(MARKER_BEGIN)
    end = existing.index(MARKER_END) + len(MARKER_END)
    prefix = existing[:start].rstrip("\n")
    suffix = existing[end:].lstrip("\n")
    if prefix and suffix:
        return f"{prefix}\n\n{suffix}"
    remainder = (prefix + suffix).strip("\n")
    return f"{remainder}\n" if remainder else ""
