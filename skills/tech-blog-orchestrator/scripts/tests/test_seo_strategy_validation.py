"""Tests for the SEO strategy layer validation (schema 2.3.0).

Covers the positive path plus the negative cases mandated by the task plan:
missing required fields, invalid enums/slug, stale SERP data, and backward
compatibility for packs without a seo_strategy block.
"""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_context_pack import validate_context_pack  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _days_ago_iso(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).replace(microsecond=0).isoformat()


def base_pack() -> dict:
    """A minimal context pack that is valid under the non-SEO flow."""
    return {
        "version": "2.3.0",
        "generated_at": _now_iso(),
        "topic": "Industrial low-temperature battery selection",
        "audience": ["B2B procurement engineers"],
        "industry_context": {
            "industry": "battery manufacturing",
            "market_segment": "industrial energy storage",
            "core_advantage": "low-temperature discharge performance",
        },
        "key_claims": [
            {
                "claim": "IFR18650 cells retain 80% capacity at minus 20 Celsius.",
                "source": {"type": "research", "reference": "lab-report-2026:Page 4"},
                "confidence": "high",
            }
        ],
        "extracted_tables": [],
        "glossary": [{"term": "IFR18650", "definition": "A lithium iron phosphate cylindrical cell."}],
        "risk_notes": [],
        "research_summary": {
            "sources_count": 1,
            "last_updated": _now_iso(),
            "key_findings": ["Low-temperature retention is the key differentiator."],
        },
        "file_summary": {
            "files_processed": ["lab-report-2026.pdf"],
            "total_pages": 12,
            "extraction_notes": [],
        },
    }


def valid_seo_strategy() -> dict:
    return {
        "target_keyword": "low temperature lithium battery",
        "secondary_keywords": ["cold weather battery", "subzero lithium cell"],
        "search_intent": "commercial",
        "secondary_intents": ["informational"],
        "intent_confidence": 0.8,
        "target_market": {"country": "US", "language": "en", "locale": "en-US"},
        "serp_analysis": {
            "checked_at": _now_iso(),
            "device": "desktop",
            "competitors": [
                {"rank": 1, "url": "https://example.com/cold-battery", "title": "Cold Battery Guide"}
            ],
            "paa_questions": ["What battery works in cold weather?"],
            "content_gaps": ["No competitor covers discharge curves at minus 30."],
        },
        "serp_freshness_policy": {"max_age_days": 90, "on_stale": "fail"},
        "on_page_recommendations": {
            "meta_title": "Low Temperature Lithium Battery: Cold Weather Guide",
            "meta_description": "How industrial lithium batteries perform in subzero conditions and how to choose one.",
            "slug": "low-temperature-lithium-battery",
        },
    }


class TestSeoStrategyPositive(unittest.TestCase):
    def test_valid_seo_pack_passes(self):
        pack = base_pack()
        pack["seo_strategy"] = valid_seo_strategy()
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertTrue(is_valid, msg=f"unexpected errors: {errors}")

    def test_pack_without_seo_strategy_still_valid(self):
        # Backward compatibility: the SEO layer is optional.
        is_valid, errors, _ = validate_context_pack(base_pack())
        self.assertTrue(is_valid, msg=f"unexpected errors: {errors}")


