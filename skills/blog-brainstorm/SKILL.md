---
name: blog-brainstorm
description: Use when the user has a vague or early technical/B2B blog, article, white paper, or thought-leadership idea and needs a Trellis-like brainstorm that creates an article workspace, recommends direction, asks one question at a time, and converges to an executable brief.
---

# Blog Brainstorm Skill

Create a Trellis-like article workspace, then turn an early content idea into an executable brief through proactive, one-question-at-a-time strategy discovery.

## When to Use This Skill

Use when the user:
- Has a vague topic, keyword, product, audience, competitor, or content idea.
- Says "brainstorm", "头脑风暴", "帮我想选题", "帮我定方向", "内容策略", or similar.
- Wants to decide whether an article is worth writing before research or drafting.
- Needs a project-local workspace for a technical/B2B article.

Use `grill-me` instead when the user already has a clear brief, outline, or plan and wants it pressure-tested.

## Not For / Boundaries

- Do not write the article body.
- Do not invent facts, market claims, sources, or audience evidence.
- Do not skip workspace creation unless the user explicitly asks not to create files.
- Do not ask multiple questions at once.
- Do not proceed into research or drafting automatically after brainstorm convergence; ask the user to choose.

## Article Workspace Contract

Default workspace path:

```text
content/articles/<slug>/
```

Create the full skeleton immediately:

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

If `content/articles/<slug>/` already exists, inspect it and continue from `article.json.currentPhase` instead of overwriting existing work. For a resumed or older project (created before this version, or with `--no-hooks`), first verify the runtime and hooks are in place — the `create` gate only fires on first creation:

```bash
python skills/blog-brainstorm/scripts/article.py doctor --root <project-root>
```

If it reports problems, run `init.py --root <project-root>` to (re)install the runtime and hooks before continuing. `init.py --check` is the equivalent read-only probe.

## Script-First Workspace Creation

When local scripts are available, create the workspace with:

```bash
python skills/blog-brainstorm/scripts/article.py create "<Working Title>" --slug <slug> --root <project-root>
```

Then validate it with:

```bash
python skills/blog-brainstorm/scripts/validate_article_workspace.py <project-root>/content/articles/<slug>
```

Rules:
- Prefer the script over manual file creation.
- `article.py create` is a hard gate: it installs the session-context hooks (SessionStart + lifecycle gate + per-turn breadcrumb) before creating the workspace, and **fails without creating the workspace** if hook installation fails (runtime files under `.trellis-writing/` may already be written and are reused on retry). Fix the reported cause and retry — do not fall back to manual creation, which would produce a workspace with no context injection. Only pass `--no-hooks` to deliberately opt out (e.g. CI), and expect no workflow injection in that project.
- If the script is unavailable, create the same skeleton manually and then inspect every required artifact.
- Never overwrite existing files; continue from the existing workspace state.
- Treat validation failure as a blocker before continuing the brainstorm.
- Do not edit `article.json.currentPhase` directly. Phase changes must use `article.py advance`; if it exits non-zero, stop and report the reason.

## article.json

Create or update `article.json` as the state file:

```json
{
  "id": "article-slug",
  "title": "Working title",
  "status": "brainstorming",
  "currentPhase": "brainstorming",
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

Valid phases:

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

## Brainstorm Loop

Use a "recommend first, let the user push back" style.

For each step:
1. Inspect existing context, files, or workspace state first.
2. State the current best recommendation and why.
3. Ask exactly one question that lets the user confirm, reject, or adjust the recommendation.
4. Update `article.json` and `brief.md` after the user's answer.

Default question sequence:

```text
business goal
target audience
reader pain
article angle
evidence available
desired conversion / CTA
scope boundary
success criteria
```

## brief.md

Keep `brief.md` as the human-readable source of truth:

```markdown
# <Working Title>

## Business Goal

## Target Audience

## Reader Pain

## Recommended Angle

## Evidence Available

## Claims To Prove

## Scope Boundary

## CTA

## Success Criteria

## Open Questions

## Next Step
```

## Completion Gate

When the brainstorm converges, present exactly two button-style options and no extra choices:

```text
[Continue to research / workflow]
[Stop at confirmed brief]
```

If the user continues, update `article.json`:

```bash
python skills/blog-brainstorm/scripts/article.py advance --to brief_confirmed --slug <slug> --root <project-root>
python skills/blog-brainstorm/scripts/article.py advance --to research_planning --slug <slug> --root <project-root>
```

If the user stops, update `article.json`:

```bash
python skills/blog-brainstorm/scripts/article.py advance --to brief_confirmed --slug <slug> --root <project-root>
```

After advancing the phase, run workspace validation again when the validator script is available. If `article.py advance` fails, do not rewrite `article.json` by hand; fix the missing gate artifact or ask the user whether to use `--waive "<reason>"`.

## Handoff

- Continue to `tech-research` or `audience-pain-point-research` when the brief needs evidence.
- Continue to `tech-blog-orchestrator` when source material should become a context_pack.
- Continue to `grill-me` when the brief exists but the strategy needs pressure-testing.
- Continue to `blog-writing-workflow` when the user wants the full article pipeline.
