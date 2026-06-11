from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _claudemd import (  # noqa: E402
    MARKER_BEGIN,
    MARKER_END,
    remove_prelude,
    render_prelude,
    upsert_prelude,
)
from install_session_hook import clear_claude_instructions, write_claude_instructions  # noqa: E402


class RenderClaudePreludeTests(unittest.TestCase):
    def test_block_is_marker_delimited(self) -> None:
        block = render_prelude(Path("C:/scaffold"))

        self.assertTrue(block.startswith(MARKER_BEGIN))
        self.assertIn(MARKER_END, block)

    def test_block_points_to_scaffold_skill_files(self) -> None:
        block = render_prelude(Path("C:/scaffold"))

        self.assertIn("SKILL.md", block)
        self.assertIn("blog-writing-workflow", block)
        self.assertIn("blog-brainstorm", block)
        self.assertIn("article.py", block)
        self.assertIn("Rich input is not a waiver", block)
        self.assertIn("Do not manually create", block)


class ClaudePreludeEditTests(unittest.TestCase):
    def test_appends_after_existing_user_content(self) -> None:
        existing = "# Local Claude Rules\n\nKeep this.\n"

        result = upsert_prelude(existing, render_prelude(Path("C:/scaffold")))

        self.assertTrue(result.startswith("# Local Claude Rules"))
        self.assertIn("Keep this.", result)
        self.assertIn(MARKER_BEGIN, result)

    def test_replaces_existing_block_in_place(self) -> None:
        old = render_prelude(Path("C:/old"))
        new = render_prelude(Path("C:/new"))
        existing = f"intro\n\n{old}\noutro\n"

        result = upsert_prelude(existing, new)

        self.assertEqual(result.count(MARKER_BEGIN), 1)
        self.assertIn("C:/new", result.replace("\\", "/"))
        self.assertIn("intro", result)
        self.assertIn("outro", result)

    def test_remove_preserves_user_content(self) -> None:
        existing = "# Keep\n\n" + render_prelude(Path("C:/scaffold")) + "\n# Also keep\n"

        result = remove_prelude(existing)

        self.assertNotIn(MARKER_BEGIN, result)
        self.assertIn("# Keep", result)
        self.assertIn("# Also keep", result)


class ClaudePreludeIOTests(unittest.TestCase):
    def test_write_then_clear_round_trip_preserves_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claude = root / "CLAUDE.md"
            claude.write_text("# Local Claude Rules\n\nKeep me.\n", encoding="utf-8")

            written = write_claude_instructions(root)
            self.assertEqual(written, claude)
            body = claude.read_text(encoding="utf-8")
            self.assertIn("Keep me.", body)
            self.assertIn(MARKER_BEGIN, body)

            cleared = clear_claude_instructions(root)
            self.assertEqual(cleared, claude)
            final = claude.read_text(encoding="utf-8")
            self.assertNotIn(MARKER_BEGIN, final)
            self.assertIn("Keep me.", final)

    def test_clear_removes_file_when_block_was_sole_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_claude_instructions(root)
            clear_claude_instructions(root)
            self.assertFalse((root / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
