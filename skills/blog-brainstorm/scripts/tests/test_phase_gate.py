from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from phase_gate import deny_reason  # noqa: E402
from _runtimeinstaller import install_runtime  # noqa: E402


def make_workspace(root: Path, slug: str, phase: str) -> Path:
    workspace = root / "content" / "articles" / slug
    workspace.mkdir(parents=True)
    (workspace / "article.json").write_text(
        json.dumps({"currentPhase": phase, "track": "full", "updatedAt": "2026-06-10T00:00:00Z"}),
        encoding="utf-8",
    )
    return workspace


class DenyReasonTests(unittest.TestCase):
    def test_denies_draft_write_before_drafting_phase(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = make_workspace(root, "demo", "context_building")

            reason = deny_reason(root, "Write", {"file_path": str(workspace / "draft.md")})

        self.assertIsNotNone(reason)
        self.assertIn("drafting", reason)
        self.assertIn("context_building", reason)
        self.assertIn("article.py", reason)

    def test_allows_draft_write_in_drafting_and_later_phases(self) -> None:
        for phase in ["drafting", "fact_checking", "editorial_review", "completed"]:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                workspace = make_workspace(root, "demo", phase)

                reason = deny_reason(root, "Edit", {"file_path": str(workspace / "draft.md")})

            self.assertIsNone(reason, f"phase {phase} should allow draft.md")

    def test_denies_outline_and_fact_check_before_their_phases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = make_workspace(root, "demo", "research_planning")

            outline = deny_reason(root, "Write", {"file_path": str(workspace / "outline.md")})
            fact_check = deny_reason(root, "Write", {"file_path": str(workspace / "fact_check.md")})

        self.assertIn("outlining", outline)
        self.assertIn("fact_checking", fact_check)

    def test_allows_ungated_workspace_files_and_other_tools(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = make_workspace(root, "demo", "brainstorming")

            brief = deny_reason(root, "Write", {"file_path": str(workspace / "brief.md")})
            sources = deny_reason(root, "Edit", {"file_path": str(workspace / "sources.jsonl")})
            read_tool = deny_reason(root, "Read", {"file_path": str(workspace / "draft.md")})

        self.assertIsNone(brief)
        self.assertIsNone(sources)
        self.assertIsNone(read_tool)

    def test_allows_paths_outside_workspaces_and_archives(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_workspace(root, "demo", "brainstorming")
            archived = root / "content" / "articles" / "_archive" / "old" / "draft.md"
            archived.parent.mkdir(parents=True)

            outside = deny_reason(root, "Write", {"file_path": str(root / "draft.md")})
            archive = deny_reason(root, "Write", {"file_path": str(archived)})
            no_path = deny_reason(root, "Write", {"content": "x"})

        self.assertIsNone(outside)
        self.assertIsNone(archive)
        self.assertIsNone(no_path)

    def test_allows_workspace_without_article_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "content" / "articles" / "loose"
            workspace.mkdir(parents=True)

            reason = deny_reason(root, "Write", {"file_path": str(workspace / "draft.md")})

        self.assertIsNone(reason)

    def test_denies_when_article_json_is_corrupt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "content" / "articles" / "demo"
            workspace.mkdir(parents=True)
            (workspace / "article.json").write_text("{bad json", encoding="utf-8")

            reason = deny_reason(root, "Write", {"file_path": str(workspace / "draft.md")})

        self.assertIsNotNone(reason)
        self.assertIn("unreadable", reason)


class PhaseGateCliTests(unittest.TestCase):
    def run_gate(self, root: Path, payload: dict) -> subprocess.CompletedProcess[str]:
        script = root / ".trellis-writing" / "runtime" / "scripts" / "phase_gate.py"
        return subprocess.run(
            [sys.executable, str(script)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_runtime_cli_emits_deny_envelope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = make_workspace(root, "demo", "context_building")
            install_runtime(root)

            result = self.run_gate(
                root,
                {"tool_name": "Write", "tool_input": {"file_path": str(workspace / "draft.md")}},
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(result.stdout)
        self.assertEqual(envelope["hookSpecificOutput"]["hookEventName"], "PreToolUse")
        self.assertEqual(envelope["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("drafting", envelope["hookSpecificOutput"]["permissionDecisionReason"])

    def test_runtime_cli_stays_silent_on_allow_and_bad_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = make_workspace(root, "demo", "drafting")
            install_runtime(root)

            allowed = self.run_gate(
                root,
                {"tool_name": "Write", "tool_input": {"file_path": str(workspace / "draft.md")}},
            )
            script = root / ".trellis-writing" / "runtime" / "scripts" / "phase_gate.py"
            garbage = subprocess.run(
                [sys.executable, str(script)],
                input="not json",
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(allowed.stdout, "")
        self.assertEqual(garbage.returncode, 0, garbage.stderr)
        self.assertEqual(garbage.stdout, "")


if __name__ == "__main__":
    unittest.main()
