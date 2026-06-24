#!/usr/bin/env python3
"""Tests for check_draft.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from check_draft import check_draft  # noqa: E402


def _sample_draft() -> str:
    return """# Demo Article

## Problem

Line scanners miss 12% of defects at 2 m/s (Source: internal bench, 2025).

## Approach

Use dual-camera fusion with 3 ms latency budget.

## Results

False rejects dropped 18% while throughput held at 95 units/min.

## Next Steps

Contact the team to pilot on your line.
"""


class CheckDraftTests(unittest.TestCase):
    def test_clean_draft_passes(self) -> None:
        result = check_draft(_sample_draft(), article_type="blog")
        self.assertTrue(result.ok)
        self.assertEqual(len(result.issues), 0)

    def test_empty_draft_fails(self) -> None:
        result = check_draft("   \n")
        self.assertFalse(result.ok)
        self.assertTrue(any("empty" in issue for issue in result.issues))

    def test_placeholder_is_issue(self) -> None:
        draft = _sample_draft() + "\n\nStill [TODO] here.\n"
        result = check_draft(draft, article_type="blog")
        self.assertFalse(result.ok)
        self.assertTrue(any("placeholder" in issue for issue in result.issues))

    def test_marketing_word_warns(self) -> None:
        draft = _sample_draft().replace(
            "Use dual-camera fusion",
            "This revolutionary dual-camera fusion",
        )
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("marketing" in warn for warn in result.warns))

    def test_hedge_word_warns(self) -> None:
        draft = _sample_draft().replace("Use dual-camera", "Use a really dual-camera")
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("hedge" in warn for warn in result.warns))

    def test_contrast_reframe_warns(self) -> None:
        draft = _sample_draft() + "\n\nIt's not about speed, it's about accuracy.\n"
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("AI-pattern" in warn for warn in result.warns))

    def test_em_dash_density_issue(self) -> None:
        dashes = " — word" * 80
        draft = _sample_draft() + dashes
        result = check_draft(draft, article_type="blog")
        combined = result.warns + result.issues
        self.assertTrue(any("em-dash" in item for item in combined))

    def test_unsourced_number_warns(self) -> None:
        draft = _sample_draft().replace(
            "(Source: internal bench, 2025).",
            ".",
        )
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("sources" in warn for warn in result.warns))

    def test_unsourced_number_ignores_code_fence(self) -> None:
        draft = _sample_draft() + "\n\n```python\nratio = 42%\n```\n"
        result = check_draft(draft, article_type="blog")
        self.assertFalse(any("42%" in warn for warn in result.warns))

    def test_robust_regression_allowlisted(self) -> None:
        draft = _sample_draft() + "\n\nWe used robust regression for the baseline.\n"
        result = check_draft(draft, article_type="blog")
        self.assertFalse(any("robust" in warn for warn in result.warns))

    def test_robust_solution_not_allowlisted(self) -> None:
        draft = _sample_draft() + "\n\nThis is a robust solution for everyone.\n"
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("robust" in warn for warn in result.warns))

    def test_case_study_requires_more_data(self) -> None:
        minimal = "# Title\n\n## Challenge\n\nOne line only.\n\n## Solution\n\nAnother.\n"
        result = check_draft(minimal, article_type="case-study")
        self.assertFalse(result.ok)

    def test_write_report_markdown(self) -> None:
        result = check_draft(_sample_draft(), article_type="blog")
        md = result.render_markdown(label="draft.md")
        self.assertIn("Draft Lint Report", md)
        self.assertIn("PASS", md)

    def test_cli_workspace_mode(self) -> None:
        script = SCRIPTS_DIR / "check_draft.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "draft.md").write_text(_sample_draft(), encoding="utf-8")
            (root / "article.json").write_text(
                json.dumps({"articleType": "blog"}),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [sys.executable, str(script), str(root), "--workspace", "--write-report"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("PASS", proc.stdout)
            self.assertTrue((root / "draft_lint.md").exists())


if __name__ == "__main__":
    unittest.main()
