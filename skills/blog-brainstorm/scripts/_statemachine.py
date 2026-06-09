#!/usr/bin/env python3
"""Pure lifecycle state machine logic for article workspaces."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PHASES = [
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
]

TRANSITIONS: dict[str, set[str]] = {
    "brainstorming": {"brief_confirmed"},
    "brief_confirmed": {"research_planning"},
    "research_planning": {"context_building"},
    "context_building": {"strategy_pressure_test"},
    "strategy_pressure_test": {"outlining", "drafting"},
    "outlining": {"drafting"},
    "drafting": {"fact_checking", "outlining"},
    "fact_checking": {"editorial_review", "drafting"},
    "editorial_review": {"completed", "drafting"},
    "completed": set(),
}

VALID_TRACKS = {"full", "lightweight"}


@dataclass(frozen=True)
class TransitionResult:
    ok: bool
    reason: str = ""


def migrate(article: dict[str, Any]) -> dict[str, Any]:
    """Return a migrated copy of an article.json mapping."""

    migrated = copy.deepcopy(article)
    if migrated.get("track") not in VALID_TRACKS:
        migrated["track"] = "full"
    if not isinstance(migrated.get("waivers"), list):
        migrated["waivers"] = []
    if not isinstance(migrated.get("history"), list):
        migrated["history"] = []
    if "series" not in migrated:
        migrated["series"] = None
    return migrated


def transition_legality(article: dict[str, Any], target_phase: str) -> TransitionResult:
    """Graph-level legality of a phase transition.

    This is the *hard* layer: valid phases, the transition graph, and the
    full-track ordering rule. It is never waivable — a waiver may excuse a
    missing artifact (a `_gate` failure), but must not let an article skip
    phases (e.g. brainstorming -> completed) and fabricate a terminal state.
    """
    migrated = migrate(article)
    current_phase = str(migrated.get("currentPhase", ""))
    track = str(migrated.get("track", "full"))

    if target_phase not in PHASES:
        return TransitionResult(False, f"unknown target phase {target_phase!r}")
    if current_phase not in TRANSITIONS:
        return TransitionResult(False, f"unknown current phase {current_phase!r}")
    if target_phase not in TRANSITIONS[current_phase]:
        return TransitionResult(False, f"illegal transition {current_phase}->{target_phase}")
    if current_phase == "strategy_pressure_test" and target_phase == "drafting" and track != "lightweight":
        return TransitionResult(False, "full track must pass through outlining before drafting")
    return TransitionResult(True)


def can_transition(article: dict[str, Any], target_phase: str, workspace: Path) -> TransitionResult:
    legality = transition_legality(article, target_phase)
    if not legality.ok:
        return legality

    migrated = migrate(article)
    current_phase = str(migrated.get("currentPhase", ""))
    track = str(migrated.get("track", "full"))
    return _gate(target_phase, current_phase, track, workspace)


def advance_article(
    article: dict[str, Any],
    target_phase: str,
    workspace: Path,
    *,
    waive_reason: str | None = None,
    now: str,
) -> tuple[dict[str, Any], TransitionResult]:
    migrated = migrate(article)
    current_phase = str(migrated.get("currentPhase", ""))

    # Legality is enforced unconditionally; only the artifact gate is waivable.
    legality = transition_legality(migrated, target_phase)
    if not legality.ok:
        return migrated, legality

    track = str(migrated.get("track", "full"))
    gate = _gate(target_phase, current_phase, track, workspace)
    reason = (waive_reason or "").strip()

    if not gate.ok and not reason:
        return migrated, gate

    updated = copy.deepcopy(migrated)
    updated["currentPhase"] = target_phase
    updated["status"] = target_phase
    updated["updatedAt"] = now
    updated["nextAction"] = "article completed" if target_phase == "completed" else f"continue from {target_phase}"
    updated["history"] = [
        *list(updated.get("history", [])),
        {"from": current_phase, "to": target_phase, "at": now},
    ]

    if not gate.ok:
        updated["waivers"] = [
            *list(updated.get("waivers", [])),
            {"from": current_phase, "to": target_phase, "reason": reason, "at": now},
        ]
        return updated, TransitionResult(True, f"waived: {gate.reason}")

    return updated, gate


def _gate(target_phase: str, current_phase: str, track: str, workspace: Path) -> TransitionResult:
    workspace_result = _workspace_shape_ok(workspace)
    if not workspace_result.ok:
        return workspace_result

    checks = {
        "brief_confirmed": lambda: _brief_has_required_sections(workspace / "brief.md"),
        "context_building": lambda: _sources_have_entries(workspace / "sources.jsonl"),
        "strategy_pressure_test": lambda: _context_pack_valid(workspace / "context_pack.json"),
        "outlining": lambda: _section_has_body(workspace / "strategy.md", "Resolved Decisions"),
        "drafting": lambda: TransitionResult(True)
        if current_phase == "strategy_pressure_test" and track == "lightweight"
        else _file_has_body(workspace / "outline.md", "outline.md"),
        "fact_checking": lambda: _file_has_body(workspace / "draft.md", "draft.md"),
        "editorial_review": lambda: _file_has_body(workspace / "fact_check.md", "fact_check.md"),
        "completed": lambda: _completed_gate(workspace),
    }
    check = checks.get(target_phase)
    if check is None:
        return TransitionResult(True)
    return check()


def _workspace_shape_ok(workspace: Path) -> TransitionResult:
    if not workspace.exists():
        return TransitionResult(False, f"{workspace}: workspace does not exist")
    if not workspace.is_dir():
        return TransitionResult(False, f"{workspace}: workspace is not a directory")
    return TransitionResult(True)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _body_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def _file_has_body(path: Path, label: str) -> TransitionResult:
    if _body_lines(_read_text(path)):
        return TransitionResult(True)
    return TransitionResult(False, f"{label} must be non-empty")


def _section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def _section_has_body(path: Path, heading: str) -> TransitionResult:
    if _body_lines(_section_body(_read_text(path), heading)):
        return TransitionResult(True)
    return TransitionResult(False, f"{path.name} section {heading!r} must be non-empty")


def _brief_has_required_sections(path: Path) -> TransitionResult:
    text = _read_text(path)
    for heading in ["Business Goal", "Target Audience", "Recommended Angle"]:
        if not _body_lines(_section_body(text, heading)):
            return TransitionResult(False, f"brief.md section {heading!r} must be non-empty")
    return TransitionResult(True)


def _sources_have_entries(path: Path) -> TransitionResult:
    entries = [line.strip() for line in _read_text(path).splitlines() if line.strip()]
    if entries:
        return TransitionResult(True)
    return TransitionResult(False, "sources.jsonl must contain at least one source")


def _context_pack_valid(path: Path) -> TransitionResult:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return TransitionResult(False, "context_pack.json must exist")
    except json.JSONDecodeError as exc:
        return TransitionResult(False, f"context_pack.json must be valid JSON: {exc}")
    if not isinstance(data, dict):
        return TransitionResult(False, "context_pack.json root must be an object")
    if not str(data.get("version", "")).startswith("2."):
        return TransitionResult(False, "context_pack.json version must be 2.x")
    if not data.get("topic"):
        return TransitionResult(False, "context_pack.json topic must be non-empty")
    if not isinstance(data.get("audience"), list) or not data["audience"]:
        return TransitionResult(False, "context_pack.json audience must be non-empty")
    if not isinstance(data.get("key_claims"), list) or not data["key_claims"]:
        return TransitionResult(False, "context_pack.json key_claims must be non-empty")
    return TransitionResult(True)


def _completed_gate(workspace: Path) -> TransitionResult:
    fact_check = _read_text(workspace / "fact_check.md")
    if not re.search(r"\bPASS(?:ED)?\b", fact_check, re.IGNORECASE):
        return TransitionResult(False, "fact_check.md must record PASS before completed")
    return _file_has_body(workspace / "editorial_review.md", "editorial_review.md")
