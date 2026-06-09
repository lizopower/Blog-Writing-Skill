#!/usr/bin/env python3
"""Initialize a project for Blog-Writing-Skill workflows."""

from __future__ import annotations

import argparse
from pathlib import Path

from install_session_hook import install_hook
from spec import ensure_store, index_path


def ensure_articles_dir(root: Path) -> Path:
    articles = root / "content" / "articles"
    articles.mkdir(parents=True, exist_ok=True)
    return articles


def selected_harnesses(value: str) -> list[str]:
    if value == "all":
        return ["claude", "codex"]
    return [value]


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    articles = ensure_articles_dir(root)
    ensure_store(root)
    specs_index = index_path(root)

    installed: list[str] = []
    if not args.no_session_hook:
        for harness in selected_harnesses(args.harness):
            result = install_hook(root, harness, assume_yes=args.yes, print_diff=True)
            if result != 0:
                return result
            installed.append(harness)

    print("\nBlog-Writing-Skill project init complete.")
    print(f"- Articles directory: {articles}")
    print(f"- Project specs index: {specs_index}")
    if installed:
        print(f"- Installed hooks: {', '.join(installed)}")
        for harness in installed:
            print(
                "- Uninstall "
                f"{harness}: python {Path(__file__).with_name('install_session_hook.py')} "
                f"--harness {harness} --uninstall --root {root}"
            )
        print("- First session may ask you to trust this hook. Review and approve it; do not bypass hook trust.")
    else:
        print("- Session hook: skipped")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize Blog-Writing-Skill project directories and optional hooks.")
    parser.add_argument("--root", default=".", help="Project root to initialize.")
    parser.add_argument("--harness", choices=["claude", "codex", "all"], default="claude")
    parser.add_argument("--no-session-hook", action="store_true", help="Only create project directories/spec store.")
    parser.add_argument("--yes", action="store_true", help="Skip hook confirmation prompt.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return cmd_init(args)


if __name__ == "__main__":
    raise SystemExit(main())