class TestSeoStrategyNegative(unittest.TestCase):
    def _pack_with(self, mutator) -> dict:
        pack = base_pack()
        seo = valid_seo_strategy()
        mutator(seo)
        pack["seo_strategy"] = seo
        return pack

    def _assert_error_contains(self, pack: dict, needle: str):
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any(needle in e for e in errors), msg=f"expected '{needle}' in {errors}")

    def test_missing_target_keyword(self):
        self._assert_error_contains(self._pack_with(lambda s: s.pop("target_keyword")), "seo_strategy.target_keyword")

    def test_missing_search_intent(self):
        self._assert_error_contains(self._pack_with(lambda s: s.pop("search_intent")), "seo_strategy.search_intent")

    def test_missing_target_market_locale(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["target_market"].pop("locale")),
            "seo_strategy.target_market.locale",
        )

    def test_missing_serp_checked_at(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["serp_analysis"].pop("checked_at")),
            "seo_strategy.serp_analysis.checked_at",
        )

    def test_competitor_missing_rank_and_url(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["serp_analysis"].__setitem__("competitors", [{"title": "no rank or url"}])),
            "competitors[0]",
        )

    def test_invalid_slug(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["on_page_recommendations"].__setitem__("slug", "Not A Slug!")),
            "on_page_recommendations.slug",
        )

    def test_invalid_search_intent_enum(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s.__setitem__("search_intent", "buy-now")),
            "seo_strategy.search_intent",
        )

    def test_invalid_device_enum(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["serp_analysis"].__setitem__("device", "watch")),
            "seo_strategy.serp_analysis.device",
        )

    def test_meta_title_too_long(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["on_page_recommendations"].__setitem__("meta_title", "x" * 61)),
            "on_page_recommendations.meta_title",
        )

    def test_intent_confidence_out_of_range(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s.__setitem__("intent_confidence", 1.5)),
            "seo_strategy.intent_confidence",
        )

    def test_intent_confidence_bool_rejected(self):
        # A bool is a subclass of int; 0 <= True <= 1 is True, so it must be
        # rejected explicitly rather than silently accepted as a number.
        self._assert_error_contains(
            self._pack_with(lambda s: s.__setitem__("intent_confidence", True)),
            "seo_strategy.intent_confidence",
        )

    def test_seo_strategy_not_a_dict(self):
        pack = base_pack()
        pack["seo_strategy"] = "not an object"
        self._assert_error_contains(pack, "seo_strategy")

    def test_serp_analysis_missing(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s.pop("serp_analysis")),
            "seo_strategy.serp_analysis",
        )

    def test_competitors_not_a_list(self):
        self._assert_error_contains(
            self._pack_with(lambda s: s["serp_analysis"].__setitem__("competitors", {"rank": 1})),
            "seo_strategy.serp_analysis.competitors",
        )


class TestSerpStaleness(unittest.TestCase):
    def test_stale_serp_fails_when_policy_fail(self):
        pack = base_pack()
        seo = valid_seo_strategy()
        seo["serp_analysis"]["checked_at"] = _days_ago_iso(200)
        seo["serp_freshness_policy"] = {"max_age_days": 90, "on_stale": "fail"}
        pack["seo_strategy"] = seo
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("days old" in e for e in errors), msg=errors)

    def test_stale_serp_warns_when_policy_warn(self):
        pack = base_pack()
        seo = valid_seo_strategy()
        seo["serp_analysis"]["checked_at"] = _days_ago_iso(200)
        seo["serp_freshness_policy"] = {"max_age_days": 90, "on_stale": "warn"}
        pack["seo_strategy"] = seo
        is_valid, errors, warnings = validate_context_pack(pack)
        self.assertTrue(is_valid, msg=f"unexpected errors: {errors}")
        self.assertTrue(any("days old" in w for w in warnings), msg=warnings)

    def test_fresh_serp_no_staleness_warning(self):
        pack = base_pack()
        pack["seo_strategy"] = valid_seo_strategy()
        _, _, warnings = validate_context_pack(pack)
        self.assertFalse(any("days old" in w for w in warnings), msg=warnings)

    def _pack_checked_at(self, delta: timedelta, policy: dict) -> dict:
        pack = base_pack()
        seo = valid_seo_strategy()
        checked = (datetime.now(timezone.utc) - delta).replace(microsecond=0).isoformat()
        seo["serp_analysis"]["checked_at"] = checked
        seo["serp_freshness_policy"] = policy
        pack["seo_strategy"] = seo
        return pack

    def test_partial_day_over_max_is_stale(self):
        # Floor bug regression: 90 days + 12h must NOT be tolerated as fresh.
        pack = self._pack_checked_at(timedelta(days=90, hours=12), {"max_age_days": 90, "on_stale": "fail"})
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("days old" in e for e in errors), msg=errors)

    def test_just_under_max_is_fresh(self):
        # 89 days 23h is within the 90-day window.
        pack = self._pack_checked_at(timedelta(days=89, hours=23), {"max_age_days": 90, "on_stale": "fail"})
        is_valid, errors, warnings = validate_context_pack(pack)
        self.assertTrue(is_valid, msg=f"unexpected errors: {errors}")
        self.assertFalse(any("days old" in w for w in warnings), msg=warnings)

    def test_future_checked_at_rejected(self):
        pack = self._pack_checked_at(timedelta(days=-2), {"max_age_days": 90, "on_stale": "warn"})
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("future" in e for e in errors), msg=errors)

    def test_invalid_freshness_policy_max_age_zero(self):
        pack = self._pack_checked_at(timedelta(days=1), {"max_age_days": 0, "on_stale": "warn"})
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("serp_freshness_policy.max_age_days" in e for e in errors), msg=errors)

    def test_invalid_freshness_policy_on_stale_enum(self):
        pack = self._pack_checked_at(timedelta(days=1), {"max_age_days": 90, "on_stale": "explode"})
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("serp_freshness_policy.on_stale" in e for e in errors), msg=errors)


