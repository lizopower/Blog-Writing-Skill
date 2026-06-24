#!/usr/bin/env python3
"""Append-only pipeline receipts for article workspaces."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def log_path(workspace: Path) -> Path:
    return workspace / "logs" / "pipeline.log"


def append_receipt(
    workspace: Path,
    *,
    phase: str,
    skill: str = "",
    artifact: str = "",
    status: str = "ok",
    advance_exit_code: int = 0,
    waive_reason: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    entry: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "phase": phase,
        "skill": skill,
        "artifact": artifact,
        "status": status,
        "advance_exit_code": advance_exit_code,
    }
    if waive_reason:
        entry["waive_reason"] = waive_reason
    if extra:
        entry.update(extra)

    path = log_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def recent_receipts(workspace: Path, limit: int = 3) -> list[dict[str, Any]]:
    path = log_path(workspace)
    if not path.exists():
        return []
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    receipts: list[dict[str, Any]] = []
    for line in lines[-limit:]:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            receipts.append(item)
    return receipts
