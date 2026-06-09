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
            self.assertIn("resume_context.py", data["hooks"]["SessionStart"][0]["hooks"][0]["command"])
            self.assertIn("Installed hooks: claude", result.stdout)
            self.assertIn("First session may ask you to trust", result.stdout)

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

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / ".codex" / "hooks.json").exists())
            self.assertIn("Uninstall with:", result.stdout)


if __name__ == "__main__":
    unittest.main()
