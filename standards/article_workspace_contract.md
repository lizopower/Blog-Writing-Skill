# Article Workspace Contract

This contract gives each technical/B2B article a Trellis-like project-local workspace so writing work can be paused, resumed, checked, and improved over time.

## Default Location

Create article workspaces under the user's current project:

```text
content/articles/<slug>/
```

Use a lowercase kebab-case slug derived from the working title or topic.

## Required Skeleton

Create the full skeleton up front:

```text
content/articles/<slug>/
  article.json
  brief.md
  research/
  sources.jsonl
  context_pack.json
  strategy.md
  outline.md
  draft.md
  fact_check.md
  editorial_review.md
  finish.md
```

Do not overwrite existing files. If a workspace already exists, inspect `article.json` and continue from its current phase.

## Scaffold and Validation Scripts

When using this bundle from a checked-out repository, prefer the scripts provided by `blog-brainstorm`:

```bash
python skills/blog-brainstorm/scripts/create_article_workspace.py "<Working Title>" --slug <slug> --root <project-root>
python skills/blog-brainstorm/scripts/validate_article_workspace.py <project-root>/content/articles/<slug>
```

The scaffold script creates the full skeleton and does not overwrite existing files. The validator checks required artifacts, `article.json`, `context_pack.json`, and lifecycle phase validity.

## State File

`article.json` is the machine-readable state file:

```json
{
  "id": "article-slug",
  "title": "Working title",
  "status": "brainstorming",
  "currentPhase": "briefing",
  "nextAction": "clarify audience and angle",
  "articleType": "blog",
  "businessGoal": "",
  "audience": [],
  "primaryKeyword": "",
  "angle": "",
  "createdAt": "ISO-8601 timestamp",
  "updatedAt": "ISO-8601 timestamp"
}
```

Update `currentPhase` and `nextAction` after each meaningful step.

## Lifecycle

```text
brainstorming
brief_confirmed
research_planning
context_building
strategy_pressure_test
outlining
drafting
fact_checking
editorial_review
completed
```

## File Responsibilities

- `brief.md`: human-readable article strategy and requirements.
- `research/`: persistent research notes, one file per topic/source cluster.
- `sources.jsonl`: source inventory, one JSON object per source.
- `context_pack.json`: structured source-backed claims, glossary, data, tables, and risk notes.
- `strategy.md`: angle decisions, pressure-test summary, rejected angles, evidence gaps.
- `outline.md`: article structure and section plan.
- `draft.md`: article body.
- `fact_check.md`: factual, numerical, unit, and source-traceability review.
- `editorial_review.md`: taste, differentiation, clarity, SEO, CTA, and publishability review.
- `finish.md`: final summary, lessons learned, reusable patterns, and standards update candidates.

## Phase Gates

Each phase should leave a durable artifact before moving forward:

| Phase | Required Artifact | Gate |
|---|---|---|
| brainstorming | `brief.md`, `article.json` | Goal, audience, pain, angle, CTA, and success criteria are explicit |
| research_planning | `research/` plan or notes | Research questions and source targets are clear |
| context_building | `context_pack.json` | Claims and data have traceable sources |
| strategy_pressure_test | `strategy.md` | Key assumptions and evidence gaps are resolved or flagged |
| outlining | `outline.md` | Structure maps to reader decision path |
| drafting | `draft.md` | Draft uses only supported claims |
| fact_checking | `fact_check.md` | Critical fact issues are resolved or flagged |
| editorial_review | `editorial_review.md` | Taste dimensions scored; `Publishability: PASS` recorded |
| completed | `editorial_review.md` | Final gate passed with `Publishability: PASS` |

`finish.md` is a post-completion learning artifact. Capture lessons there when useful; it is not required by the `completed` lifecycle gate.

## editorial_review.md required sections

When `content-taste-advisor` completes the editorial phase, `editorial_review.md` must include:

1. **Seven-dimension scores** (topic, angle, structure, evidence use, tone, differentiation, publishability) — each with a brief rationale.
2. **Publishability:** `PASS` or `FAIL` on its own line (lifecycle gate requires `Publishability: PASS` before `completed`).
3. **Top revisions** (if any) — concrete edits still recommended before external publish.

## Finish-Time Learning

At the end of each article, write `finish.md` with:

- What worked in the topic/angle/evidence strategy.
- Claims, terms, or explanations worth reusing.
- Sources that were trustworthy or weak.
- Standards that should be updated.
- Follow-up article ideas.
