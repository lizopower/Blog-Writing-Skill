from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _specstore import merge_index_entries, parse_spec, render_index, render_spec, slugify  # noqa: E402


class SpecStoreTests(unittest.TestCase):
    def test_slugify_handles_latin_and_fallback(self) -> None:
        self.assertEqual(slugify("Numeric Formatting Rules"), "numeric-formatting-rules")
        self.assertEqual(slugify("数值与单位格式规范"), "spec")

    def test_render_and_parse_spec_round_trip(self) -> None:
        markdown = render_spec(
            spec_id="numeric-formatting",
            title="Numeric Formatting",
            scope="project",
            created_at="2026-06-09T00:00:00Z",
            body="Use SI units.",
        )

        parsed = parse_spec(markdown)

        self.assertEqual(parsed.front_matter["id"], "numeric-formatting")
        self.assertEqual(parsed.front_matter["title"], "Numeric Formatting")
        self.assertEqual(parsed.body, "Use SI units.\n")

    def test_merge_index_entries_dedupes_by_slug_and_preserves_order(self) -> None:
        entries = merge_index_entries(
            [
                ("alpha", "Alpha", "First"),
                ("beta", "Beta", "Second"),
            ],
            [("alpha", "Alpha Updated", "Updated"), ("gamma", "Gamma", "")],
        )

        self.assertEqual(
            entries,
            [
                ("alpha", "Alpha Updated", "Updated"),
                ("beta", "Beta", "Second"),
                ("gamma", "Gamma", ""),
            ],
        )

    def test_render_index_contains_relative_links(self) -> None:
        rendered = render_index([("numeric-formatting", "Numeric Formatting", "Use SI units.")])

        self.assertIn("# Project Writing Specs", rendered)
        self.assertIn("[Numeric Formatting](numeric-formatting.md)", rendered)
        self.assertIn("Use SI units.", rendered)


if __name__ == "__main__":
    unittest.main()