class TestSeoStrategyFieldValidation(unittest.TestCase):
    def _seo_error(self, mutator, needle):
        pack = base_pack()
        seo = valid_seo_strategy()
        mutator(seo)
        pack["seo_strategy"] = seo
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any(needle in e for e in errors), msg=f"expected '{needle}' in {errors}")

    def test_empty_competitors_rejected(self):
        self._seo_error(lambda s: s["serp_analysis"].__setitem__("competitors", []),
                        "seo_strategy.serp_analysis.competitors")

    def test_invalid_buyer_stage(self):
        self._seo_error(lambda s: s.__setitem__("buyer_stage", "shopping"), "seo_strategy.buyer_stage")

    def test_invalid_page_type(self):
        self._seo_error(lambda s: s.__setitem__("page_type", "blogpost"), "seo_strategy.page_type")

    def test_secondary_keywords_not_list_of_strings(self):
        self._seo_error(lambda s: s.__setitem__("secondary_keywords", ["ok", 123]),
                        "seo_strategy.secondary_keywords")


class TestSeoFinalization(unittest.TestCase):
    def test_valid_finalization_passes(self):
        pack = base_pack()
        pack["seo_strategy"] = valid_seo_strategy()
        pack["seo_finalization"] = {
            "meta_title": "Low Temperature Lithium Battery Guide",
            "meta_description": "Choosing industrial lithium batteries for subzero operating conditions.",
            "slug": "low-temperature-lithium-battery",
            "finalized_at": _now_iso(),
            "overrides": ["adopted strategist meta_title verbatim"],
        }
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertTrue(is_valid, msg=f"unexpected errors: {errors}")

    def test_finalization_missing_required_field(self):
        pack = base_pack()
        pack["seo_finalization"] = {
            "meta_title": "Title only",
            "meta_description": "desc",
            "slug": "title-only",
        }
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("seo_finalization.finalized_at" in e for e in errors), msg=errors)

    def test_finalization_meta_title_too_long(self):
        pack = base_pack()
        pack["seo_finalization"] = {
            "meta_title": "x" * 61,
            "meta_description": "A valid length description for the finalized on-page metadata block.",
            "slug": "valid-slug",
            "finalized_at": _now_iso(),
        }
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("seo_finalization.meta_title" in e for e in errors), msg=errors)

    def test_finalization_invalid_slug(self):
        pack = base_pack()
        pack["seo_finalization"] = {
            "meta_title": "Valid Title",
            "meta_description": "A valid length description for the finalized on-page metadata block.",
            "slug": "/leading-slash",
            "finalized_at": _now_iso(),
        }
        is_valid, errors, _ = validate_context_pack(pack)
        self.assertFalse(is_valid)
        self.assertTrue(any("seo_finalization.slug" in e for e in errors), msg=errors)


if __name__ == "__main__":
    unittest.main()
