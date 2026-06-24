# Stage → Prompt → Artifacts

| Phase | Prompt file | Read artifacts | Write artifact | Sub-skill |
|-------|-------------|----------------|----------------|-----------|
| brainstorming | brainstorm.md | brief.md | brief.md | blog-brainstorm |
| research_planning | research_plan.md | brief.md, sources.jsonl | research/* | tech-research |
| context_building | research_plan.md | brief.md, sources.jsonl | context_pack.json | tech-blog-orchestrator |
| strategy_pressure_test | brainstorm.md | context_pack.json, strategy.md | strategy.md | grill-me |
| outlining | outline.md | brief.md, context_pack.json, strategy.md, genre_conventions.json | outline.md | tech-article-architect |
| drafting | draft.md | outline.md, context_pack.json, strategy.md | draft.md | tech-blog-writer |
| fact_checking | fact_check.md | draft.md, context_pack.json | fact_check.md | fact-checker |
| editorial_review | editorial_review.md | draft.md, fact_check.md | editorial_review.md | content-taste-advisor |

`bws run --slug <slug> --stage <phase>` loads the prompt file from this directory and upstream artifacts into `content/articles/<slug>/stage/<phase>_context.txt`.

Bundle path: `templates/prompts/` (relative to Blog-Writing-Skill repo root).
