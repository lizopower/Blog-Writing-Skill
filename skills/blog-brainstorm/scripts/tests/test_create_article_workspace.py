from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

CREATE_SCRIPT = SCRIPTS_DIR / "create_article_workspace.py"
VALIDATE_SCRIPT = SCRIPTS_DIR / "validate_article_workspace.py"

from create_article_workspace import REQUIRED_FILES, create_workspace, now_iso, slugify  # noqa: E402


ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def run_create(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CREATE_SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def run_validate(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


class CreateArticleWorkspaceTests(unittest.TestCase):
    def test_slugify_normal_title(self) -> None:
        self.assertEqual(slugify("How to Build Better B2B Content"), "how-to-build-better-b2b-content")

    def test_slugify_empty_string_falls_back(self) -> None:
        self.assertEqual(slugify(""), "untitled-article")

    def test_slugify_special_char_only_falls_back(self) -> None:
        self.assertEqual(slugify(" !@#$%^&*() "), "untitled-article")

    def test_slugify_mixed_case_and_spaces_to_kebab(self) -> None:
        self.assertEqual(slugify("  Mixed   CASE   Title  "), "mixed-case-title")

    def test_now_iso_uses_utc_z_without_microseconds(self) -> None:
        timestamp = now_iso()

        self.assertRegex(timestamp, ISO_Z)
        self.assertNotIn(".", timestamp)

    def test_create_workspace_returns_path_and_writes_expected_article_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            workspace = create_workspace(root, "custom-slug", "Custom Title", "how-to")
            article = json.loads((workspace / "article.json").read_text(encoding="utf-8"))

        self.assertEqual(workspace, root / "content" / "articles" / "custom-slug")
        self.assertEqual(
            article,
            {
                "id": "custom-slug",
                "title": "Custom Title",
                "status": "brainstorming",
                "currentPhase": "brainstorming",
                "nextAction": "clarify audience and angle",
                "articleType": "how-to",
                "businessGoal": "",
                "audience": [],
                "primaryKeyword": "",
                "angle": "",
                "createdAt": article["createdAt"],
                "updatedAt": article["updatedAt"],
            },
        )
        self.assertRegex(article["createdAt"], ISO_Z)
        self.assertEqual(article["updatedAt"], article["createdAt"])

    def test_create_workspace_creates_expected_skeleton_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            workspace = create_workspace(root, "demo", "Demo Title", "blog")

            self.assertTrue((workspace / "research").is_dir())
            for relative_path in REQUIRED_FILES:
                self.assertTrue((workspace / relative_path).is_file(), relative_path)
            self.assertIn("# Demo Title", (workspace / "brief.md").read_text(encoding="utf-8"))

    def test_create_workspace_is_idempotent_and_preserves_existing_article(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            first = create_workspace(root, "demo", "Demo Title", "blog")
            article_path = first / "article.json"
            mutated = json.loads(article_path.read_text(encoding="utf-8"))
            mutated["currentPhase"] = "drafting"
            article_path.write_text(json.dumps(mutated), encoding="utf-8")

            second = create_workspace(root, "demo", "Demo Title", "blog")
            preserved = json.loads(article_path.read_text(encoding="utf-8"))

        self.assertEqual(first, second)
        self.assertEqual(preserved["currentPhase"], "drafting")

    def test_cli_create_then_validate_round_trip_with_default_slug(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            created = run_create("Round Trip Draft", "--root", str(root), "--type", "white-paper")
            workspace = root / "content" / "articles" / "round-trip-draft"
            validated = run_validate(str(workspace))
            article = json.loads((workspace / "article.json").read_text(encoding="utf-8"))

        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertEqual(Path(created.stdout.strip()).resolve(), workspace.resolve())
        self.assertEqual(article["articleType"], "white-paper")
        self.assertEqual(validated.returncode, 0, validated.stderr)
        self.assertIn("Article workspace is VALID", validated.stdout)

    def test_cli_rejects_unknown_article_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            created = run_create("Bad Type", "--root", str(root), "--type", "guide")

        self.assertEqual(created.returncode, 2)
        self.assertFalse((root / "content" / "articles" / "bad-type").exists())


if __name__ == "__main__":
    unittest.main()
