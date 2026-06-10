#!/usr/bin/env python3
"""Validate a Blog-Writing-Skill Context Pack.

This validator intentionally avoids third-party dependencies so it can run in
agent environments before article drafting.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
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
VALID_EXPERIENCE_USES = {"story_anchor", "expert_commentary", "guardrail", "preference"}
STYLE_EXEMPLAR_FIELDS = {"reference", "scope", "what_to_emulate", "what_to_avoid"}
CORE_OFFERING_FIELDS = {"name", "value_prop", "target_user", "when_to_mention", "source_ref"}
AUTHOR_EXPERIENCE_FIELDS = {"note", "source_ref", "usable_as"}

# SEO strategy layer (schema 2.3.0). Optional; validated only when present.
VALID_SEARCH_INTENTS = {"informational", "commercial", "transactional", "navigational"}
VALID_SERP_DEVICES = {"desktop", "mobile", "unknown"}
VALID_ON_STALE = {"warn", "fail"}
VALID_BUYER_STAGES = {"awareness", "consideration", "decision"}
VALID_PAGE_TYPES = {"guide", "comparison", "category", "landing", "faq", "case_study"}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEFAULT_SERP_MAX_AGE_DAYS = 90
META_TITLE_MAX = 60
META_DESCRIPTION_MAX = 155


def _is_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _parse_iso_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


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
        _add(errors, "version", "must be a semantic version string such as 2.3.0")

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

    style_exemplars = data.get("style_exemplars")
    if style_exemplars is not None:
        if not isinstance(style_exemplars, list):
            _add(errors, "style_exemplars", "must be an array when present")
        else:
            for idx, exemplar in enumerate(style_exemplars):
                loc = f"style_exemplars[{idx}]"
                if not isinstance(exemplar, dict):
                    _add(errors, loc, "must be an object")
                    continue
                extra = set(exemplar) - STYLE_EXEMPLAR_FIELDS
                if extra:
                    _add(errors, loc, f"unexpected fields: {', '.join(sorted(extra))}")
                if not isinstance(exemplar.get("reference"), str) or not exemplar.get("reference", "").strip():
                    _add(errors, f"{loc}.reference", "must be a non-empty string")
                if exemplar.get("scope") != "style_only":
                    _add(errors, f"{loc}.scope", "must be style_only; exemplars are not factual sources")
                for field in ["what_to_emulate", "what_to_avoid"]:
                    if field in exemplar and not isinstance(exemplar.get(field), list):
                        _add(errors, f"{loc}.{field}", "must be an array when present")

    core_offerings = data.get("core_offerings")
    if core_offerings is not None:
        if not isinstance(core_offerings, list):
            _add(errors, "core_offerings", "must be an array when present")
        else:
            for idx, offering in enumerate(core_offerings):
                loc = f"core_offerings[{idx}]"
                if not isinstance(offering, dict):
                    _add(errors, loc, "must be an object")
                    continue
                extra = set(offering) - CORE_OFFERING_FIELDS
                if extra:
                    _add(errors, loc, f"unexpected fields: {', '.join(sorted(extra))}")
                for field in ["name", "value_prop", "target_user"]:
                    if not isinstance(offering.get(field), str) or not offering.get(field, "").strip():
                        _add(errors, f"{loc}.{field}", "must be a non-empty string")
                if not isinstance(offering.get("source_ref"), str) or len(offering.get("source_ref", "").strip()) < 5:
                    _add(errors, f"{loc}.source_ref", "must be a traceable string with at least 5 characters")
                if "when_to_mention" in offering and not isinstance(offering.get("when_to_mention"), str):
                    _add(errors, f"{loc}.when_to_mention", "must be a string when present")

    author_experience_notes = data.get("author_experience_notes")
    if author_experience_notes is not None:
        if not isinstance(author_experience_notes, list):
            _add(errors, "author_experience_notes", "must be an array when present")
        else:
            for idx, note in enumerate(author_experience_notes):
                loc = f"author_experience_notes[{idx}]"
                if not isinstance(note, dict):
                    _add(errors, loc, "must be an object")
                    continue
                extra = set(note) - AUTHOR_EXPERIENCE_FIELDS
                if extra:
                    _add(errors, loc, f"unexpected fields: {', '.join(sorted(extra))}")
                if not isinstance(note.get("note"), str) or not note.get("note", "").strip():
                    _add(errors, f"{loc}.note", "must be a non-empty string")
                if not isinstance(note.get("source_ref"), str) or len(note.get("source_ref", "").strip()) < 5:
                    _add(errors, f"{loc}.source_ref", "must be a traceable string with at least 5 characters")
                if "usable_as" in note and note.get("usable_as") not in VALID_EXPERIENCE_USES:
                    _add(errors, f"{loc}.usable_as", f"must be one of {sorted(VALID_EXPERIENCE_USES)}")

    if "seo_strategy" in data:
        _validate_seo_strategy(data.get("seo_strategy"), errors, warnings)

    if "seo_finalization" in data:
        _validate_seo_finalization(data.get("seo_finalization"), errors)

    return not errors, errors, warnings


def _validate_seo_strategy(seo: Any, errors: list[str], warnings: list[str]) -> None:
    """Validate the optional SEO strategy layer (schema 2.3.0).

    English-first: meta length caps and slug rules assume English markets.
    Only invoked when ``seo_strategy`` is present, so packs without it stay
    backward compatible.
    """
    if not isinstance(seo, dict):
        _add(errors, "seo_strategy", "must be an object when present")
        return

    if not isinstance(seo.get("target_keyword"), str) or not seo.get("target_keyword", "").strip():
        _add(errors, "seo_strategy.target_keyword", "must be a non-empty string")

    if seo.get("search_intent") not in VALID_SEARCH_INTENTS:
        _add(errors, "seo_strategy.search_intent", f"must be one of {sorted(VALID_SEARCH_INTENTS)}")

    secondary_intents = seo.get("secondary_intents")
    if secondary_intents is not None:
        if not isinstance(secondary_intents, list):
            _add(errors, "seo_strategy.secondary_intents", "must be an array when present")
        else:
            for idx, item in enumerate(secondary_intents):
                if item not in VALID_SEARCH_INTENTS:
                    _add(errors, f"seo_strategy.secondary_intents[{idx}]", f"must be one of {sorted(VALID_SEARCH_INTENTS)}")

    confidence = seo.get("intent_confidence")
    if confidence is not None and (
        not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1
    ):
        _add(errors, "seo_strategy.intent_confidence", "must be a number between 0 and 1")

    secondary_keywords = seo.get("secondary_keywords")
    if secondary_keywords is not None and (
        not isinstance(secondary_keywords, list)
        or not all(isinstance(kw, str) and kw.strip() for kw in secondary_keywords)
    ):
        _add(errors, "seo_strategy.secondary_keywords", "must be an array of non-empty strings when present")

    buyer_stage = seo.get("buyer_stage")
    if buyer_stage is not None and buyer_stage not in VALID_BUYER_STAGES:
        _add(errors, "seo_strategy.buyer_stage", f"must be one of {sorted(VALID_BUYER_STAGES)}")

    page_type = seo.get("page_type")
    if page_type is not None and page_type not in VALID_PAGE_TYPES:
        _add(errors, "seo_strategy.page_type", f"must be one of {sorted(VALID_PAGE_TYPES)}")

    market = seo.get("target_market")
    if not isinstance(market, dict):
        _add(errors, "seo_strategy.target_market", "must be an object")
    elif not isinstance(market.get("locale"), str) or not market.get("locale", "").strip():
        _add(errors, "seo_strategy.target_market.locale", "must be a non-empty string such as en-US")

    _validate_serp_analysis(seo.get("serp_analysis"), seo.get("serp_freshness_policy"), errors, warnings)

    recommendations = seo.get("on_page_recommendations")
    if recommendations is not None:
        _validate_on_page_block(recommendations, "seo_strategy.on_page_recommendations", errors)


def _validate_serp_analysis(serp: Any, freshness_policy: Any, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(serp, dict):
        _add(errors, "seo_strategy.serp_analysis", "must be an object")
        return

    _validate_freshness_policy(freshness_policy, errors)

    checked_at = serp.get("checked_at")
    if not _is_iso_datetime(checked_at):
        _add(errors, "seo_strategy.serp_analysis.checked_at", "must be an ISO 8601 timestamp (SERP freshness is mandatory)")
    else:
        _check_serp_staleness(checked_at, freshness_policy, errors, warnings)

    device = serp.get("device")
    if device is not None and device not in VALID_SERP_DEVICES:
        _add(errors, "seo_strategy.serp_analysis.device", f"must be one of {sorted(VALID_SERP_DEVICES)}")

    competitors = serp.get("competitors")
    if not isinstance(competitors, list):
        _add(errors, "seo_strategy.serp_analysis.competitors", "must be an array")
    elif not competitors:
        _add(errors, "seo_strategy.serp_analysis.competitors", "must contain at least one competitor (SERP-grounded)")
    else:
        for idx, competitor in enumerate(competitors):
            loc = f"seo_strategy.serp_analysis.competitors[{idx}]"
            if not isinstance(competitor, dict):
                _add(errors, loc, "must be an object")
                continue
            rank = competitor.get("rank")
            if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
                _add(errors, f"{loc}.rank", "must be an integer >= 1")
            if not isinstance(competitor.get("url"), str) or not competitor.get("url", "").strip():
                _add(errors, f"{loc}.url", "must be a non-empty string")


def _validate_freshness_policy(freshness_policy: Any, errors: list[str]) -> None:
    """Validate the freshness policy object itself instead of silently defaulting.

    A malformed policy (e.g. ``max_age_days: 0`` or ``on_stale: "bad"``) would
    otherwise be ignored, weakening the SERP-freshness guarantee.
    """
    if freshness_policy is None:
        return
    if not isinstance(freshness_policy, dict):
        _add(errors, "seo_strategy.serp_freshness_policy", "must be an object when present")
        return
    if "max_age_days" in freshness_policy:
        max_age_days = freshness_policy["max_age_days"]
        if not isinstance(max_age_days, int) or isinstance(max_age_days, bool) or max_age_days < 1:
            _add(errors, "seo_strategy.serp_freshness_policy.max_age_days", "must be an integer >= 1")
    if "on_stale" in freshness_policy and freshness_policy["on_stale"] not in VALID_ON_STALE:
        _add(errors, "seo_strategy.serp_freshness_policy.on_stale", f"must be one of {sorted(VALID_ON_STALE)}")


def _check_serp_staleness(checked_at: str, freshness_policy: Any, errors: list[str], warnings: list[str]) -> None:
    checked = _parse_iso_datetime(checked_at)
    if checked is None:
        return
    if checked.tzinfo is None:
        checked = checked.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    # A SERP that claims to have been checked in the future is invalid, not fresh.
    if checked > now:
        _add(errors, "seo_strategy.serp_analysis.checked_at", "must not be in the future")
        return

    max_age_days = DEFAULT_SERP_MAX_AGE_DAYS
    on_stale = "warn"
    if isinstance(freshness_policy, dict):
        candidate_age = freshness_policy.get("max_age_days", DEFAULT_SERP_MAX_AGE_DAYS)
        if isinstance(candidate_age, int) and not isinstance(candidate_age, bool) and candidate_age >= 1:
            max_age_days = candidate_age
        if freshness_policy.get("on_stale") in VALID_ON_STALE:
            on_stale = freshness_policy["on_stale"]

    # Use the full timedelta (not .days, which floors and would tolerate an
    # extra ~24h). Exactly max_age_days old is still considered fresh.
    age = now - checked
    if age > timedelta(days=max_age_days):
        message = f"SERP data is {age.days} days old (max_age_days={max_age_days})"
        if on_stale == "fail":
            _add(errors, "seo_strategy.serp_analysis.checked_at", message)
        else:
            _add(warnings, "seo_strategy.serp_analysis.checked_at", message)


def _validate_on_page_block(block: Any, location: str, errors: list[str]) -> None:
    if not isinstance(block, dict):
        _add(errors, location, "must be an object when present")
        return
    title = block.get("meta_title")
    if title is not None and (not isinstance(title, str) or len(title) > META_TITLE_MAX):
        _add(errors, f"{location}.meta_title", f"must be a string no longer than {META_TITLE_MAX} characters")
    description = block.get("meta_description")
    if description is not None and (not isinstance(description, str) or len(description) > META_DESCRIPTION_MAX):
        _add(errors, f"{location}.meta_description", f"must be a string no longer than {META_DESCRIPTION_MAX} characters")
    slug = block.get("slug")
    if slug is not None and (not isinstance(slug, str) or not SLUG_PATTERN.match(slug)):
        _add(errors, f"{location}.slug", "must be a kebab-case slug (lowercase, digits, single hyphens)")


def _validate_seo_finalization(final: Any, errors: list[str]) -> None:
    if not isinstance(final, dict):
        _add(errors, "seo_finalization", "must be an object when present")
        return
    for field in ["meta_title", "meta_description", "slug", "finalized_at"]:
        if field not in final:
            _add(errors, f"seo_finalization.{field}", "missing required field")
    _validate_on_page_block(final, "seo_finalization", errors)
    if "finalized_at" in final and not _is_iso_datetime(final.get("finalized_at")):
        _add(errors, "seo_finalization.finalized_at", "must be an ISO 8601 timestamp")


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
