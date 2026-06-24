#!/usr/bin/env python3
"""Tests for extract_genre_conventions.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "extract_genre_conventions.py"


class ExtractGenreConventionsTests(unittest.TestCase):
    def test_extract_from_reference_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            corpus = root / "content" / "reference" / "demo-topic" / "blog"
            corpus.mkdir(parents=True)
            for index in range(3):
                (corpus / f"sample-{index}.md").write_text(
                    f"# Sample {index}\n\n## Problem\n\nData {index}.\n\n## Solution\n\nFix.\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nTL;DR: ok\n\nContact us.\n",
                    encoding="utf-8",
                )
            out = root / "out.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--topic",
                    "demo-topic",
                    "--type",
                    "blog",
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["sample_count"], 3)
            self.assertGreaterEqual(len(payload["conventions"]), 1)


if __name__ == "__main__":
    unittest.main()
