#!/usr/bin/env python3
"""Pure helpers for the Codex ``AGENTS.md`` lifecycle prelude.

Codex has no ``PreToolUse`` hook, so the mechanical phase gate that protects
Claude sessions cannot run there. To compensate, ``init.py`` writes a managed
block into the project-root ``AGENTS.md`` instructing Codex agents to load
workspace context first and to honour the same lifecycle gates by convention.

The block is delimited by stable markers so it can be refreshed or removed
without disturbing any user-authored content in the same file. The gated
artifacts are sourced from :data:`phase_gate.ARTIFACT_MIN_PHASE` so the prose
prelude and the mechanical gate can never drift apart.
"""

from __future__ import annotations

from phase_gate import ARTIFACT_MIN_PHASE
from _runtimeinstaller import RUNTIME_ROOT


PRELUDE_FILENAME = "AGENTS.md"
MARKER_BEGIN = "<!-- BEGIN blog-writing-skill (managed) -->"
MARKER_END = "<!-- END blog-writing-skill (managed) -->"

RUNTIME_SCRIPTS = f"{RUNTIME_ROOT}/runtime/scripts"


def render_prelude() -> str:
    """Render the managed lifecycle prelude block (marker-delimited)."""
    resume = f"{RUNTIME_SCRIPTS}/resume_context.py"
    article = f"{RUNTIME_SCRIPTS}/article.py"
    gates = "\n".join(
        f"- `{name}` requires lifecycle phase `{phase}` or later."
        for name, phase in ARTIFACT_MIN_PHASE.items()
    )
    return (
        f"{MARKER_BEGIN}\n"
        "## Blog-Writing-Skill lifecycle (Codex)\n"
        "\n"
        "This project uses the Blog-Writing-Skill article lifecycle. Codex has no\n"
        "PreToolUse gate, so these rules are enforced by convention — follow them.\n"
        "\n"
        "**At session start**, load the current article target, phase, and the\n"
        "exact artifacts that phase needs:\n"
        "\n"
        "```\n"
        f"python {resume} --root .\n"
        "```\n"
        "\n"
        "**Lifecycle gates.** Do not create or edit these workspace artifacts\n"
        "before the article reaches the listed phase:\n"
        "\n"
        f"{gates}\n"
        "\n"
        "Advance phases only through the lifecycle CLI — never edit `article.json`\n"
        "by hand:\n"
        "\n"
        "```\n"
        f"python {article} advance --slug <slug> --to <next-phase> --root .\n"
        "```\n"
        "\n"
        "Do not work around a gate by writing the artifact elsewhere. A gate may\n"
        "be waived only with explicit user approval.\n"
        f"{MARKER_END}\n"
    )


def upsert_prelude(existing: str, block: str) -> str:
    """Return ``existing`` with the managed ``block`` inserted or refreshed.

    If a managed block is already present it is replaced in place, preserving
    everything outside the markers. Otherwise the block is appended after the
    existing content (or becomes the whole file when ``existing`` is blank).
    """
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
