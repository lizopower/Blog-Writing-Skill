from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "article.py"


def run_article(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def load_article(root: Path, slug: str) -> dict:
    return json.loads((root / "content" / "articles" / slug / "article.json").read_text(encoding="utf-8"))


def complete_workspace(root: Path, slug: str) -> Path:
    workspace = root / "content" / "articles" / slug
    (workspace / "brief.md").write_text(
        "# Demo\n\n"
        "## Business Goal\n\nGrow qualified leads.\n\n"
        "## Target Audience\n\nB2B marketers.\n\n"
        "## Recommended Angle\n\nShow the buying criteria.\n",
        encoding="utf-8",
    )
    (workspace / "sources.jsonl").write_text('{"url":"https://example.com"}\n', encoding="utf-8")
    (workspace / "context_pack.json").write_text(
        json.dumps(
            {
                "version": "2.3.0",
                "topic": "demo",
                "audience": ["marketers"],
                "key_claims": [{"claim": "demo"}],
            }
        ),
        encoding="utf-8",
    )
    (workspace / "strategy.md").write_text(
        "# Strategy Pressure Test\n\n## Resolved Decisions\n\nUse a practical angle.\n",
        encoding="utf-8",
    )
    (workspace / "outline.md").write_text("# Outline\n\n1. Intro\n", encoding="utf-8")
    (workspace / "draft.md").write_text("# Draft\n\nBody copy.\n", encoding="utf-8")
    (workspace / "fact_check.md").write_text("# Fact Check\n\nStatus: PASS\n", encoding="utf-8")
    (workspace / "editorial_review.md").write_text(
        "# Editorial Review\n\nApproved.\n\nPublishability: PASS\n",
        encoding="utf-8",
    )
    return workspace


class ArticleCliTests(unittest.TestCase):
    def test_create_injects_track(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root), "--track", "lightweight")

            self.assertEqual(result.returncode, 0, result.stderr)
            article = load_article(root, "demo")
            self.assertEqual(article["track"], "lightweight")
            self.assertEqual(article["waivers"], [])

    def test_create_rejects_unknown_article_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_article(
                "create",
                "Demo Title",
                "--slug",
                "demo",
                "--root",
                str(root),
                "--type",
                "guide",
                "--no-hooks",
            )

            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "content" / "articles" / "demo").exists())

    def test_create_installs_hooks_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stderr)
            settings = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
            events = settings["hooks"]
            self.assertTrue(any(e.get("_managed_by") == "blog-writing-skill" for e in events["SessionStart"]))
            self.assertTrue(any(e.get("_managed_by") == "blog-writing-skill" for e in events["UserPromptSubmit"]))

    def test_create_fails_closed_when_hook_install_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # An invalid host settings.json makes install_hook return non-zero,
            # which must abort create instead of leaving a hook-less workspace.
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text("{bad json", encoding="utf-8")

            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertIn("hook install failed", result.stderr)
            self.assertIn("--no-hooks", result.stderr)
            self.assertFalse((root / "content" / "articles" / "demo").exists())

    def test_create_codex_harness_is_also_gated(self) -> None:
        # The hard gate must not be Claude-only: Codex still needs SessionStart +
        # prelude, so a Codex hook install failure must abort create too.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".codex").mkdir()
            (root / ".codex" / "hooks.json").write_text("{bad json", encoding="utf-8")

            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root), "--harness", "codex")

            self.assertEqual(result.returncode, 1)
            self.assertIn("hook install failed", result.stderr)
            self.assertFalse((root / "content" / "articles" / "demo").exists())

    def test_create_codex_harness_installs_and_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root), "--harness", "codex")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "content" / "articles" / "demo" / "article.json").exists())
            hooks = json.loads((root / ".codex" / "hooks.json").read_text(encoding="utf-8"))
            self.assertTrue(any(e.get("_managed_by") == "blog-writing-skill" for e in hooks["hooks"]["SessionStart"]))

    def test_create_no_hooks_opts_out_of_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            # Even with broken host settings, --no-hooks must still create the workspace.
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text("{bad json", encoding="utf-8")

            result = run_article("create", "Demo Title", "--slug", "demo", "--root", str(root), "--no-hooks")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "content" / "articles" / "demo" / "article.json").exists())

    def test_advance_rejects_illegal_transition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))

            result = run_article("advance", "--to", "drafting", "--slug", "demo", "--root", str(root))

        self.assertEqual(result.returncode, 1)
        self.assertIn("illegal transition", result.stderr)

    def test_advance_with_waive_excuses_missing_artifact(self) -> None:
        # brainstorming -> brief_confirmed is a legal edge; an empty brief.md
        # fails its gate, and a waiver excuses that artifact gap.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))
            (root / "content" / "articles" / "demo" / "brief.md").write_text("# Demo\n", encoding="utf-8")

            result = run_article(
                "advance",
                "--to",
                "brief_confirmed",
                "--slug",
                "demo",
                "--root",
                str(root),
                "--waive",
                "legacy import",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            article = load_article(root, "demo")
            self.assertEqual(article["currentPhase"], "brief_confirmed")
            self.assertEqual(article["waivers"][0]["reason"], "legacy import")
            log_path = root / "content" / "articles" / "demo" / "logs" / "pipeline.log"
            self.assertIn('"phase": "brief_confirmed"', log_path.read_text(encoding="utf-8"))

    def test_advance_waive_cannot_bypass_illegal_transition(self) -> None:
        # A waiver must not skip phases to fabricate a terminal state.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))

            result = run_article(
                "advance",
                "--to",
                "completed",
                "--slug",
                "demo",
                "--root",
                str(root),
                "--waive",
                "force illegal jump",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("illegal transition", result.stderr)
            self.assertEqual(load_article(root, "demo")["currentPhase"], "brainstorming")

    def test_status_migrates_legacy_article_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))
            path = root / "content" / "articles" / "demo" / "article.json"
            legacy = load_article(root, "demo")
            legacy.pop("track")
            legacy.pop("waivers", None)
            path.write_text(json.dumps(legacy, indent=2), encoding="utf-8")

            result = run_article("status", "--slug", "demo", "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("track: full", result.stdout)
            persisted = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("track", persisted)

    def test_full_happy_path_to_completed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))
            complete_workspace(root, "demo")

            for phase in [
                "brief_confirmed",
                "research_planning",
                "context_building",
                "strategy_pressure_test",
                "outlining",
                "drafting",
                "fact_checking",
                "editorial_review",
                "completed",
            ]:
                result = run_article("advance", "--to", phase, "--slug", "demo", "--root", str(root))
                self.assertEqual(result.returncode, 0, f"{phase}: {result.stderr}")

            self.assertEqual(load_article(root, "demo")["currentPhase"], "completed")

    def test_list_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_article("create", "Demo Title", "--slug", "demo", "--root", str(root))

            listing = run_article("list", "--root", str(root))
            self.assertIn("demo", listing.stdout)

            archived = run_article("archive", "--slug", "demo", "--root", str(root))
            self.assertEqual(archived.returncode, 0, archived.stderr)
            self.assertTrue((root / "content" / "articles" / "_archive" / "demo").exists())


if __name__ == "__main__":
    unittest.main()
