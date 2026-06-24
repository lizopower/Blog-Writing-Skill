#!/usr/bin/env python3
"""Validate a Blog-Writing-Skill article workspace skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from create_article_workspace import VALID_ARTICLE_TYPES


REQUIRED_FILES = [
    "article.json",
    "brief.md",
    "research",
    "sources.jsonl",
    "context_pack.json",
    "strategy.md",
    "outline.md",
    "draft.md",
    "fact_check.md",
    "editorial_review.md",
    "finish.md",
]

VALID_PHASES = {
    "brainstorming",
    "brief_confirmed",
    "research_planning",
    "context_building",
    "strategy_pressure_test",
    "outlining",
    "drafting",
    "fact_checking",
    "editorial_review",
    "completed",
}


def _load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"{path}: file not found"
    except json.JSONDecodeError as exc:
        return None, f"{path}: invalid JSON: {exc}"

    if not isinstance(data, dict):
        return None, f"{path}: root must be an object"
    return data, None


def validate_workspace(workspace: Path) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not workspace.exists():
        return False, [f"{workspace}: workspace does not exist"], warnings
    if not workspace.is_dir():
        return False, [f"{workspace}: workspace is not a directory"], warnings

    for relative_path in REQUIRED_FILES:
        target = workspace / relative_path
        if not target.exists():
            errors.append(f"missing required artifact: {relative_path}")
        elif relative_path == "research" and not target.is_dir():
            errors.append("research must be a directory")
        elif relative_path != "research" and not target.is_file():
            errors.append(f"{relative_path} must be a file")

    article, article_error = _load_json(workspace / "article.json")
    if article_error:
        errors.append(article_error)
    elif article:
        for field in ["id", "title", "status", "currentPhase", "nextAction", "createdAt", "updatedAt"]:
            if not article.get(field):
                errors.append(f"article.json.{field}: missing or empty")
        phase = article.get("currentPhase")
        if phase not in VALID_PHASES:
            errors.append(f"article.json.currentPhase: invalid phase {phase!r}")
        article_type = article.get("articleType")
        if article_type is not None and article_type not in VALID_ARTICLE_TYPES:
            errors.append(f"article.json.articleType: invalid value {article_type!r}")

    context_pack, context_error = _load_json(workspace / "context_pack.json")
    if context_error:
        errors.append(context_error)
    elif context_pack:
        version = context_pack.get("version")
        if version and not str(version).startswith("2."):
            warnings.append(f"context_pack.json.version: expected v2.x, got {version}")

    for relative_path in ["brief.md", "strategy.md", "outline.md"]:
        target = workspace / relative_path
        if target.exists() and target.is_file() and not target.read_text(encoding="utf-8").strip():
            warnings.append(f"{relative_path}: empty artifact")

    return not errors, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an article workspace skeleton.")
    parser.add_argument("workspace", help="Path to content/articles/<slug>.")
    args = parser.parse_args()

    ok, errors, warnings = validate_workspace(Path(args.workspace).resolve())
    if ok:
        print("Article workspace is VALID")
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for idx, warning in enumerate(warnings, 1):
                print(f"  {idx}. {warning}")
        return 0

    print("Article workspace is INVALID")
    print(f"\nErrors ({len(errors)}):")
    for idx, error in enumerate(errors, 1):
        print(f"  {idx}. {error}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for idx, warning in enumerate(warnings, 1):
            print(f"  {idx}. {warning}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
