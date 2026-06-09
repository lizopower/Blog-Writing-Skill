from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "resume_context.py"
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import resume_context  # noqa: E402


def run_resume(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def write_article(root: Path, slug: str, *, phase: str, track: str, updated_at: str) -> Path:
    workspace = root / "content" / "articles" / slug
    workspace.mkdir(parents=True)
    (workspace / "article.json").write_text(
        json.dumps(
            {
                "id": slug,
                "title": slug.replace("-", " ").title(),
                "status": phase,
                "currentPhase": phase,
                "nextAction": "next",
                "track": track,
                "updatedAt": updated_at,
                "createdAt": "2026-06-09T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    (workspace / "brief.md").write_text(
        "# Brief\n\n## Business Goal\n\nGrow.\n\n## Target Audience\n\nEngineers.\n\n## Recommended Angle\n\nPractical.\n",
        encoding="utf-8",
    )
    (workspace / "sources.jsonl").write_text('{"url":"https://example.com"}\n', encoding="utf-8")
    (workspace / "context_pack.json").write_text(
        json.dumps({"version": "2.2.0", "topic": "demo", "audience": ["engineers"], "key_claims": [{"claim": "x"}]}),
        encoding="utf-8",
    )
    (workspace / "strategy.md").write_text("# Strategy\n\n## Resolved Decisions\n\nUse this angle.\n", encoding="utf-8")
    (workspace / "outline.md").write_text("# Outline\n\n", encoding="utf-8")
    (workspace / "draft.md").write_text("# Draft\n\nBody.\n", encoding="utf-8")
    (workspace / "fact_check.md").write_text("# Fact Check\n\nStatus: PASS\n", encoding="utf-8")
    (workspace / "editorial_review.md").write_text("# Editorial Review\n\nApproved.\n", encoding="utf-8")
    return workspace


def write_spec(root: Path) -> None:
    specs = root / "content" / "specs"
    specs.mkdir(parents=True)
    (specs / "numeric-formatting.md").write_text(
        "---\n"
        "id: numeric-formatting\n"
        "title: Numeric Formatting\n"
        "scope: project\n"
        "createdAt: 2026-06-09T00:00:00Z\n"
        "---\n\nUse SI units.\n",
        encoding="utf-8",
    )


class ResumeContextTests(unittest.TestCase):
    def test_no_articles_prints_quiet_hint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_resume("--root", directory)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "No article workspace found.")

    def test_prints_phase_track_next_blockers_and_specs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "demo", phase="strategy_pressure_test", track="full", updated_at="2026-06-09T02:00:00Z")
            write_spec(root)

            result = run_resume("--root", str(root), "--slug", "demo")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current Target: demo", result.stdout)
        self.assertIn("Phase: strategy_pressure_test", result.stdout)
        self.assertIn("Track: full", result.stdout)
        self.assertIn("outlining: ok", result.stdout)
        self.assertIn("drafting: blocked: full track must pass through outlining before drafting", result.stdout)
        self.assertIn("Numeric Formatting [project]", result.stdout)

    def test_latest_updated_article_is_current_and_others_are_listed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "older", phase="drafting", track="full", updated_at="2026-06-09T01:00:00Z")
            write_article(root, "newer", phase="context_building", track="lightweight", updated_at="2026-06-09T03:00:00Z")

            result = run_resume("--root", str(root))

        self.assertEqual(result.returncode, 0, result.stderr)
        first_line = result.stdout.splitlines()[0]
        self.assertEqual(first_line, "Current Target: newer")
        self.assertIn("Other in-progress articles:", result.stdout)
        self.assertIn("older", result.stdout)
        self.assertIn("Switch with: resume_context.py --slug older", result.stdout)

    def test_completed_article_is_not_listed_as_other_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "active", phase="drafting", track="full", updated_at="2026-06-09T03:00:00Z")
            write_article(root, "done", phase="completed", track="full", updated_at="2026-06-09T04:00:00Z")

            result = run_resume("--root", str(root))

        self.assertIn("Current Target: active", result.stdout)
        self.assertNotIn("done", result.stdout)

    def test_missing_child_capabilities_degrade_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "demo", phase="drafting", track="full", updated_at="2026-06-09T03:00:00Z")
            original_statemachine = resume_context.load_statemachine
            original_specstore = resume_context.load_specstore
            try:
                resume_context.load_statemachine = lambda: (None, "Lifecycle state machine unavailable.")
                resume_context.load_specstore = lambda: (None, "Project specs unavailable.")

                output = resume_context.render_context(root, "demo")
            finally:
                resume_context.load_statemachine = original_statemachine
                resume_context.load_specstore = original_specstore

        self.assertIn("Current Target: demo", output)
        self.assertIn("Lifecycle state machine unavailable.", output)
        self.assertIn("Project specs unavailable.", output)


if __name__ == "__main__":
    unittest.main()
