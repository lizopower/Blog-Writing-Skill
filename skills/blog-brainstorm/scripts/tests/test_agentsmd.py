from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _agentsmd import (  # noqa: E402
    MARKER_BEGIN,
    MARKER_END,
    remove_prelude,
    render_prelude,
    upsert_prelude,
)
from phase_gate import ARTIFACT_MIN_PHASE  # noqa: E402
from install_session_hook import clear_prelude, write_prelude  # noqa: E402


class RenderPreludeTests(unittest.TestCase):
    def test_block_is_marker_delimited(self) -> None:
        block = render_prelude()
        self.assertTrue(block.startswith(MARKER_BEGIN))
        self.assertIn(MARKER_END, block)

    def test_block_lists_every_gated_artifact_and_phase(self) -> None:
        block = render_prelude()
        for name, phase in ARTIFACT_MIN_PHASE.items():
            self.assertIn(name, block)
            self.assertIn(phase, block)

    def test_block_directs_to_resume_context(self) -> None:
        self.assertIn("resume_context.py --root .", render_prelude())


class UpsertPreludeTests(unittest.TestCase):
    def test_creates_file_content_when_blank(self) -> None:
        result = upsert_prelude("", render_prelude())
        self.assertTrue(result.startswith(MARKER_BEGIN))

    def test_appends_after_existing_user_content(self) -> None:
        existing = "# Local Override\n\nCCG disabled.\n"
        result = upsert_prelude(existing, render_prelude())
        self.assertTrue(result.startswith("# Local Override"))
        self.assertIn("CCG disabled.", result)
        self.assertIn(MARKER_BEGIN, result)

    def test_replaces_existing_block_in_place_is_idempotent(self) -> None:
        existing = "intro\n\n" + render_prelude() + "\noutro\n"
        once = upsert_prelude(existing, render_prelude())
        twice = upsert_prelude(once, render_prelude())
        self.assertEqual(once, twice)
        self.assertEqual(once.count(MARKER_BEGIN), 1)
        self.assertIn("intro", once)
        self.assertIn("outro", once)


class RemovePreludeTests(unittest.TestCase):
    def test_strips_block_and_preserves_surrounding_content(self) -> None:
        existing = "# Keep\n\n" + render_prelude() + "\n# Also keep\n"
        result = remove_prelude(existing)
        self.assertNotIn(MARKER_BEGIN, result)
        self.assertIn("# Keep", result)
        self.assertIn("# Also keep", result)

    def test_noop_without_managed_block(self) -> None:
        existing = "# Untouched\n"
        self.assertEqual(remove_prelude(existing), existing)

    def test_empty_when_block_was_sole_content(self) -> None:
        self.assertEqual(remove_prelude(render_prelude()), "")


class PreludeIOTests(unittest.TestCase):
    def test_write_then_clear_round_trip_preserves_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents = root / "AGENTS.md"
            agents.write_text("# Local Override\n\nKeep me.\n", encoding="utf-8")

            written = write_prelude(root)
            self.assertEqual(written, agents)
            body = agents.read_text(encoding="utf-8")
            self.assertIn("Keep me.", body)
            self.assertIn(MARKER_BEGIN, body)

            cleared = clear_prelude(root)
            self.assertEqual(cleared, agents)
            final = agents.read_text(encoding="utf-8")
            self.assertNotIn(MARKER_BEGIN, final)
            self.assertIn("Keep me.", final)

    def test_clear_removes_file_when_block_was_sole_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_prelude(root)
            clear_prelude(root)
            self.assertFalse((root / "AGENTS.md").exists())

    def test_clear_is_noop_when_no_managed_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents = root / "AGENTS.md"
            agents.write_text("# Mine\n", encoding="utf-8")
            self.assertIsNone(clear_prelude(root))
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Mine\n")


if __name__ == "__main__":
    unittest.main()
