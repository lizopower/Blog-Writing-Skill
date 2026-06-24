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
        draft = _sample_draft().replace("Demo", "Revolutionary Demo")
        result = check_draft(draft, article_type="blog")
        self.assertTrue(any("marketing" in warn for warn in result.warns))

    def test_case_study_requires_more_data(self) -> None:
        minimal = "# Title\n\n## Challenge\n\nOne line only.\n\n## Solution\n\nAnother.\n"
        result = check_draft(minimal, article_type="case-study")
        self.assertFalse(result.ok)

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
                [sys.executable, str(script), str(root), "--workspace"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
