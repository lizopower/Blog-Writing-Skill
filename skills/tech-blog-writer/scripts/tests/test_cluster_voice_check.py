#!/usr/bin/env python3
"""Tests for cluster_voice_check.py (cross-article voice checks)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from cluster_voice_check import build_article, run_cluster_check  # noqa: E402

NO_ALLOW: frozenset[str] = frozenset()


def _art(label: str, body: str, primary: str = ""):
    return build_article(label, body, primary)


def _all_findings(result) -> list[str]:
    return result.passes + result.warns + result.issues


def _has(result, needle: str) -> bool:
    return any(needle in item for item in _all_findings(result))


# --- Distinct, clean articles (should not collide) --------------------------

CLEAN_A = """# Migrating Postgres without downtime

Downtime is a promise you make to customers, and breaking it erodes trust fast.

## The replica swap
We stood up a logical replica, let it catch up over four days, then flipped
traffic inside a single transaction with zero dropped connections. (Source: log)

## What broke anyway
Sequences drifted, and a nightly reconciliation job caught it at 3am.
"""

CLEAN_B = """# A field guide to flaky tests

Every engineer has a story about the test that only fails on a Friday afternoon.

## Reproduce, then record
Flakiness hides in timing. We record thread schedules until the failure appears,
sometimes after two hundred repeated runs on the same machine.

## The usual suspects
Shared fixtures, wall-clock assumptions, and unclosed sockets explain most cases.

## Quarantine that works
Give each quarantined test an owner and a deadline, or the suite quietly rots.
"""


class ClusterVoiceUnitTests(unittest.TestCase):
    def test_clean_cluster_passes(self) -> None:
        result = run_cluster_check([_art("a", CLEAN_A), _art("b", CLEAN_B)], NO_ALLOW)
        self.assertTrue(result.ok, result.issues)
        self.assertEqual(len(result.issues), 0)

    def test_shared_opener_is_issue(self) -> None:
        opener = "The migration was slow and everyone on the team knew it early.\n"
        a = f"# A\n\n{opener}\n## S\n\nAlpha content diverges wildly from here onward indeed.\n"
        b = f"# B\n\n{opener}\n## S\n\nBravo content diverges wildly from there onward instead.\n"
        result = run_cluster_check([_art("a", a), _art("b", b)], NO_ALLOW)
        self.assertFalse(result.ok)
        self.assertTrue(_has(result, "opener"))

    def test_shared_cliche_across_all_is_issue(self) -> None:
        a = "# A\n\nOpeners differ here plainly.\n\nAt the end of the day, latency is the metric.\n"
        b = "# B\n\nDistinct start entirely now.\n\nAt the end of the day, cost is the metric.\n"
        result = run_cluster_check([_art("a", a), _art("b", b)], NO_ALLOW)
        self.assertTrue(_has(result, "shared-cliche"))

    def test_shared_contrast_reframe_is_issue(self) -> None:
        a = "# A\n\nUnique first line alpha.\n\nIt's not about speed, it's about accuracy always.\n"
        b = "# B\n\nUnique first line bravo.\n\nIt's not about volume, it's about accuracy mostly.\n"
        result = run_cluster_check([_art("a", a), _art("b", b)], NO_ALLOW)
        self.assertTrue(_has(result, "contrast-reframe"))

    def test_long_duplicate_run_is_issue(self) -> None:
        shared = "we rebuilt the entire ingestion pipeline from scratch to handle backpressure"
        a = f"# A\n\nAlpha opener stands alone.\n\n{shared} under load.\n"
        b = f"# B\n\nBravo opener stands apart.\n\n{shared} during spikes.\n"
        result = run_cluster_check([_art("a", a), _art("b", b)], NO_ALLOW)
        self.assertFalse(result.ok)
        self.assertTrue(_has(result, "duplicate-line"))

    def test_cadence_sameness_warns(self) -> None:
        a = "# A\n\nOne two three four. Five six seven eight. Nine ten more twelve.\n"
        b = "# B\n\nApple pear plum grape. Lemon lime kiwi fig. Mango guava melon date.\n"
        result = run_cluster_check([_art("a", a), _art("b", b)], NO_ALLOW)
        self.assertTrue(_has(result, "cadence"))

    # Neighbor words on both sides differ, so only the exempt phrase itself overlaps.
    _PHRASE = "acme quantum ledger sync engine"
    _DRAFT_A = f"# A\n\nAlpha opener alone here.\n\nOur {_PHRASE} launched last spring.\n"
    _DRAFT_B = f"# B\n\nBravo opener apart there.\n\nThe {_PHRASE} debuted one winter.\n"

    def test_allow_exempts_shared_phrase(self) -> None:
        without = run_cluster_check([_art("a", self._DRAFT_A), _art("b", self._DRAFT_B)], NO_ALLOW)
        self.assertTrue(_has(without, "cross-phrase"))
        allow = frozenset(self._PHRASE.split())
        withallow = run_cluster_check([_art("a", self._DRAFT_A), _art("b", self._DRAFT_B)], allow)
        self.assertFalse(_has(withallow, "cross-phrase"))

    def test_primary_keyword_auto_exempt(self) -> None:
        arts = [
            _art("a", self._DRAFT_A, primary=self._PHRASE),
            _art("b", self._DRAFT_B, primary=self._PHRASE),
        ]
        result = run_cluster_check(arts, NO_ALLOW)
        self.assertFalse(_has(result, "cross-phrase"))

    def test_report_markdown_renders(self) -> None:
        result = run_cluster_check([_art("a", CLEAN_A), _art("b", CLEAN_B)], NO_ALLOW)
        md = result.render_markdown(labels=["a", "b"])
        self.assertIn("Cluster Voice Report", md)
        self.assertIn("PASS", md)


class ClusterVoiceCliTests(unittest.TestCase):
    SCRIPT = SCRIPTS_DIR / "cluster_voice_check.py"

    def _workspace(self, root: Path, slug: str, body: str) -> Path:
        ws = root / "content" / "articles" / slug
        ws.mkdir(parents=True, exist_ok=True)
        (ws / "draft.md").write_text(body, encoding="utf-8")
        (ws / "article.json").write_text(json.dumps({"primaryKeyword": ""}), encoding="utf-8")
        return ws

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_cli_clean_cluster_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a = self._workspace(root, "a", CLEAN_A)
            b = self._workspace(root, "b", CLEAN_B)
            proc = self._run(str(a), str(b), "--write-report")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("PASS", proc.stdout)
            self.assertTrue((a.parent / "cluster_voice_report.md").exists())

    def test_cli_colliding_cluster_fails(self) -> None:
        collide = (
            "# {t}\n\nIn today's fast-paced digital world, teams struggle to move fast.\n\n"
            "## Why\n\nOur pipeline processes real time event data at massive scale daily.\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a = self._workspace(root, "a", collide.format(t="A"))
            b = self._workspace(root, "b", collide.format(t="B"))
            proc = self._run("--root", str(root), "--slugs", "a,b")
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("FAIL", proc.stdout)

    def test_cli_requires_two_articles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a = self._workspace(root, "a", CLEAN_A)
            proc = self._run(str(a))
            self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
