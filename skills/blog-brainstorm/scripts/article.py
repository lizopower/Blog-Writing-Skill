#!/usr/bin/env python3
"""Manage Blog-Writing-Skill article lifecycle state."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _statemachine import PHASES, TRANSITIONS, advance_article, can_transition, migrate
from create_article_workspace import VALID_ARTICLE_TYPES, create_workspace, slugify


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def workspace_path(root: Path, slug: str) -> Path:
    return root / "content" / "articles" / slug


def load_article(workspace: Path) -> dict[str, Any]:
    path = workspace / "article.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{path}: article.json not found") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be an object")
    return data


def save_article(workspace: Path, article: dict[str, Any]) -> None:
    (workspace / "article.json").write_text(
        json.dumps(article, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def ensure_hooks(root: Path, harness: str) -> bool:
    """Install session/gate hooks for the selected harness(es).

    Returns ``True`` only when every selected harness installs cleanly. This is
    a hard gate for ``create`` (Trellis parity): the workflow must not run
    without context injection, so a failure here is fatal unless the caller
    explicitly opted out with ``--no-hooks``.
    """
    from install_session_hook import HARNESS_CONFIG, install_hook

    harnesses = sorted(HARNESS_CONFIG) if harness == "all" else [harness]
    ok = True
    for name in harnesses:
        try:
            code = install_hook(root, name, assume_yes=True, print_diff=False)
        except Exception as exc:  # noqa: BLE001 - report and fail the gate, do not crash
            print(f"error: {name} hook install failed ({exc})", file=sys.stderr)
            ok = False
            continue
        if code != 0:
            print(f"error: {name} hook install failed", file=sys.stderr)
            ok = False
    return ok


def cmd_create(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    if not args.no_hooks:
        # Hard gate: install context-injection hooks BEFORE creating the
        # workspace so a hook failure leaves no half-initialized project (a
        # workspace that would run without injection — the silent failure mode
        # this gate exists to prevent). Opt out explicitly with --no-hooks.
        if not ensure_hooks(root, args.harness):
            print(
                "error: session hook installation failed; refusing to create a workspace that "
                "would run without workflow context injection. Fix the cause shown above and retry, "
                "run init.py manually, or pass --no-hooks to create the workspace without hooks.",
                file=sys.stderr,
            )
            return 1
    slug = args.slug or slugify(args.title)
    workspace = create_workspace(root, slug, args.title, args.type)
    article = migrate(load_article(workspace))
    article["track"] = args.track
    article.setdefault("history", [])
    article.setdefault("waivers", [])
    article.setdefault("series", None)
    save_article(workspace, article)
    print(workspace)
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    workspace = workspace_path(root, args.slug)
    try:
        article = load_article(workspace)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    updated, result = advance_article(
        article,
        args.to,
        workspace,
        waive_reason=args.waive,
        now=now_iso(),
    )
    if not result.ok:
        print(result.reason, file=sys.stderr)
        return 1

    save_article(workspace, updated)
    print(f"{args.slug}: {article.get('currentPhase')} -> {args.to}")
    if result.reason.startswith("waived:"):
        print(result.reason)
    try:
        from _pipeline_log import append_receipt

        append_receipt(
            workspace,
            phase=args.to,
            skill="article.py",
            artifact=args.to,
            status="advanced",
            advance_exit_code=0,
            waive_reason=args.waive,
        )
    except Exception as exc:  # noqa: BLE001 - receipts are advisory, lifecycle already advanced
        print(f"warning: pipeline receipt not written ({exc})", file=sys.stderr)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    workspace = workspace_path(root, args.slug)
    try:
        article = migrate(load_article(workspace))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    current = str(article.get("currentPhase", ""))
    track = str(article.get("track", "full"))
    print(f"slug: {args.slug}")
    print(f"phase: {current}")
    print(f"track: {track}")
    next_phases = sorted(TRANSITIONS.get(current, set()), key=lambda item: PHASES.index(item))
    if next_phases:
        print("next:")
        for phase in next_phases:
            result = can_transition(article, phase, workspace)
            suffix = "ok" if result.ok else f"blocked: {result.reason}"
            print(f"  - {phase}: {suffix}")
    else:
        print("next: none")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    articles_dir = root / "content" / "articles"
    if not articles_dir.exists():
        return 0
    for workspace in sorted(path for path in articles_dir.iterdir() if path.is_dir() and path.name != "_archive"):
        article_path = workspace / "article.json"
        if not article_path.exists():
            continue
        try:
            article = migrate(load_article(workspace))
        except ValueError:
            continue
        print(f"{workspace.name}\t{article.get('currentPhase')}\t{article.get('track')}")
    return 0


def cmd_finish(args: argparse.Namespace) -> int:
    args.to = "completed"
    return cmd_advance(args)


def cmd_archive(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    source = workspace_path(root, args.slug)
    target = root / "content" / "articles" / "_archive" / args.slug
    if target.exists() and not source.exists():
        print(target)
        return 0
    if not source.exists():
        print(f"{source}: workspace does not exist", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        print(f"{target}: archive target already exists", file=sys.stderr)
        return 1
    shutil.move(str(source), str(target))
    print(target)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    try:
        from doctor import diagnose, render_report
        from install_session_hook import HARNESS_CONFIG
    except ImportError as exc:
        # doctor depends on installer-side modules that ship only in the source
        # scripts dir, not the project-local runtime copy. Run it from source.
        print(f"error: doctor is unavailable here ({exc}); run article.py from the skill's source scripts dir.", file=sys.stderr)
        return 1

    harnesses = sorted(HARNESS_CONFIG) if args.harness == "all" else [args.harness]
    overall_ok = True
    for name in harnesses:
        diagnosis = diagnose(root, name)
        print(render_report(diagnosis))
        overall_ok = overall_ok and diagnosis.ok
    return 0 if overall_ok else 1


def cmd_link(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    workspace = workspace_path(root, args.slug)
    try:
        article = migrate(load_article(workspace))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    article["series"] = args.series
    article["updatedAt"] = now_iso()
    save_article(workspace, article)
    print(f"{args.slug}: series={args.series}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage article lifecycle state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create an article workspace.")
    create.add_argument("title", help="Working article title.")
    create.add_argument("--slug", help="Lowercase kebab-case article slug. Defaults to slugified title.")
    create.add_argument("--root", default=".", help="Project root where content/articles lives.")
    create.add_argument("--type", choices=VALID_ARTICLE_TYPES, default="blog", help="Article type.")
    create.add_argument("--track", choices=["full", "lightweight"], default="full")
    create.add_argument("--harness", choices=["claude", "codex", "all"], default="claude")
    create.add_argument(
        "--no-hooks",
        action="store_true",
        help="Opt out of the hard gate: create the workspace without installing session/gate hooks.",
    )
    create.set_defaults(func=cmd_create)

    advance = subparsers.add_parser("advance", help="Advance to a lifecycle phase.")
    advance.add_argument("--to", required=True, choices=PHASES)
    advance.add_argument("--root", default=".", help="Project root where content/articles lives.")
    advance.add_argument("--slug", required=True, help="Article slug.")
    advance.add_argument("--waive", help="Reason for waiving a failed lifecycle gate.")
    advance.set_defaults(func=cmd_advance)

    status = subparsers.add_parser("status", help="Show current lifecycle state.")
    status.add_argument("--root", default=".", help="Project root where content/articles lives.")
    status.add_argument("--slug", required=True, help="Article slug.")
    status.set_defaults(func=cmd_status)

    listing = subparsers.add_parser("list", help="List article workspaces.")
    listing.add_argument("--root", default=".", help="Project root where content/articles lives.")
    listing.set_defaults(func=cmd_list)

    finish = subparsers.add_parser("finish", help="Advance an article to completed.")
    finish.add_argument("--root", default=".", help="Project root where content/articles lives.")
    finish.add_argument("--slug", required=True, help="Article slug.")
    finish.add_argument("--waive", help="Reason for waiving a failed lifecycle gate.")
    finish.set_defaults(func=cmd_finish)

    archive = subparsers.add_parser("archive", help="Archive an article workspace.")
    archive.add_argument("--root", default=".", help="Project root where content/articles lives.")
    archive.add_argument("--slug", required=True, help="Article slug.")
    archive.set_defaults(func=cmd_archive)

    doctor = subparsers.add_parser("doctor", help="Verify runtime + hooks are installed for this project.")
    doctor.add_argument("--root", default=".", help="Project root where content/articles lives.")
    doctor.add_argument("--harness", choices=["claude", "codex", "all"], default="claude")
    doctor.set_defaults(func=cmd_doctor)

    link = subparsers.add_parser("link", help="Attach an article to a parent series slug.")
    link.add_argument("--root", default=".", help="Project root where content/articles lives.")
    link.add_argument("--slug", required=True, help="Article slug.")
    link.add_argument("--series", required=True, help="Parent series article slug.")
    link.set_defaults(func=cmd_link)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
