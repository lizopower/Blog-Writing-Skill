from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _runtimeinstaller import (  # noqa: E402
    install_runtime,
    load_hashes,
    runtime_root,
    template_files,
    uninstall_runtime,
    update_runtime,
)


class RuntimeInstallerTests(unittest.TestCase):
    def test_install_runtime_writes_hash_registry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            install_runtime(root)
            registry = load_hashes(root)

        self.assertIn("version", registry)
        self.assertIn("runtime/scripts/session_start.py", registry["files"])
        self.assertIn("runtime/scripts/resume_context.py", registry["files"])
        self.assertIn("runtime/scripts/inject_workflow_state.py", registry["files"])
        self.assertIn("runtime/prompts/draft.md", registry["files"])

    def test_update_rewrites_unchanged_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_runtime(root)
            session_start = runtime_root(root) / "runtime" / "scripts" / "session_start.py"
            session_start.write_text(template_files()[0].render(), encoding="utf-8")

            result = update_runtime(root)

            self.assertFalse(result.conflicts)
            self.assertEqual(session_start.read_text(encoding="utf-8"), template_files()[0].render())

    def test_update_preserves_modified_file_and_writes_new(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_runtime(root)
            session_start = runtime_root(root) / "runtime" / "scripts" / "session_start.py"
            session_start.write_text("# user custom\n", encoding="utf-8")

            result = update_runtime(root)
            new_path = session_start.with_name(session_start.name + ".new")

            self.assertEqual(session_start.read_text(encoding="utf-8"), "# user custom\n")
            self.assertTrue(new_path.is_file())
            self.assertIn("runtime/scripts/session_start.py", result.conflicts)

    def test_update_does_not_touch_content_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "content" / "articles" / "demo" / "draft.md"
            spec = root / "content" / "specs" / "tone.md"
            article.parent.mkdir(parents=True)
            spec.parent.mkdir(parents=True)
            article.write_text("draft", encoding="utf-8")
            spec.write_text("tone", encoding="utf-8")
            install_runtime(root)

            update_runtime(root)

            self.assertEqual(article.read_text(encoding="utf-8"), "draft")
            self.assertEqual(spec.read_text(encoding="utf-8"), "tone")

    def test_uninstall_runtime_deletes_unchanged_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_runtime(root)

            result = uninstall_runtime(root)

            self.assertFalse(result.preserved)
            self.assertFalse((runtime_root(root) / "runtime" / "scripts" / "session_start.py").exists())

    def test_uninstall_runtime_preserves_modified_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install_runtime(root)
            session_start = runtime_root(root) / "runtime" / "scripts" / "session_start.py"
            session_start.write_text("# user custom\n", encoding="utf-8")

            result = uninstall_runtime(root)

            self.assertTrue(session_start.exists())
            self.assertIn("runtime/scripts/session_start.py", result.preserved)

    def test_uninstall_runtime_preserves_content_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / "content" / "articles" / "demo" / "draft.md"
            spec = root / "content" / "specs" / "tone.md"
            article.parent.mkdir(parents=True)
            spec.parent.mkdir(parents=True)
            article.write_text("draft", encoding="utf-8")
            spec.write_text("tone", encoding="utf-8")
            install_runtime(root)

            uninstall_runtime(root)

            self.assertEqual(article.read_text(encoding="utf-8"), "draft")
            self.assertEqual(spec.read_text(encoding="utf-8"), "tone")


if __name__ == "__main__":
    unittest.main()
