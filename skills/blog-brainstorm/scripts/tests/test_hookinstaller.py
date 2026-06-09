from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
INSTALLER = SCRIPTS_DIR / "install_session_hook.py"

from _hookinstaller import (  # noqa: E402
    MANAGED_BY,
    build_session_start_entries,
    merge_block,
    remove_block,
    render_diff,
)
from install_session_hook import command_for  # noqa: E402
from _runtimeinstaller import install_runtime  # noqa: E402


class HookInstallerTests(unittest.TestCase):
    def test_merge_block_preserves_existing_hooks_and_adds_managed_entries(self) -> None:
        config = {
            "env": {"KEEP": "1"},
            "hooks": {
                "SessionStart": [
                    {
                        "matcher": "startup",
                        "hooks": [{"type": "command", "command": "python existing.py", "timeout": 30}],
                    }
                ],
                "PreToolUse": [{"matcher": "Task", "hooks": []}],
            },
        }
        block = build_session_start_entries("python resume_context.py --root C:/proj", timeout=10)

        merged = merge_block(config, block)

        self.assertEqual(config["hooks"]["SessionStart"][0]["hooks"][0]["command"], "python existing.py")
        self.assertEqual(merged["env"], {"KEEP": "1"})
        self.assertEqual(merged["hooks"]["PreToolUse"], [{"matcher": "Task", "hooks": []}])
        self.assertEqual(len(merged["hooks"]["SessionStart"]), 4)
        self.assertEqual(
            [entry["_managed_by"] for entry in merged["hooks"]["SessionStart"][1:]],
            [MANAGED_BY, MANAGED_BY, MANAGED_BY],
        )

    def test_merge_block_replaces_previous_managed_entries(self) -> None:
        old_block = build_session_start_entries("python old.py", timeout=10)
        new_block = build_session_start_entries("python new.py", timeout=10)
        config = merge_block({}, old_block)

        merged = merge_block(config, new_block)

        self.assertEqual(len(merged["hooks"]["SessionStart"]), 3)
        self.assertTrue(all(entry["hooks"][0]["command"] == "python new.py" for entry in merged["hooks"]["SessionStart"]))

    def test_remove_block_is_idempotent_and_preserves_host_config(self) -> None:
        config = merge_block(
            {"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python keep.py"}]}]}},
            build_session_start_entries("python resume_context.py", timeout=10),
        )

        removed = remove_block(config)
        removed_again = remove_block(removed)

        self.assertEqual(removed, removed_again)
        self.assertEqual(removed["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"], "python keep.py")
        self.assertEqual(removed["hooks"].get("SessionStart"), [])

    def test_render_diff_includes_why_and_unified_diff(self) -> None:
        old = {"hooks": {"SessionStart": []}}
        new = merge_block(old, build_session_start_entries("python resume_context.py", timeout=10))

        diff = render_diff(old, new, why="Inject current article context at session start.")

        self.assertIn("Why: Inject current article context at session start.", diff)
        self.assertIn("--- before", diff)
        self.assertIn("+++ after", diff)
        self.assertIn("resume_context.py", diff)

    def test_installer_cli_installs_and_uninstalls_claude_hook(self) -> None:
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
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )

            installed = run_installer("--harness", "claude", "--install", "--root", str(root), "--yes")
            data = json.loads(settings.read_text(encoding="utf-8"))
            uninstalled = run_installer("--harness", "claude", "--uninstall", "--root", str(root), "--yes")
            cleaned = json.loads(settings.read_text(encoding="utf-8"))

        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertIn("Why:", installed.stdout)
        self.assertIn("Uninstall with:", installed.stdout)
        self.assertEqual(len(data["hooks"]["SessionStart"]), 4)
        self.assertEqual(data["hooks"]["SessionStart"][0]["hooks"][0]["command"], "python existing.py")
        self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
        self.assertEqual(cleaned["hooks"]["SessionStart"][0]["hooks"][0]["command"], "python existing.py")
        self.assertEqual(len(cleaned["hooks"]["SessionStart"]), 1)

    def test_installer_cli_uses_codex_hooks_json_schema_from_sample(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = run_installer("--harness", "codex", "--install", "--root", str(root), "--yes")
            hooks_json = root / ".codex" / "hooks.json"
            data = json.loads(hooks_json.read_text(encoding="utf-8"))
            uninstalled = run_installer("--harness", "codex", "--uninstall", "--root", str(root), "--yes")
            cleaned = json.loads(hooks_json.read_text(encoding="utf-8"))

        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertIn("hook trust", installed.stdout)
        self.assertIn("hooks", data)
        self.assertIn("SessionStart", data["hooks"])
        self.assertNotIn("session_start", data)
        self.assertEqual(len(data["hooks"]["SessionStart"]), 3)
        self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
        self.assertEqual(cleaned["hooks"]["SessionStart"], [])


    @unittest.skipUnless(sys.platform == "win32", "Windows command-shell quoting regression")
    def test_generated_command_runs_under_windows_command_shell(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project with spaces"
            article_dir = root / "content" / "articles" / "demo"
            article_dir.mkdir(parents=True)
            (article_dir / "article.json").write_text(
                json.dumps(
                    {
                        "currentPhase": "drafting",
                        "track": "full",
                        "updatedAt": "2026-06-09T12:00:00Z",
                    }
                ),
                encoding="utf-8",
            )
            install_runtime(root)

            result = subprocess.run(
                command_for(root),
                cwd=str(root),
                shell=True,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current Target: demo", result.stdout)


    def test_installer_cli_reports_invalid_host_json_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings = root / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text("{bad json", encoding="utf-8")

            result = run_installer("--harness", "claude", "--install", "--root", str(root), "--yes")
            unchanged = settings.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid JSON", result.stderr)
        self.assertNotIn("NameError", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(unchanged, "{bad json")


def run_installer(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), *args],
        text=True,
        capture_output=True,
        check=False,
    )


if __name__ == "__main__":
    unittest.main()
