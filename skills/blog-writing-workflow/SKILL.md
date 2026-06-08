---
name: blog-writing-workflow
description: Use when the user requests a full technical/B2B blog or article end-to-end, from topic/files through research, context pack, strategy pressure test, outline, draft, and fact-check.
---

# Blog Writing Workflow

Run the complete technical/B2B article pipeline. This skill is an orchestrator: it coordinates sub-skills and quality gates, but does not manually write article body content.

## When to Use This Skill

Use immediately when the user asks for:
- "写博客", "写文章", "技术文章", "write a blog", "write an article", or similar.
- A complete article from a topic and/or uploaded files.
- Research-to-draft, source-backed writing, or full article QA.

If the request is still vague or strategic and no article workspace exists, invoke `blog-brainstorm` first.

## Not For / Boundaries

- Do not use for quick snippets, social posts, or lightweight copy edits.
- Do not write unsupported article content manually; delegate drafting to `tech-blog-writer`.
- Do not invent statistics, claims, charts, case studies, or citations.
- Do not proceed with online research unless Tavily preflight passes.

## Required Dependency: Tavily

Before any topic research, audience research, source discovery, extraction, or claim verification beyond local files, confirm:

```bash
tvly --status
```

Tavily requirements:
- Tavily skills from `https://github.com/tavily-ai/skills` are installed or available.
- Tavily CLI `tvly` is installed.
- Authentication is configured via `tvly login` or `TAVILY_API_KEY`.

If Tavily is unavailable, stop and ask the user to install/authenticate Tavily. Do not silently fall back to generic web search.

Local file-only parsing may run without Tavily until online research or external claim verification is requested.

## Article Workspace Awareness

Before running the workflow, check for:

```text
content/articles/<slug>/
```

If present:
- Treat `article.json` as workflow state.
- Treat `brief.md` as strategy source of truth.
- Read existing `research/`, `sources.jsonl`, `context_pack.json`, `strategy.md`, `outline.md`, `draft.md`, `fact_check.md`, and `editorial_review.md`.
- Continue from `article.json.currentPhase` when possible.
- Do not overwrite artifacts without user confirmation.

If absent and the user wants ideation or strategy discovery, invoke `blog-brainstorm`.

## 8-Step Pipeline

1. `audience-pain-point-research` [optional]
   Run for audience research, SEO/search-intent strategy, or unfamiliar topics.

2. `tech-blog-orchestrator` [required]
   Prepare Context Pack v2.1.0 from topic research and/or local files.

3. `data-validator` [required]
   Validate Context Pack schema, completeness, sources, units, and consistency.

4. `grill-me` [conditional / mandatory if requested]
   Pressure-test strategy before outlining.

5. `tech-article-architect` [required]
   Build outline and section plan from validated Context Pack and strategy summary.

6. `tech-visualization-generator` [conditional]
   Create visualization manifest only when structured data supports it.

7. `tech-blog-writer` [required]
   Draft the article from outline, Context Pack, charts manifest, and strategy summary.

8. `fact-checker` [required]
   Verify factual claims, numbers, units, logic, and source traceability.

## Mandatory `grill-me` Triggers

Invoke `grill-me` before outlining when any of these applies:
- User says "grill me", "追问我", "拷问我", "challenge this", "pressure-test", or "stress-test".
- Data validation warnings affect thesis, evidence, scope, or claims.
- Multiple plausible angles remain.
- Topic is high-risk, high-competition, strategically vague, or under-evidenced.

If `grill-me` finds missing evidence, return to `tech-research`, `audience-pain-point-research`, or `tech-blog-orchestrator` before continuing.

## Context Pack Contract

Use Context Pack v2.1.0. Validate against:

```text
schemas/context_pack_schema.json
skills/tech-blog-orchestrator/scripts/validate_context_pack.py
```

Downstream writing and fact-checking must use only source-backed claims from the Context Pack unless the user explicitly provides new source material.

## Execution Notes

- Pass outputs forward without silently reshaping them.
- Stop on failed validation unless the user explicitly accepts the risk.
- Skip visualization when data is insufficient; do not invent chart values.
- Present validation and fact-check warnings clearly in the final report.

## References

- `references/execution-details.md`: detailed step-by-step execution.
- `references/failure-recovery.md`: failure handling.
- `references/data-flow.md`: artifact handoffs.
- `references/output-format.md`: final report format.

## Success Criteria

- Required steps complete or failures are explicitly reported.
- Context Pack validates or warnings are disclosed.
- Article word count is within target tolerance when specified.
- Quantitative claims are source-backed.
- Fact check is completed and issues are documented.
- Final output includes article, quality reports, and next step.

## Metadata

- Updated: 2026-06-08
- Industry: Domain-agnostic
- Version: governed by the release version in the manifests (see `VERSIONING.md`).
