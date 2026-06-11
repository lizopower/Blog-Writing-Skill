from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
CLI_SCRIPT = REPO_ROOT / "scripts" / "blog-writing.py"


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


class BlogWritingCliTests(unittest.TestCase):
    def test_init_defaults_to_current_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_cli("init", "--no-session-hook", cwd=root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "content" / "articles").is_dir())
            self.assertTrue((root / ".trellis-writing" / "runtime" / "scripts" / "session_start.py").is_file())
            self.assertIn("Blog-Writing-Skill project init complete", result.stdout)

    def test_init_accepts_positional_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_cli("init", str(root), "--no-session-hook")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "content" / "specs" / "index.md").is_file())

    def test_check_maps_to_init_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_result = run_cli("init", str(root), "--harness", "codex", "--yes")

            result = run_cli("check", str(root), "--harness", "codex")

            self.assertEqual(init_result.returncode, 0, init_result.stderr)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("runtime_scripts", result.stdout)

    def test_rejects_positional_root_with_root_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_cli("init", str(root), "--root", str(root))

            self.assertEqual(result.returncode, 2)
            self.assertIn("either positionally or with --root", result.stderr)


if __name__ == "__main__":
    unittest.main()
