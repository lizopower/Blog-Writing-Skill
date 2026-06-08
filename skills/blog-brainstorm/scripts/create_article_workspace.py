#!/usr/bin/env python3
"""Create a Blog-Writing-Skill article workspace skeleton."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_FILES = {
    "brief.md": "# {title}\n\n## Business Goal\n\n## Target Audience\n\n## Reader Pain\n\n## Recommended Angle\n\n## Evidence Available\n\n## Claims To Prove\n\n## Scope Boundary\n\n## CTA\n\n## Success Criteria\n\n## Open Questions\n\n## Next Step\n",
    "sources.jsonl": "",
    "context_pack.json": "{\n  \"version\": \"2.1.0\",\n  \"generated_at\": \"\",\n  \"topic\": \"\",\n  \"audience\": [],\n  \"industry_context\": {\n    \"industry\": \"\",\n    \"market_segment\": \"\",\n    \"core_advantage\": \"\"\n  },\n  \"key_claims\": [],\n  \"extracted_tables\": [],\n  \"glossary\": [],\n  \"risk_notes\": [],\n  \"research_summary\": {\n    \"sources_count\": 0,\n    \"last_updated\": \"\",\n    \"key_findings\": []\n  },\n  \"file_summary\": {\n    \"files_processed\": [],\n    \"total_pages\": 0,\n    \"extraction_notes\": []\n  }\n}\n",
    "strategy.md": "# Strategy Pressure Test\n\n## Resolved Decisions\n\n## Rejected Angles\n\n## Evidence Gaps\n\n## Next Step\n",
    "outline.md": "# Outline\n\n",
    "draft.md": "# Draft\n\n",
    "fact_check.md": "# Fact Check\n\n",
    "editorial_review.md": "# Editorial Review\n\n",
    "finish.md": "# Finish\n\n## What Worked\n\n## Reusable Patterns\n\n## Weak Sources\n\n## Standards Update Candidates\n\n## Follow-Up Ideas\n",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "untitled-article"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create_workspace(root: Path, slug: str, title: str, article_type: str) -> Path:
    workspace = root / "content" / "articles" / slug
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "research").mkdir(exist_ok=True)

    timestamp = now_iso()
    article_json = workspace / "article.json"
    if not article_json.exists():
        article_json.write_text(
            json.dumps(
                {
                    "id": slug,
                    "title": title,
                    "status": "brainstorming",
                    "currentPhase": "brainstorming",
                    "nextAction": "clarify audience and angle",
                    "articleType": article_type,
                    "businessGoal": "",
                    "audience": [],
                    "primaryKeyword": "",
                    "angle": "",
                    "createdAt": timestamp,
                    "updatedAt": timestamp,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    for relative_path, template in REQUIRED_FILES.items():
        target = workspace / relative_path
        if not target.exists():
            target.write_text(template.replace("{title}", title), encoding="utf-8")

    return workspace


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an article workspace skeleton.")
    parser.add_argument("title", help="Working article title.")
    parser.add_argument("--slug", help="Lowercase kebab-case article slug. Defaults to slugified title.")
    parser.add_argument("--root", default=".", help="Project root where content/articles will be created.")
    parser.add_argument("--type", default="blog", help="Article type, e.g. blog, white-paper, guide.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    slug = args.slug or slugify(args.title)
    workspace = create_workspace(root, slug, args.title, args.type)
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
