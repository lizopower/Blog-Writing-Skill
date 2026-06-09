#!/usr/bin/env python3
"""Manage project-local writing specs under content/specs."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from _specstore import merge_index_entries, parse_index, parse_spec, render_index, render_spec, slugify


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def specs_dir(root: Path) -> Path:
    return root / "content" / "specs"


def index_path(root: Path) -> Path:
    return specs_dir(root) / "index.md"


def ensure_store(root: Path) -> Path:
    directory = specs_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = index_path(root)
    if not path.exists():
        path.write_text(render_index([]), encoding="utf-8")
    return directory


def read_body(args: argparse.Namespace) -> str:
    if args.from_file:
        return Path(args.from_file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_store(root)
    print(index_path(root))
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    directory = ensure_store(root)
    slug = args.slug or slugify(args.title)
    target = directory / f"{slug}.md"
    if target.exists():
        print(f"{target}: spec already exists", file=sys.stderr)
        return 1

    body = read_body(args)
    hook = args.hook or first_body_line(body)
    target.write_text(
        render_spec(
            spec_id=slug,
            title=args.title,
            scope=args.scope,
            created_at=now_iso(),
            body=body,
        ),
        encoding="utf-8",
    )

    existing = parse_index(index_path(root).read_text(encoding="utf-8"))
    merged = merge_index_entries(existing, [(slug, args.title, hook)])
    index_path(root).write_text(render_index(merged), encoding="utf-8")
    print(target)
    return 0


def first_body_line(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def cmd_list(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    directory = ensure_store(root)
    specs = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "index.md":
            continue
        parsed = parse_spec(path.read_text(encoding="utf-8"))
        specs.append(
            (
                parsed.front_matter.get("id", path.stem),
                parsed.front_matter.get("title", path.stem),
                parsed.front_matter.get("scope", "project"),
            )
        )
    for spec_id, title, scope in specs:
        print(f"{spec_id}\t{title}\t{scope}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    path = specs_dir(root) / f"{args.slug}.md"
    if not path.exists():
        print(f"{path}: spec not found", file=sys.stderr)
        return 1
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage project-local writing specs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create content/specs and index.md.")
    init.add_argument("--root", default=".", help="Project root.")
    init.set_defaults(func=cmd_init)

    add = subparsers.add_parser("add", help="Add a project-local writing spec.")
    add.add_argument("--title", required=True, help="Spec title.")
    add.add_argument("--scope", default="project", help="Spec scope, e.g. project or article:<slug>.")
    add.add_argument("--root", default=".", help="Project root.")
    add.add_argument("--slug", help="Spec slug. Defaults to slugified title.")
    add.add_argument("--from-file", help="Read spec body from a file. Defaults to stdin.")
    add.add_argument("--hook", help="One-line index hook. Defaults to first body line.")
    add.set_defaults(func=cmd_add)

    listing = subparsers.add_parser("list", help="List project-local specs.")
    listing.add_argument("--root", default=".", help="Project root.")
    listing.set_defaults(func=cmd_list)

    show = subparsers.add_parser("show", help="Show a spec by slug.")
    show.add_argument("slug", help="Spec slug.")
    show.add_argument("--root", default=".", help="Project root.")
    show.set_defaults(func=cmd_show)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
