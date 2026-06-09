#!/usr/bin/env python3
"""Print compact article workspace context for session-start hooks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def load_statemachine() -> tuple[Any | None, str | None]:
    try:
        import _statemachine
    except Exception as exc:  # pragma: no cover - defensive optional dependency
        return None, f"Lifecycle state machine unavailable: {exc}"
    return _statemachine, None


def load_specstore() -> tuple[Any | None, str | None]:
    try:
        import _specstore
    except Exception as exc:  # pragma: no cover - defensive optional dependency
        return None, f"Project specs unavailable: {exc}"
    return _specstore, None


def article_workspaces(root: Path) -> list[dict[str, Any]]:
    articles_dir = root / "content" / "articles"
    if not articles_dir.exists():
        return []
    workspaces: list[dict[str, Any]] = []
    for workspace in sorted(path for path in articles_dir.iterdir() if path.is_dir() and path.name != "_archive"):
        article_path = workspace / "article.json"
        if not article_path.exists():
            continue
        try:
            article = json.loads(article_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(article, dict):
            continue
        workspaces.append({"slug": workspace.name, "workspace": workspace, "article": article})
    return workspaces


def select_current(workspaces: list[dict[str, Any]], slug: str | None) -> dict[str, Any] | None:
    active = [item for item in workspaces if item["article"].get("currentPhase") != "completed"]
    candidates = active or workspaces
    if slug:
        for item in candidates:
            if item["slug"] == slug:
                return item
        return None
    if not candidates:
        return None
    return max(candidates, key=lambda item: str(item["article"].get("updatedAt", "")))


def render_context(root: Path, slug: str | None = None) -> str:
    statemachine, statemachine_error = load_statemachine()
    specstore, specstore_error = load_specstore()
    workspaces = article_workspaces(root)
    if not workspaces:
        return "No article workspace found.\n"

    current = select_current(workspaces, slug)
    if current is None:
        return f"No article workspace found for slug: {slug}\n"

    article = current["article"]
    if statemachine is not None:
        article = statemachine.migrate(article)
    current_phase = str(article.get("currentPhase", "unknown"))
    track = str(article.get("track", "full"))

    lines = [
        f"Current Target: {current['slug']}",
        f"Phase: {current_phase}",
        f"Track: {track}",
        f"Workspace: {current['workspace']}",
    ]

    other_active = [
        item
        for item in workspaces
        if item["slug"] != current["slug"] and item["article"].get("currentPhase") != "completed"
    ]
    if other_active:
        lines.extend(["", "Other in-progress articles:"])
        for item in sorted(other_active, key=lambda entry: entry["slug"]):
            phase = item["article"].get("currentPhase", "unknown")
            updated_at = item["article"].get("updatedAt", "")
            lines.append(f"- {item['slug']} ({phase}, updatedAt={updated_at})")
            lines.append(f"  Switch with: resume_context.py --slug {item['slug']} --root {root}")

    lines.extend(["", "Next phases:"])
    if statemachine is None:
        lines.append(f"- {statemachine_error or 'Lifecycle state machine unavailable.'}")
    else:
        next_phases = sorted(
            statemachine.TRANSITIONS.get(current_phase, set()),
            key=lambda phase: statemachine.PHASES.index(phase),
        )
        if not next_phases:
            lines.append("- none")
        for phase in next_phases:
            result = statemachine.can_transition(article, phase, current["workspace"])
            status = "ok" if result.ok else f"blocked: {result.reason}"
            lines.append(f"- {phase}: {status}")

    lines.extend(["", "Project specs:"])
    if specstore is None:
        lines.append(f"- {specstore_error or 'Project specs unavailable.'}")
    else:
        specs = read_specs(root, specstore)
        if specs:
            lines.extend(f"- {title} [{scope}] ({spec_id})" for spec_id, title, scope in specs)
        else:
            lines.append("- none")

    return "\n".join(lines).rstrip() + "\n"


def read_specs(root: Path, specstore: Any) -> list[tuple[str, str, str]]:
    specs_dir = root / "content" / "specs"
    if not specs_dir.exists():
        return []
    specs: list[tuple[str, str, str]] = []
    for path in sorted(specs_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        parsed = specstore.parse_spec(path.read_text(encoding="utf-8"))
        specs.append(
            (
                parsed.front_matter.get("id", path.stem),
                parsed.front_matter.get("title", path.stem),
                parsed.front_matter.get("scope", "project"),
            )
        )
    return specs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print article workspace context for session start.")
    parser.add_argument("--root", default=".", help="Project root.")
    parser.add_argument("--slug", help="Current article slug. Defaults to latest updated in-progress article.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    print(render_context(Path(args.root).resolve(), args.slug), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
