#!/usr/bin/env python3
"""Diagnose whether a project is fully initialized for Blog-Writing-Skill.

The `create` hard gate only fires when a workspace is first created. Projects
initialized by an older release, or with ``--no-hooks``, can resume without the
runtime scripts or hooks the workflow expects. ``diagnose`` reports those gaps
so ``article.py doctor`` and ``init.py --check`` can surface and fix them.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _hookinstaller import MANAGED_BY, PRE_TOOL_USE_MATCHER, SESSION_MATCHERS
from _runtimeinstaller import (
    RUNTIME_ROOT,
    destination_path,
    load_hashes,
    runtime_root,
    sha256_text,
    template_files,
)
from install_session_hook import HARNESS_CONFIG, config_path, load_json


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class Diagnosis:
    harness: str
    checks: tuple[Check, ...]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


def _is_managed(entry: Any) -> bool:
    return isinstance(entry, dict) and entry.get("_managed_by") == MANAGED_BY


def _managed_entries(config: dict[str, Any], event: str) -> list[dict[str, Any]]:
    hooks = config.get("hooks") if isinstance(config, dict) else None
    if not isinstance(hooks, dict):
        return []
    entries = hooks.get(event)
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if _is_managed(entry)]


def _command_of(entry: dict[str, Any]) -> str:
    hooks = entry.get("hooks")
    if isinstance(hooks, list) and hooks and isinstance(hooks[0], dict):
        return str(hooks[0].get("command", ""))
    return ""


def _targets_runtime_script(entries: list[dict[str, Any]], script: str) -> bool:
    """True only if every managed entry runs the expected runtime script.

    Catches the "right count, wrong/stale command" case an older managed config
    can otherwise hide (e.g. a command still pointing at a removed script path).
    """
    if not entries:
        return False
    return all(RUNTIME_ROOT in _command_of(entry) and script in _command_of(entry) for entry in entries)


def _runtime_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    rroot = runtime_root(root)
    checks.append(Check("runtime_dir", rroot.is_dir(), str(rroot) if rroot.is_dir() else f"missing {rroot}"))

    registry = load_hashes(root)
    files = registry.get("files", {}) if isinstance(registry, dict) else {}
    missing: list[str] = []
    modified: list[str] = []
    conflicts: list[str] = []
    unverified: list[str] = []
    for template in template_files():
        rel = template.destination.as_posix()
        path = destination_path(root, template)
        if not path.exists():
            missing.append(rel)
            continue
        if path.with_name(path.name + ".new").exists():
            conflicts.append(rel)
        stored = files.get(rel)
        stored_hash = stored.get("sha256") if isinstance(stored, dict) else None
        if stored_hash is None:
            # File present but the template-hashes registry has no entry for it,
            # so we cannot confirm it matches a known release.
            unverified.append(rel)
        elif sha256_text(path.read_text(encoding="utf-8")) != stored_hash:
            modified.append(rel)

    checks.append(
        Check(
            "runtime_scripts",
            not missing,
            "all present" if not missing else f"missing: {', '.join(missing)}",
        )
    )
    issues = []
    if modified:
        issues.append(f"modified/unverified: {', '.join(modified)}")
    if conflicts:
        issues.append(f"unresolved .new: {', '.join(conflicts)}")
    if unverified:
        issues.append(f"no registry hash: {', '.join(unverified)}")
    checks.append(Check("runtime_fresh", not issues, "up to date" if not issues else "; ".join(issues)))
    return checks


def _hook_checks(root: Path, harness: str) -> list[Check]:
    checks: list[Check] = []
    path = config_path(root, harness)
    config: dict[str, Any] = {}
    if not path.exists():
        checks.append(Check("hook_config", False, f"missing {path}"))
    else:
        try:
            config = load_json(path)
            checks.append(Check("hook_config", True, str(path)))
        except ValueError as exc:
            checks.append(Check("hook_config", False, f"invalid: {exc}"))

    session = _managed_entries(config, "SessionStart")
    session_matchers = {entry.get("matcher") for entry in session}
    session_ok = session_matchers == set(SESSION_MATCHERS) and _targets_runtime_script(session, "session_start.py")
    if not session:
        session_detail = "no managed SessionStart entries"
    elif session_matchers != set(SESSION_MATCHERS):
        session_detail = f"matchers {sorted(m for m in session_matchers if m)} != {list(SESSION_MATCHERS)}"
    elif not session_ok:
        session_detail = "command not pointing at runtime session_start.py"
    else:
        session_detail = f"{len(session)} entries -> runtime session_start.py"
    checks.append(Check("hook_session_start", session_ok, session_detail))

    _dir, _file, _timeout, gate_supported, breadcrumb_supported = HARNESS_CONFIG[harness]
    if gate_supported:
        gate = _managed_entries(config, "PreToolUse")
        gate_ok = (
            bool(gate)
            and all(entry.get("matcher") == PRE_TOOL_USE_MATCHER for entry in gate)
            and _targets_runtime_script(gate, "phase_gate.py")
        )
        checks.append(
            Check("hook_phase_gate", gate_ok, f"{PRE_TOOL_USE_MATCHER} -> phase_gate.py" if gate_ok else "missing or misconfigured managed PreToolUse gate")
        )
    if breadcrumb_supported:
        breadcrumb = _managed_entries(config, "UserPromptSubmit")
        breadcrumb_ok = (
            bool(breadcrumb)
            and all("matcher" not in entry for entry in breadcrumb)
            and _targets_runtime_script(breadcrumb, "inject_workflow_state.py")
        )
        checks.append(
            Check(
                "hook_breadcrumb",
                breadcrumb_ok,
                "matcherless -> inject_workflow_state.py" if breadcrumb_ok else "missing or misconfigured managed UserPromptSubmit breadcrumb",
            )
        )
    return checks


def diagnose(root: Path, harness: str) -> Diagnosis:
    if harness not in HARNESS_CONFIG:
        raise ValueError(f"unknown harness: {harness}")
    root = root.resolve()
    checks = _runtime_checks(root) + _hook_checks(root, harness)
    return Diagnosis(harness, tuple(checks))


def render_report(diagnosis: Diagnosis) -> str:
    header = f"Blog-Writing-Skill doctor [{diagnosis.harness}]: {'OK' if diagnosis.ok else 'PROBLEMS'}"
    lines = [header]
    for check in diagnosis.checks:
        lines.append(f"  [{'ok' if check.ok else 'FAIL'}] {check.name}: {check.detail}")
    if not diagnosis.ok:
        init_path = Path(__file__).resolve().with_name("init.py")
        lines.append(
            f"  Fix: python {init_path} --root <project-root> --harness {diagnosis.harness} "
            "(reinstalls runtime + hooks; resolve any .new files first)."
        )
    return "\n".join(lines)
