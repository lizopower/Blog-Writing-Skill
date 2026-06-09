from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
INIT_SCRIPT = SCRIPTS_DIR / "init.py"
INSTALLER_SCRIPT = SCRIPTS_DIR / "install_session_hook.py"


def run_init(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INIT_SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def run_installer(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER_SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class UnifiedInitTests(unittest.TestCase):
    def test_init_creates_project_directories_without_session_hook(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_init("--root", str(root), "--no-session-hook")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "content" / "articles").is_dir())
            self.assertTrue((root / "content" / "specs" / "index.md").is_file())
            self.assertTrue((root / ".trellis-writing" / "runtime" / "scripts" / "session_start.py").is_file())
            self.assertTrue((root / ".trellis-writing" / "runtime" / "scripts" / "resume_context.py").is_file())
            self.assertTrue((root / ".trellis-writing" / ".version").is_file())
            self.assertTrue((root / ".trellis-writing" / ".template-hashes.json").is_file())
            self.assertFalse((root / ".claude" / "settings.json").exists())
            self.assertFalse((root / ".codex" / "hooks.json").exists())
            self.assertIn("Session hook: skipped", result.stdout)

    def test_init_installs_claude_hook_with_yes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_init("--root", str(root), "--harness", "claude", "--yes")
            data = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(data["hooks"]["SessionStart"]), 3)
            self.assertTrue(all("_managed_by" in entry for entry in data["hooks"]["SessionStart"]))
            command = data["hooks"]["SessionStart"][0]["hooks"][0]["command"]
            self.assertIn(".trellis-writing", command)
            self.assertIn("session_start.py", command)
            self.assertNotIn("skills", command)
            self.assertNotIn("resume_context.py --root", command)
            self.assertIn("Installed hooks: claude", result.stdout)
            self.assertIn("First session may ask you to trust", result.stdout)

    def test_project_local_session_start_prints_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article_dir = root / "content" / "articles" / "demo"
            article_dir.mkdir(parents=True)
            (article_dir / "article.json").write_text(
                json.dumps(
                    {
                        "id": "demo",
                        "title": "Demo",
                        "status": "drafting",
                        "currentPhase": "drafting",
                        "track": "full",
                        "updatedAt": "2026-06-09T12:00:00Z",
                        "createdAt": "2026-06-09T00:00:00Z",
                    }
                ),
                encoding="utf-8",
            )

            init_result = run_init("--root", str(root), "--no-session-hook")
            session_start = root / ".trellis-writing" / "runtime" / "scripts" / "session_start.py"
            result = subprocess.run(
                [sys.executable, str(session_start)],
                cwd=str(root),
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(init_result.returncode, 0, init_result.stderr)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current Target: demo", result.stdout)
        self.assertIn("Phase: drafting", result.stdout)

    def test_init_installs_all_harnesses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_init("--root", str(root), "--harness", "all", "--yes")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / ".claude" / "settings.json").exists())
            self.assertTrue((root / ".codex" / "hooks.json").exists())
            self.assertIn("Installed hooks: claude, codex", result.stdout)

    def test_init_is_idempotent_and_preserves_existing_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = root / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text(
                json.dumps(
                    {
                        "env": {"KEEP": "1"},
                        "hooks": {
                            "SessionStart": [
                                {
                                    "matcher": "startup",
                                    "hooks": [{"type": "command", "command": "python existing.py", "timeout": 30}],
                                }
                            ],
                            "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python keep.py"}]}],
                        },
                    }
                ),
                encoding="utf-8",
            )

            first = run_init("--root", str(root), "--harness", "claude", "--yes")
            second = run_init("--root", str(root), "--harness", "claude", "--yes")
            data = json.loads(settings.read_text(encoding="utf-8"))

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(data["env"], {"KEEP": "1"})
            self.assertEqual(data["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"], "python keep.py")
            self.assertEqual(len(data["hooks"]["SessionStart"]), 4)
            managed = [entry for entry in data["hooks"]["SessionStart"] if entry.get("_managed_by") == "blog-writing-skill"]
            self.assertEqual(len(managed), 3)

    def test_init_reports_invalid_host_json_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = root / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text("{not json", encoding="utf-8")

            result = run_init("--root", str(root), "--harness", "claude", "--yes")

            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid JSON", result.stderr)

    def test_installer_cli_still_installs_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_installer("--harness", "codex", "--install", "--root", str(root), "--yes")
            data = json.loads((root / ".codex" / "hooks.json").read_text(encoding="utf-8"))
            command = data["hooks"]["SessionStart"][0]["hooks"][0]["command"]

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / ".codex" / "hooks.json").exists())
            self.assertTrue((root / ".trellis-writing" / "runtime" / "scripts" / "session_start.py").exists())
            self.assertIn(".trellis-writing", command)
            self.assertIn("Uninstall with:", result.stdout)

    def test_update_refreshes_managed_hook_to_local_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = root / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "SessionStart": [
                                {
                                    "_managed_by": "blog-writing-skill",
                                    "matcher": "startup",
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python C:/bundle/skills/blog-brainstorm/scripts/resume_context.py --root C:/project",
                                            "timeout": 30,
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = run_init("--root", str(root), "--harness", "claude", "--update", "--yes")
            data = json.loads(settings.read_text(encoding="utf-8"))
            command = data["hooks"]["SessionStart"][0]["hooks"][0]["command"]

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(".trellis-writing", command)
        self.assertNotIn("resume_context.py --root", command)
        self.assertIn("Updated runtime", result.stdout)

    def test_uninstall_removes_managed_hook_and_preserves_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "content" / "articles" / "demo" / "draft.md"
            article.parent.mkdir(parents=True)
            article.write_text("draft", encoding="utf-8")
            init_result = run_init("--root", str(root), "--harness", "claude", "--yes")

            result = run_init("--root", str(root), "--harness", "claude", "--uninstall", "--yes")
            data = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
            article_text = article.read_text(encoding="utf-8")

        self.assertEqual(init_result.returncode, 0, init_result.stderr)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(data["hooks"]["SessionStart"], [])
        self.assertEqual(article_text, "draft")
        self.assertIn("Uninstalled runtime", result.stdout)


if __name__ == "__main__":
    unittest.main()
