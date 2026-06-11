from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "inject_workflow_state.py"


def write_article(root: Path, slug: str, *, phase: str, track: str, updated_at: str) -> Path:
    workspace = root / "content" / "articles" / slug
    workspace.mkdir(parents=True)
    (workspace / "article.json").write_text(
        json.dumps(
            {
                "id": slug,
                "currentPhase": phase,
                "track": track,
                "updatedAt": updated_at,
                "createdAt": "2026-06-09T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    return workspace


def run_inject(cwd: Path, stdin: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(cwd),
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


class InjectWorkflowStateTests(unittest.TestCase):
    def test_active_article_emits_user_prompt_submit_breadcrumb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "demo", phase="drafting", track="full", updated_at="2026-06-09T03:00:00Z")

            result = run_inject(root, stdin='{"prompt": "hi"}')

        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        context = envelope["hookSpecificOutput"]["additionalContext"]
        self.assertIn("<workflow-state>", context)
        self.assertIn("Current article: demo", context)
        self.assertIn("Phase: drafting", context)

    def test_no_article_workspace_stays_silent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "content" / "articles").mkdir(parents=True)

            result = run_inject(root, stdin='{"prompt": "hi"}')

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_completed_only_article_stays_silent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "done", phase="completed", track="full", updated_at="2026-06-09T03:00:00Z")

            result = run_inject(root, stdin='{"prompt": "hi"}')

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_subagent_payload_stays_silent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_article(root, "demo", phase="drafting", track="full", updated_at="2026-06-09T03:00:00Z")

            result = run_inject(root, stdin='{"isSubagent": true}')

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
