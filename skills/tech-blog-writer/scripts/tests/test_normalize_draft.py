#!/usr/bin/env python3
"""Tests for normalize_draft.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "normalize_draft.py"


class NormalizeDraftTests(unittest.TestCase):
    def test_check_only_does_not_modify(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            original = "# Title\n\n|a|b|\n|-|-|\n|1|2|\n"
            draft.write_text(original, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(draft)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(draft.read_text(encoding="utf-8"), original)

    def test_apply_normalizes_tables(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("# Title\n\n|a|b|\n|-|-|\n|1|2|\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(draft), "--apply"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0)
            self.assertIn("| a | b |", draft.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
