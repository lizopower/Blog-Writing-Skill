from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

VALIDATE_SCRIPT = SCRIPTS_DIR / "validate_article_workspace.py"

from create_article_workspace import create_workspace  # noqa: E402
from validate_article_workspace import _load_json, validate_workspace  # noqa: E402


def run_validate(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class LoadJsonTests(unittest.TestCase):
    def test_load_json_file_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            data, error = _load_json(path)

        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertIn("file not found", error)

    def test_load_json_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{not json", encoding="utf-8")

            data, error = _load_json(path)

        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertIn("invalid JSON", error)

    def test_load_json_root_must_be_object(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "array.json"
            path.write_text('["not", "an", "object"]', encoding="utf-8")

            data, error = _load_json(path)

        self.assertIsNone(data)
        self.assertIsNotNone(error)
        self.assertIn("root must be an object", error)

    def test_load_json_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.json"
            path.write_text(json.dumps({"id": "demo"}), encoding="utf-8")

            data, error = _load_json(path)

        self.assertEqual(data, {"id": "demo"})
        self.assertIsNone(error)


class ValidateArticleWorkspaceTests(unittest.TestCase):
    def test_validate_workspace_nonexistent_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "missing"

            ok, errors, warnings = validate_workspace(workspace)

        self.assertFalse(ok)
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [f"{workspace}: workspace does not exist"])

    def test_validate_workspace_file_not_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "article"
            workspace.write_text("not a directory", encoding="utf-8")

            ok, errors, warnings = validate_workspace(workspace)

        self.assertFalse(ok)
        self.assertEqual(warnings, [])
        self.assertEqual(errors, [f"{workspace}: workspace is not a directory"])

    def test_validate_workspace_freshly_created_workspace_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory), "demo", "Demo Title", "blog")

            ok, errors, warnings = validate_workspace(workspace)

        self.assertTrue(ok, errors)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_validate_workspace_missing_article_json_surfaces_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory), "demo", "Demo Title", "blog")
            (workspace / "article.json").unlink()

            ok, errors, warnings = validate_workspace(workspace)

        self.assertFalse(ok)
        self.assertEqual(warnings, [])
        self.assertIn("missing required artifact: article.json", errors)
        self.assertTrue(any("article.json" in error and "file not found" in error for error in errors))

    def test_validate_workspace_invalid_article_json_surfaces_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory), "demo", "Demo Title", "blog")
            (workspace / "article.json").write_text("{not json", encoding="utf-8")

            ok, errors, warnings = validate_workspace(workspace)

        self.assertFalse(ok)
        self.assertEqual(warnings, [])
        self.assertTrue(any("article.json" in error and "invalid JSON" in error for error in errors))

    def test_validate_workspace_invalid_phase_surfaces_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory), "demo", "Demo Title", "blog")
            article_path = workspace / "article.json"
            data = json.loads(article_path.read_text(encoding="utf-8"))
            data["currentPhase"] = "not-a-real-phase"
            article_path.write_text(json.dumps(data), encoding="utf-8")

            ok, errors, warnings = validate_workspace(workspace)

        self.assertFalse(ok)
        self.assertTrue(any("currentPhase" in error and "invalid phase" in error for error in errors))

    def test_cli_exit_codes_for_valid_and_invalid_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = create_workspace(root, "demo", "Demo Title", "blog")

            valid = run_validate(str(workspace))
            invalid = run_validate(str(root / "missing"))

        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertIn("Article workspace is VALID", valid.stdout)
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("Article workspace is INVALID", invalid.stdout)
        self.assertIn("workspace does not exist", invalid.stdout)


if __name__ == "__main__":
    unittest.main()
