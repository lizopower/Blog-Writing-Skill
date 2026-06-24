#!/usr/bin/env python3
"""Tests for run_stage.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))
RUN_STAGE = SCRIPTS_DIR / "run_stage.py"
CREATE = SCRIPTS_DIR / "article.py"

from _runtimeinstaller import install_runtime, runtime_root  # noqa: E402


class RunStageTests(unittest.TestCase):
    def test_run_stage_writes_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            proc_create = subprocess.run(
                [
                    sys.executable,
                    str(CREATE),
                    "create",
                    "Demo",
                    "--slug",
                    "demo",
                    "--root",
                    str(root),
                    "--no-hooks",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc_create.returncode, 0, proc_create.stderr)
            (root / "content" / "articles" / "demo" / "brief.md").write_text(
                "# Brief\n\n## Business Goal\n\ngoal\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RUN_STAGE),
                    "--root",
                    str(root),
                    "--slug",
                    "demo",
                    "--stage",
                    "brainstorming",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("recommended_skill: blog-brainstorm", proc.stdout)
            context_path = root / "content" / "articles" / "demo" / "stage" / "brainstorming_context.txt"
            self.assertTrue(context_path.exists())
            self.assertIn("Business Goal", context_path.read_text(encoding="utf-8"))

    def test_installed_runtime_run_stage_uses_copied_prompts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_runtime(root)
            workspace = root / "content" / "articles" / "demo"
            workspace.mkdir(parents=True)
            (workspace / "article.json").write_text(
                json.dumps({"id": "demo", "title": "Demo", "currentPhase": "outlining"}),
                encoding="utf-8",
            )
            (workspace / "brief.md").write_text("# Brief\n\n## Business Goal\n\ngoal\n", encoding="utf-8")
            runtime_script = runtime_root(root) / "runtime" / "scripts" / "run_stage.py"

            proc = subprocess.run(
                [
                    sys.executable,
                    str(runtime_script),
                    "--root",
                    str(root),
                    "--slug",
                    "demo",
                    "--stage",
                    "outlining",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            context_path = workspace / "stage" / "outlining_context.txt"
            self.assertIn("# Outline prompt", context_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
