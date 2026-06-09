from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "spec.py"


def run_spec(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


class SpecCliTests(unittest.TestCase):
    def test_init_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            first = run_spec("init", "--root", str(root))
            second = run_spec("init", "--root", str(root))

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue((root / "content" / "specs" / "index.md").exists())

    def test_add_writes_spec_and_index_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = run_spec(
                "add",
                "--title",
                "Numeric Formatting",
                "--root",
                str(root),
                "--slug",
                "numeric-formatting",
                input_text="Use SI units.",
            )
            duplicate = run_spec(
                "add",
                "--title",
                "Numeric Formatting",
                "--root",
                str(root),
                "--slug",
                "numeric-formatting",
                input_text="Overwrite attempt.",
            )

            spec_file = root / "content" / "specs" / "numeric-formatting.md"
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(duplicate.returncode, 1)
            self.assertIn("already exists", duplicate.stderr)
            self.assertIn("Use SI units.", spec_file.read_text(encoding="utf-8"))
            self.assertNotIn("Overwrite attempt.", spec_file.read_text(encoding="utf-8"))
            self.assertIn("numeric-formatting.md", (root / "content" / "specs" / "index.md").read_text(encoding="utf-8"))

    def test_list_and_show(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_spec(
                "add",
                "--title",
                "Numeric Formatting",
                "--root",
                str(root),
                "--slug",
                "numeric-formatting",
                input_text="Use SI units.",
            )

            listing = run_spec("list", "--root", str(root))
            shown = run_spec("show", "numeric-formatting", "--root", str(root))

            self.assertIn("numeric-formatting", listing.stdout)
            self.assertIn("Numeric Formatting", listing.stdout)
            self.assertIn("Use SI units.", shown.stdout)

    def test_add_writes_only_project_content_specs_not_bundle_standards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            standards = root / "standards"
            standards.mkdir()
            marker = standards / "marker.md"
            marker.write_text("do not touch", encoding="utf-8")

            result = run_spec(
                "add",
                "--title",
                "Project Rule",
                "--root",
                str(root),
                "--slug",
                "project-rule",
                input_text="Project-local rule.",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "do not touch")
            self.assertTrue((root / "content" / "specs" / "project-rule.md").exists())
            self.assertFalse((standards / "project-rule.md").exists())


if __name__ == "__main__":
    unittest.main()
