from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _statemachine import advance_article, can_transition, migrate  # noqa: E402


def base_article(phase: str = "brainstorming", track: str = "full") -> dict:
    return {
        "id": "demo",
        "title": "Demo",
        "status": phase,
        "currentPhase": phase,
        "nextAction": "next",
        "createdAt": "2026-06-09T00:00:00Z",
        "updatedAt": "2026-06-09T00:00:00Z",
        "track": track,
    }


def write_workspace(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "research").mkdir()
    (root / "article.json").write_text(json.dumps(base_article()), encoding="utf-8")
    (root / "brief.md").write_text(
        "# Demo\n\n"
        "## Business Goal\n\nGrow qualified leads.\n\n"
        "## Target Audience\n\nB2B marketers.\n\n"
        "## Recommended Angle\n\nShow the buying criteria.\n",
        encoding="utf-8",
    )
    (root / "sources.jsonl").write_text('{"url":"https://example.com"}\n', encoding="utf-8")
    (root / "context_pack.json").write_text(
        json.dumps(
            {
                "version": "2.2.0",
                "topic": "demo",
                "audience": ["marketers"],
                "key_claims": [{"claim": "demo"}],
            }
        ),
        encoding="utf-8",
    )
    (root / "strategy.md").write_text(
        "# Strategy Pressure Test\n\n## Resolved Decisions\n\nUse a practical angle.\n",
        encoding="utf-8",
    )
    (root / "outline.md").write_text("# Outline\n\n1. Intro\n", encoding="utf-8")
    (root / "draft.md").write_text("# Draft\n\nBody copy.\n", encoding="utf-8")
    (root / "fact_check.md").write_text("# Fact Check\n\nStatus: PASS\n", encoding="utf-8")
    (root / "editorial_review.md").write_text("# Editorial Review\n\nApproved.\n", encoding="utf-8")
    (root / "finish.md").write_text("# Finish\n", encoding="utf-8")


class StateMachineTests(unittest.TestCase):
    def test_migrate_adds_defaults_without_mutating_input(self) -> None:
        legacy = {"currentPhase": "drafting", "track": "surprise"}

        migrated = migrate(legacy)

        self.assertIsNot(migrated, legacy)
        self.assertEqual(migrated["track"], "full")
        self.assertEqual(migrated["waivers"], [])
        self.assertEqual(migrated["history"], [])
        self.assertIsNone(migrated["series"])
        self.assertNotIn("waivers", legacy)

    def test_transition_table_rejects_illegal_jump(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            article = base_article("brainstorming")

            result = can_transition(article, "drafting", workspace)

        self.assertFalse(result.ok)
        self.assertIn("illegal transition", result.reason)

    def test_full_track_cannot_skip_outlining(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            article = base_article("strategy_pressure_test", track="full")

            result = can_transition(article, "drafting", workspace)

        self.assertFalse(result.ok)
        self.assertIn("full track", result.reason)

    def test_lightweight_track_can_skip_outlining_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            (workspace / "outline.md").write_text("# Outline\n\n", encoding="utf-8")
            article = base_article("strategy_pressure_test", track="lightweight")

            result = can_transition(article, "drafting", workspace)

        self.assertTrue(result.ok)

    def test_completed_requires_fact_check_pass_even_on_lightweight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            (workspace / "fact_check.md").write_text("# Fact Check\n\nStatus: FAIL\n", encoding="utf-8")
            article = base_article("editorial_review", track="lightweight")

            result = can_transition(article, "completed", workspace)

        self.assertFalse(result.ok)
        self.assertIn("fact_check.md must record PASS", result.reason)

    def test_waive_excuses_missing_artifact_on_a_legal_transition(self) -> None:
        # brainstorming -> brief_confirmed is a legal edge whose gate requires a
        # populated brief.md. An empty brief.md fails the gate; a waiver excuses
        # that artifact gap and advances, recording the waiver.
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            (workspace / "brief.md").write_text("# Demo\n", encoding="utf-8")
            article = base_article("brainstorming")

            updated, result = advance_article(
                article,
                "brief_confirmed",
                workspace,
                waive_reason="manual migration",
                now="2026-06-09T01:00:00Z",
            )

        self.assertTrue(result.ok)
        self.assertEqual(updated["currentPhase"], "brief_confirmed")
        self.assertEqual(
            updated["waivers"],
            [
                {
                    "from": "brainstorming",
                    "to": "brief_confirmed",
                    "reason": "manual migration",
                    "at": "2026-06-09T01:00:00Z",
                }
            ],
        )
        self.assertEqual(
            updated["history"],
            [{"from": "brainstorming", "to": "brief_confirmed", "at": "2026-06-09T01:00:00Z"}],
        )

    def test_waive_cannot_bypass_illegal_transition(self) -> None:
        # A waiver must not let an article skip phases and fabricate a terminal
        # state. brainstorming -> completed is an illegal edge; even with a
        # waive reason it must be rejected and leave the article untouched.
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            write_workspace(workspace)
            article = base_article("brainstorming")

            updated, result = advance_article(
                article,
                "completed",
                workspace,
                waive_reason="force illegal jump",
                now="2026-06-09T01:00:00Z",
            )

        self.assertFalse(result.ok)
        self.assertIn("illegal transition", result.reason)
        self.assertEqual(updated["currentPhase"], "brainstorming")
        self.assertEqual(updated.get("waivers", []), [])
        self.assertEqual(updated.get("history", []), [])


if __name__ == "__main__":
    unittest.main()
