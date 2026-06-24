#!/usr/bin/env python3
"""Assemble stage context and recommend the next sub-skill for an article workspace."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from resume_context import PHASE_CONTEXT, render_context  # noqa: E402

PHASE_SKILLS: dict[str, str] = {
    "brainstorming": "blog-brainstorm",
    "brief_confirmed": "blog-brainstorm",
    "research_planning": "tech-research",
    "context_building": "tech-blog-orchestrator",
    "strategy_pressure_test": "grill-me",
    "outlining": "tech-article-architect",
    "drafting": "tech-blog-writer",
    "fact_checking": "fact-checker",
    "editorial_review": "content-taste-advisor",
    "completed": "blog-brainstorm",
}

PROMPT_FILES: dict[str, str] = {
    "brainstorming": "brainstorm.md",
    "research_planning": "research_plan.md",
    "outlining": "outline.md",
    "drafting": "draft.md",
    "fact_checking": "fact_check.md",
    "editorial_review": "editorial_review.md",
}


def bundle_prompts_dir() -> Path:
    runtime_prompts = SCRIPT_DIR.parent / "prompts"
    if runtime_prompts.exists():
        return runtime_prompts
    return REPO_ROOT / "templates" / "prompts"


def load_prompt_template(phase: str) -> str:
    filename = PROMPT_FILES.get(phase)
    if not filename:
        return ""
    path = bundle_prompts_dir() / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def load_article(workspace: Path) -> dict[str, Any]:
    data = json.loads((workspace / "article.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("article.json root must be an object")
    return data


def assemble_stage_context(workspace: Path, phase: str) -> str:
    lines = [f"# Stage context: {phase}", ""]
    for name in PHASE_CONTEXT.get(phase, ()):
        artifact = workspace / name
        lines.append(f"## Artifact: {name}")
        if artifact.exists():
            text = artifact.read_text(encoding="utf-8")
            preview = text[:4000]
            if len(text) > 4000:
                preview += "\n\n...[truncated]..."
            lines.append(preview)
        else:
            lines.append("(missing)")
        lines.append("")

    template = load_prompt_template(phase)
    if template:
        lines.extend(["## Prompt template", "", template])
    return "\n".join(lines)


def write_stage_output(root: Path, slug: str, phase: str, content: str, dry_run: bool) -> Path:
    out_dir = root / "content" / "articles" / slug / "stage"
    out_path = out_dir / f"{phase}_context.txt"
    if dry_run:
        return out_path
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Run or prepare a single article workflow stage.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--slug", required=True, help="Article slug")
    parser.add_argument("--stage", help="Target phase (defaults to article.json currentPhase)")
    parser.add_argument("--dry-run", action="store_true", help="Do not write stage context files")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    workspace = root / "content" / "articles" / args.slug
    if not workspace.is_dir():
        print(f"Error: workspace not found: {workspace}", file=sys.stderr)
        return 1

    article = load_article(workspace)
    phase = args.stage or str(article.get("currentPhase", "brainstorming"))
    skill = PHASE_SKILLS.get(phase, "blog-writing-workflow")

    print(render_context(root, args.slug), end="")
    print("\n--- run_stage receipt ---")
    print(f"slug: {args.slug}")
    print(f"phase: {phase}")
    print(f"recommended_skill: {skill}")
    print(f"artifacts: {', '.join(PHASE_CONTEXT.get(phase, ()))}")

    context = assemble_stage_context(workspace, phase)
    out_path = write_stage_output(root, args.slug, phase, context, args.dry_run)
    if args.dry_run:
        print(f"dry-run: would write {out_path}")
    else:
        print(f"stage_context: {out_path}")

    try:
        from _pipeline_log import append_receipt

        append_receipt(
            workspace,
            phase=phase,
            skill=skill,
            artifact=str(out_path.relative_to(root)) if not args.dry_run else "",
            status="dry-run" if args.dry_run else "prepared",
        )
    except Exception as exc:  # noqa: BLE001 - receipts are advisory, context was already written
        print(f"warning: pipeline receipt not written ({exc})", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
