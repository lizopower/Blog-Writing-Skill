#!/usr/bin/env python3
"""Tests for audit_near_duplicate.py."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from audit_near_duplicate import audit, load_source_texts  # noqa: E402


class AuditNearDuplicateTests(unittest.TestCase):
    def test_sources_jsonl_relative_path_is_resolved_from_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "content" / "articles" / "demo"
            source = root / "content" / "articles" / "demo" / "research" / "source.md"
            source.parent.mkdir(parents=True)
            source.write_text("This shared source passage should be detected.", encoding="utf-8")
            (workspace / "sources.jsonl").write_text(
                json.dumps({"local_path": "content/articles/demo/research/source.md"}) + "\n",
                encoding="utf-8",
            )

            sources = load_source_texts(workspace, root, include_reference=False)
            findings = audit("Draft repeats: this shared source passage should be detected.", sources)

        self.assertEqual(sources[0][0], "source.md")
        self.assertTrue(findings)
        self.assertEqual(findings[0]["source"], "source.md")


if __name__ == "__main__":
    unittest.main()
