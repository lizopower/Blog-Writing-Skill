from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import doctor  # noqa: E402

ARTICLE = SCRIPTS_DIR / "article.py"
INIT = SCRIPTS_DIR / "init.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], text=True, capture_output=True, check=False)


def create_project(root: Path, harness: str = "claude") -> None:
    result = run(str(ARTICLE), "create", "Demo", "--slug", "demo", "--root", str(root), "--harness", harness)
    if result.returncode != 0:
        raise AssertionError(f"create failed: {result.stderr}")


def settings_path(root: Path) -> Path:
    return root / ".claude" / "settings.json"


class DoctorTests(unittest.TestCase):
    def test_healthy_project_passes_all_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)

            diagnosis = doctor.diagnose(root, "claude")

            self.assertTrue(diagnosis.ok, [c for c in diagnosis.checks if not c.ok])
            names = {c.name for c in diagnosis.checks}
            self.assertIn("hook_breadcrumb", names)
            self.assertIn("hook_phase_gate", names)
            self.assertIn("claude_project_instructions", names)

    def test_missing_runtime_script_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            (root / ".trellis-writing" / "runtime" / "scripts" / "inject_workflow_state.py").unlink()

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            scripts_check = next(c for c in diagnosis.checks if c.name == "runtime_scripts")
            self.assertFalse(scripts_check.ok)
            self.assertIn("inject_workflow_state.py", scripts_check.detail)

    def test_missing_hook_config_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            settings_path(root).unlink()

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "hook_config").ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "hook_session_start").ok)

    def test_missing_breadcrumb_hook_is_flagged(self) -> None:
        # Simulate a project initialized before the UserPromptSubmit breadcrumb existed.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            config = json.loads(settings_path(root).read_text(encoding="utf-8"))
            config["hooks"]["UserPromptSubmit"] = [
                e for e in config["hooks"]["UserPromptSubmit"] if e.get("_managed_by") != "blog-writing-skill"
            ]
            settings_path(root).write_text(json.dumps(config), encoding="utf-8")

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "hook_breadcrumb").ok)

    def test_missing_claude_project_instructions_are_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            (root / "CLAUDE.md").unlink()

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "claude_project_instructions").ok)

    def test_session_start_with_right_count_but_wrong_command_is_flagged(self) -> None:
        # A managed config can keep the right matcher count while pointing at a
        # stale/wrong script; doctor must catch that, not just count entries.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            config = json.loads(settings_path(root).read_text(encoding="utf-8"))
            for entry in config["hooks"]["SessionStart"]:
                if entry.get("_managed_by") == "blog-writing-skill":
                    entry["hooks"][0]["command"] = "python some_old_path/session_start.py"
            settings_path(root).write_text(json.dumps(config), encoding="utf-8")

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "hook_session_start").ok)

    def test_missing_template_hash_registry_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            (root / ".trellis-writing" / ".template-hashes.json").unlink()

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            fresh = next(c for c in diagnosis.checks if c.name == "runtime_fresh")
            self.assertFalse(fresh.ok)
            self.assertIn("no registry hash", fresh.detail)

    def test_invalid_config_json_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)
            settings_path(root).write_text("{bad json", encoding="utf-8")

            diagnosis = doctor.diagnose(root, "claude")

            self.assertFalse(diagnosis.ok)
            self.assertFalse(next(c for c in diagnosis.checks if c.name == "hook_config").ok)

    def test_codex_harness_omits_claude_only_checks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root, harness="codex")

            diagnosis = doctor.diagnose(root, "codex")

            self.assertTrue(diagnosis.ok, [c for c in diagnosis.checks if not c.ok])
            names = {c.name for c in diagnosis.checks}
            self.assertNotIn("hook_phase_gate", names)
            self.assertNotIn("hook_breadcrumb", names)
            self.assertNotIn("claude_project_instructions", names)

    def test_article_doctor_cli_returns_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)

            healthy = run(str(ARTICLE), "doctor", "--root", str(root))
            self.assertEqual(healthy.returncode, 0, healthy.stderr)
            self.assertIn("OK", healthy.stdout)

            settings_path(root).unlink()
            broken = run(str(ARTICLE), "doctor", "--root", str(root))
            self.assertEqual(broken.returncode, 1)
            self.assertIn("PROBLEMS", broken.stdout)

    def test_init_check_cli_returns_status_and_rejects_bad_combo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_project(root)

            healthy = run(str(INIT), "--root", str(root), "--check")
            self.assertEqual(healthy.returncode, 0, healthy.stderr)

            bad_combo = run(str(INIT), "--root", str(root), "--check", "--update")
            self.assertEqual(bad_combo.returncode, 1)
            self.assertIn("cannot be combined", bad_combo.stdout)


if __name__ == "__main__":
    unittest.main()
