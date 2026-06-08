#!/usr/bin/env python3
"""Validate a Blog-Writing-Skill Context Pack.

This validator intentionally avoids third-party dependencies so it can run in
agent environments before article drafting.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "version",
    "generated_at",
    "topic",
    "audience",
    "industry_context",
    "key_claims",
    "extracted_tables",
    "glossary",
    "risk_notes",
    "research_summary",
    "file_summary",
]

VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_SOURCE_TYPES = {"pdf", "excel", "word", "web", "research", "user_provided"}
VALID_RISK_TYPES = {"data_gap", "uncertainty", "conflict", "limitation"}
VALID_COLUMN_TYPES = {"string", "number", "date", "boolean"}


def _is_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _add(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def validate_context_pack(data: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    """Return (is_valid, errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            _add(errors, field, "missing required field")

    version = data.get("version")
    if not isinstance(version, str) or not version.count(".") == 2:
        _add(errors, "version", "must be a semantic version string such as 2.1.0")

    if not _is_iso_datetime(data.get("generated_at")):
        _add(errors, "generated_at", "must be an ISO 8601 timestamp")

    topic = data.get("topic")
    if not isinstance(topic, str) or len(topic.strip()) < 5:
        _add(errors, "topic", "must be a string with at least 5 characters")

    audience = data.get("audience")
    if not isinstance(audience, list) or not audience:
        _add(errors, "audience", "must be a non-empty array")
    elif not all(isinstance(item, str) and item.strip() for item in audience):
        _add(errors, "audience", "all items must be non-empty strings")

    industry_context = data.get("industry_context")
    if not isinstance(industry_context, dict):
        _add(errors, "industry_context", "must be an object")
    else:
        for field in ["industry", "market_segment", "core_advantage"]:
            if not isinstance(industry_context.get(field), str) or not industry_context.get(field, "").strip():
                _add(errors, f"industry_context.{field}", "must be a non-empty string")

    key_claims = data.get("key_claims")
    if not isinstance(key_claims, list) or not key_claims:
        _add(errors, "key_claims", "must be a non-empty array")
    else:
        for idx, claim in enumerate(key_claims):
            loc = f"key_claims[{idx}]"
            if not isinstance(claim, dict):
                _add(errors, loc, "must be an object")
                continue
            if not isinstance(claim.get("claim"), str) or len(claim.get("claim", "").strip()) < 10:
                _add(errors, f"{loc}.claim", "must be a meaningful claim string")
            if claim.get("confidence") not in VALID_CONFIDENCE:
                _add(errors, f"{loc}.confidence", "must be high, medium, or low")

            source = claim.get("source")
            if not isinstance(source, dict):
                _add(errors, f"{loc}.source", "must be an object with type and reference")
            else:
                if source.get("type") not in VALID_SOURCE_TYPES:
                    _add(errors, f"{loc}.source.type", f"must be one of {sorted(VALID_SOURCE_TYPES)}")
                if not isinstance(source.get("reference"), str) or len(source.get("reference", "").strip()) < 5:
                    _add(errors, f"{loc}.source.reference", "must be a traceable reference string")
                if source.get("credibility") and source.get("credibility") not in VALID_CONFIDENCE:
                    _add(errors, f"{loc}.source.credibility", "must be high, medium, or low")
                if source.get("verified_at") and not _is_iso_datetime(source.get("verified_at")):
                    _add(errors, f"{loc}.source.verified_at", "must be an ISO 8601 timestamp")

    extracted_tables = data.get("extracted_tables")
    if not isinstance(extracted_tables, list):
        _add(errors, "extracted_tables", "must be an array")
    else:
        for idx, table in enumerate(extracted_tables):
            loc = f"extracted_tables[{idx}]"
            if not isinstance(table, dict):
                _add(errors, loc, "must be an object")
                continue
            for field in ["table_id", "source", "columns", "data"]:
                if field not in table:
                    _add(errors, f"{loc}.{field}", "missing required field")
            if not isinstance(table.get("table_id"), str) or not table.get("table_id", "").startswith("table_"):
                _add(errors, f"{loc}.table_id", "must start with table_")
            if not isinstance(table.get("source"), str) or len(table.get("source", "").strip()) < 5:
                _add(errors, f"{loc}.source", "must be a traceable source string")

            columns = table.get("columns")
            if not isinstance(columns, list) or not columns:
                _add(errors, f"{loc}.columns", "must be a non-empty array")
                column_names: list[str] = []
            else:
                column_names = []
                for col_idx, column in enumerate(columns):
                    col_loc = f"{loc}.columns[{col_idx}]"
                    if not isinstance(column, dict):
                        _add(errors, col_loc, "must be an object")
                        continue
                    name = column.get("name")
                    if not isinstance(name, str) or not name.strip():
                        _add(errors, f"{col_loc}.name", "must be a non-empty string")
                    else:
                        column_names.append(name)
                    col_type = column.get("type", "string")
                    if col_type not in VALID_COLUMN_TYPES:
                        _add(errors, f"{col_loc}.type", f"must be one of {sorted(VALID_COLUMN_TYPES)}")
                    if col_type == "number" and not column.get("unit"):
                        _add(errors, f"{col_loc}.unit", "numeric columns must include a unit")

            rows = table.get("data")
            if not isinstance(rows, list):
                _add(errors, f"{loc}.data", "must be an array")
            else:
                for row_idx, row in enumerate(rows):
                    row_loc = f"{loc}.data[{row_idx}]"
                    if not isinstance(row, dict):
                        _add(errors, row_loc, "must be an object; use array_of_objects format")
                        continue
                    missing = [name for name in column_names if name not in row]
                    if missing:
                        _add(warnings, row_loc, f"missing values for columns: {', '.join(missing)}")

    glossary = data.get("glossary")
    if not isinstance(glossary, list):
        _add(errors, "glossary", "must be an array")
    else:
        for idx, item in enumerate(glossary):
            loc = f"glossary[{idx}]"
            if not isinstance(item, dict):
                _add(errors, loc, "must be an object")
                continue
            if not item.get("term"):
                _add(errors, f"{loc}.term", "must be present")
            if not item.get("definition"):
                _add(errors, f"{loc}.definition", "must be present")

    risk_notes = data.get("risk_notes")
    if not isinstance(risk_notes, list):
        _add(errors, "risk_notes", "must be an array")
    else:
        for idx, risk in enumerate(risk_notes):
            loc = f"risk_notes[{idx}]"
            if not isinstance(risk, dict):
                _add(errors, loc, "must be an object")
                continue
            if risk.get("risk_type") not in VALID_RISK_TYPES:
                _add(errors, f"{loc}.risk_type", f"must be one of {sorted(VALID_RISK_TYPES)}")
            if not risk.get("description"):
                _add(errors, f"{loc}.description", "must be present")

    research_summary = data.get("research_summary")
    if not isinstance(research_summary, dict):
        _add(errors, "research_summary", "must be an object")
    else:
        if not isinstance(research_summary.get("sources_count"), int):
            _add(errors, "research_summary.sources_count", "must be an integer")
        if not _is_iso_datetime(research_summary.get("last_updated")):
            _add(errors, "research_summary.last_updated", "must be an ISO 8601 timestamp")
        if not isinstance(research_summary.get("key_findings"), list):
            _add(errors, "research_summary.key_findings", "must be an array")

    file_summary = data.get("file_summary")
    if not isinstance(file_summary, dict):
        _add(errors, "file_summary", "must be an object")
    else:
        if not isinstance(file_summary.get("files_processed"), list):
            _add(errors, "file_summary.files_processed", "must be an array")
        if not isinstance(file_summary.get("total_pages"), int):
            _add(errors, "file_summary.total_pages", "must be an integer")
        if not isinstance(file_summary.get("extraction_notes"), list):
            _add(errors, "file_summary.extraction_notes", "must be an array")

    if isinstance(research_summary, dict) and isinstance(file_summary, dict):
        source_count = research_summary.get("sources_count", 0)
        files_processed = file_summary.get("files_processed", [])
        if source_count == 0 and not files_processed:
            _add(warnings, "source_coverage", "no research sources and no files processed")

    return not errors, errors, warnings


def validate_from_file(file_path: str | Path) -> tuple[bool, list[str], list[str]]:
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        return False, [f"invalid JSON: {exc}"], []
    except FileNotFoundError:
        return False, [f"file not found: {file_path}"], []

    if not isinstance(data, dict):
        return False, ["root: must be a JSON object"], []

    return validate_context_pack(data)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_context_pack.py <context_pack.json>")
        return 2

    is_valid, errors, warnings = validate_from_file(sys.argv[1])

    if is_valid:
        print("Context Pack is VALID")
        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for idx, warning in enumerate(warnings, 1):
                print(f"  {idx}. {warning}")
        return 0

    print("Context Pack is INVALID")
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
