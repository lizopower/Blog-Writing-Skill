#!/usr/bin/env python3
"""Small command wrapper for project-local Blog-Writing-Skill tasks."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
BRAINSTORM_SCRIPTS = REPO_ROOT / "skills" / "blog-brainstorm" / "scripts"
INIT_SCRIPT = BRAINSTORM_SCRIPTS / "init.py"


def _load_script(path: Path, module_name: str) -> ModuleType:
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _has_root_flag(args: list[str]) -> bool:
    return "--root" in args or any(item.startswith("--root=") for item in args)


def _forward_init(command: str, args: list[str]) -> int:
    positional_root: str | None = None
    forwarded = list(args)

    if forwarded and not forwarded[0].startswith("-"):
        positional_root = forwarded.pop(0)

    if positional_root is not None and _has_root_flag(forwarded):
        print("error: pass the project root either positionally or with --root, not both", file=sys.stderr)
        return 2

    if not _has_root_flag(forwarded):
        forwarded = ["--root", positional_root or ".", *forwarded]

    if command == "check":
        forwarded.append("--check")
    elif command == "update":
        forwarded.append("--update")
    elif command == "uninstall":
        forwarded.append("--uninstall")

    init_module = _load_script(INIT_SCRIPT, "blog_writing_skill_init")
    return int(init_module.main(forwarded))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blog-writing",
        description="Run Blog-Writing-Skill project commands from any writing project.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["init", "check", "update", "uninstall"],
        help="Command to run. Use 'init' to set up the current project.",
    )
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments passed to the command.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(argv)
    if parsed.command is None:
        parser.print_help()
        return 0
    return _forward_init(parsed.command, parsed.args)


if __name__ == "__main__":
    raise SystemExit(main())
