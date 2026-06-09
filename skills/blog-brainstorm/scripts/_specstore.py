#!/usr/bin/env python3
"""Pure helpers for project-local writing specs."""

from __future__ import annotations

import re
from dataclasses import dataclass


INDEX_TITLE = "# Project Writing Specs"


@dataclass(frozen=True)
class ParsedSpec:
    front_matter: dict[str, str]
    body: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "spec"


def render_spec(*, spec_id: str, title: str, scope: str, created_at: str, body: str) -> str:
    normalized_body = body.strip() + "\n" if body.strip() else "\n"
    return (
        "---\n"
        f"id: {spec_id}\n"
        f"title: {title}\n"
        f"scope: {scope or 'project'}\n"
        f"createdAt: {created_at}\n"
        "---\n\n"
        f"{normalized_body}"
    )


def parse_spec(markdown: str) -> ParsedSpec:
    if not markdown.startswith("---\n"):
        return ParsedSpec({}, markdown)
    end = markdown.find("\n---", 4)
    if end == -1:
        return ParsedSpec({}, markdown)
    raw_front_matter = markdown[4:end]
    body = markdown[end + len("\n---") :].lstrip("\n")
    front_matter: dict[str, str] = {}
    for line in raw_front_matter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip()
    return ParsedSpec(front_matter, body)


def render_index_line(slug: str, title: str, hook: str) -> str:
    line = f"- [{title}]({slug}.md)"
    if hook.strip():
        line += f" - {hook.strip()}"
    return line


def render_index(entries: list[tuple[str, str, str]]) -> str:
    lines = [
        INDEX_TITLE,
        "",
        "Project-local writing standards captured during article finish/review.",
        "",
    ]
    if entries:
        lines.extend(render_index_line(slug, title, hook) for slug, title, hook in entries)
    else:
        lines.append("_No project writing specs captured yet._")
    return "\n".join(lines).rstrip() + "\n"


def parse_index(markdown: str) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    pattern = re.compile(r"^-\s+\[(?P<title>[^\]]+)\]\((?P<slug>[^)]+)\)(?:\s+-\s+(?P<hook>.*))?$")
    for line in markdown.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        slug = match.group("slug").removesuffix(".md")
        entries.append((slug, match.group("title"), match.group("hook") or ""))
    return entries


def merge_index_entries(
    existing: list[tuple[str, str, str]],
    incoming: list[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    order: list[str] = []
    by_slug: dict[str, tuple[str, str, str]] = {}
    for entry in [*existing, *incoming]:
        slug = entry[0]
        if slug not in by_slug:
            order.append(slug)
        by_slug[slug] = entry
    return [by_slug[slug] for slug in order]
