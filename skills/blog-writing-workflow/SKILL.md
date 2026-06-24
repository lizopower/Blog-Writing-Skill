---
name: blog-writing-workflow
description: Use when the user requests a full technical/B2B blog or article end-to-end, from topic/files through research, context pack, strategy pressure test, outline, draft, and fact-check.
---

# Blog Writing Workflow

Run the complete technical/B2B article pipeline. This skill is an orchestrator: it coordinates sub-skills and quality gates, but does not manually write article body content.

## Default: Full Pipeline — No Skipping

Run **every step by default.** The core evidence chain is mandatory and must NEVER be collapsed or jumped over on your own initiative:

> **2 orchestrate/research → 3 validate → 5 outline → 7 draft → 8 fact-check**

Rules:
- **Execution contract**: this workflow is not a style reference. It is a production pipeline with evidence-gathering, validation, outline, drafting, and fact-check gates; treating it as style guidance skips those gates and produces unsupported output.
- If invoked, produce or continue the concrete workflow artifacts (context_pack, validation report, outline, draft, fact-check report, etc.) for each required stage, or stop and explain which dependency/user waiver prevents completion.
- **Do not jump straight to drafting (step 7 / `tech-blog-writer`).** A draft produced without an upstream validated context_pack and an outline is a failure, even if the user only said "write an article about X."
- **Research momentum is not a waiver.** Tavily search/extract results, deep-research notes, source lists, and "I already understand the structure" are raw material only. They are not a Context Pack, not validation, not an outline, and not permission to draft.
- **Rich input is not a waiver.** A complete-looking user brief with title, audience, keywords, source links, pasted notes, desired structure, CTA, tone, and word count is still raw material for the workflow. It is not a validated Context Pack, not an approved outline, and not permission to draft directly.
- **Pre-draft gate**: before writing any article body text, verify that:
  1. Context Pack v2.3.0 exists,
  2. `data-validator` has passed or returned warnings explicitly accepted by the user,
  3. an outline from `tech-article-architect` exists,
  4. any skipped upstream stage has an explicit user waiver.
  If any item is missing, stop and produce a blocked workflow receipt instead of drafting. When an article workspace exists, this gate is enforced mechanically: `article.py advance --to drafting` must succeed first (see Lifecycle State Binding).
- **Workflow receipt after every stage**: after each completed, skipped, or blocked stage, record the stage name, status, artifact path/name, and next allowed skill. Never keep stage outputs only in working memory.
- The user only naming a topic, audience, word count, or keyword density is **not** a request to skip steps. Run the whole pipeline.
- Skip a step **only** on an explicit user request — "直接写" / "跳过研究" / "不用查资料" / "skip research" / "just draft" / "no fact-check". When you skip on request, state which steps you skipped.
- Conditional steps (1 audience research, 4 grill-me, 6 visualization) may be skipped when genuinely inapplicable, but **announce each skip and why** — never skip silently. `grill-me` is mandatory when the user asks to be grilled/pressure-tested.
- A user disabling or declining CCG, project management, task archival, or any other process framework, whether by user instruction or configuration, is not a waiver of this workflow. Continue the Blog-Writing-Skill pipeline unless they explicitly waive Blog-Writing-Skill stages.

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

If absent for a full-pipeline request, create one so lifecycle gates are active:

```bash
python skills/blog-brainstorm/scripts/article.py create "<working title>" --root <project-root>
```

If absent and the user wants ideation or strategy discovery, invoke `blog-brainstorm`.

## Lifecycle State Binding (hard gates)

When an article workspace exists, `article.json` — enforced by the lifecycle state machine, not by this document — is the single source of truth for pipeline position. Bind every stage to it. The `article.py` CLI lives at `skills/blog-brainstorm/scripts/article.py` in the bundle and is mirrored to `<project-root>/.trellis-writing/runtime/scripts/article.py`.

- **Stage start**: run `python article.py status --slug <slug> --root <project-root>`. Only do work for the current phase or a `next:` phase marked `ok`.
- **Stage end**: run `python article.py advance --to <phase> --slug <slug> --root <project-root>`. The artifact gate verifies the stage output file; a non-zero exit means the stage is NOT done — fix the artifact or stop with a blocked receipt. Never hand-edit `article.json` phase fields.
- **Receipts are script output**: each workflow receipt row must quote the `advance` result line (e.g. `demo: context_building -> strategy_pressure_test`). A receipt for a workspace-backed stage without a successful `advance` is invalid.
- **Waivers**: pass `--waive "<reason>"` only after explicit user approval, quoting the user's words.

Step-to-phase mapping:

| After completing | Advance to |
|---|---|
| research plan agreed | `research_planning` |
| sources gathered (`sources.jsonl` non-empty) | `context_building` |
| steps 2–3: Context Pack built and validated | `strategy_pressure_test` |
| step 4 (or default strategy): `strategy.md` Resolved Decisions filled | `outlining` |
| step 5: outline approved | `drafting` |
| step 7: draft complete | `fact_checking` |
| step 8: fact-check report written | `editorial_review` |
| step 9 (optional SEO): `seo_finalization` written | `editorial_review` |
| step 10: editorial review + `Publishability: PASS` | `completed` |

A PreToolUse hook (installed by `init.py` and `article.py create`) independently denies writes to `outline.md`, `draft.md`, `fact_check.md`, and `editorial_review.md` before their phase. If a write is denied, do not work around it (no renamed files, no shell redirection, no inline article text in chat); run the missing upstream stages and advance the phase instead.

## Controlled Fan-Out Boundary

The main session is the only orchestrator, canonical artifact writer, and phase advancer. Do not use spawned workers to advance phases, make strategy decisions, write the outline, write the draft, or modify canonical lifecycle artifacts.

Spawned workers may be used only for scratch-only parallel work such as source discovery, research-note gathering, source credibility checks, fact-check shard audits, visualization/material suggestions, or editorial review by separate dimensions. Give each worker a narrow task prompt and the minimum context needed; do not rely on lifecycle hook injection for sub-agents. Merge worker outputs into canonical artifacts only from the main session after validation.

## Pipeline (core 8 steps + optional SEO layers)

1. `audience-pain-point-research` [optional]
   Run for audience research or unfamiliar topics (social-platform user language).

1b. `seo-serp-strategist` [optional · SEO front layer]
   For English SEO articles, produce the `seo_strategy` (SERP-grounded keywords, search intent, competitor
   gaps, PAA, advisory on-page seeds) before research/outline. Independent from step 1. Requires live Tavily SERP.

2. `tech-blog-orchestrator` [required]
   Prepare Context Pack v2.3.0 from topic research and/or local files. If a `seo_strategy` exists, carry it
   through unchanged (orchestrator performs no SEO analysis).

3. `data-validator` [required]
   Validate Context Pack schema, completeness, sources, units, and consistency.

4. `grill-me` [conditional / mandatory if requested]
   Pressure-test strategy before outlining. This is human-gated: do not let approval/autonomy modes answer on the user's behalf or skip the wait for an explicit user reply.

5. `tech-article-architect` [required]
   Build outline and section plan from validated Context Pack and strategy summary.

6. `tech-visualization-generator` [conditional]
   Create visualization manifest only when structured data supports it.

7. `tech-blog-writer` [required]
   Draft the article from outline, Context Pack, charts manifest, and strategy summary.

7b. `normalize_draft` [optional]
   Run `normalize_draft.py --workspace --check-only` (or `--apply` after user confirmation) between draft and fact-check.

8. `fact-checker` [required]
   Verify factual claims, numbers, units, logic, and source traceability.

9. `on-page-seo-finalizer` [conditional · SEO back layer]
   After fact-check, run final on-page SEO QA (meta, slug, alt, internal links, tables, FAQ schema) and write
   the sole final on-page values into top-level `seo_finalization`. Edits are limited to the metadata layer and
   must not touch `glossary` terms. Metadata-only changes do **not** re-run `fact-checker`; a rare body-fact
   change re-runs it at most once, else stop and ask the author. Run when `seo_strategy` is present or the user
   asks for on-page SEO finishing.

10. `content-taste-advisor` [required · editorial_review phase]
   After fact-check (and optional on-page SEO), run the seven-dimension taste review.
   Write `editorial_review.md` with dimension scores and `Publishability: PASS` or `FAIL`.
   When publishability passes, advance lifecycle state to `completed` (or use `article.py finish`, which advances to `completed`).

## Mandatory `grill-me` Triggers

Invoke `grill-me` before outlining when any of these applies:
- User says "grill me", "追问我", "拷问我", "challenge this", "pressure-test", or "stress-test".
- Data validation warnings affect thesis, evidence, scope, or claims.
- Multiple plausible angles remain.
- Topic is high-risk, high-competition, strategically vague, or under-evidenced.

If `grill-me` finds missing evidence, return to `tech-research`, `audience-pain-point-research`, or `tech-blog-orchestrator` before continuing.

During `grill-me`, the assistant's recommended answer is not user approval. Wait for the user's explicit answer unless they requested autopilot/no-interaction mode.

## Context Pack Contract

Use Context Pack v2.3.0. Validate against:

```text
schemas/context_pack_schema.json
skills/tech-blog-orchestrator/scripts/validate_context_pack.py
```

Downstream writing and fact-checking must use only source-backed claims from the Context Pack unless the user explicitly provides new source material.

Before handoff to `tech-blog-writer`, confirm the Context Pack includes all available context:
- Topic, audience, industry, and core advantage
- Source-backed claims, tables, glossary, and risk notes
- Optional `style_exemplars` for voice and structure only
- Optional `core_offerings` for contextual, non-promotional product/service mentions
- Optional `author_experience_notes` for real stories, preferences, and expert commentary

## Execution Notes

- Pass outputs forward without silently reshaping them.
- Convert rich user input into workflow artifacts first. If the user provides title, audience, keywords, source links, pasted notes, desired structure, CTA, tone, or word count, preserve those details in the Context Pack/brief/outline path instead of treating them as permission to draft directly.
- Stop on failed validation unless the user explicitly accepts the risk.
- Skip visualization when data is insufficient; do not invent chart values.
- Present validation and fact-check warnings clearly in the final report.
- When the workflow is blocked before completion, produce a partial workflow receipt showing completed stages and the blocking stage.
- Never convert research notes directly into article body text. The only allowed path from research to prose is: research notes → Context Pack → validation → outline → `tech-blog-writer` draft → fact-check.
- Draft section by section through `tech-blog-writer`; for interactive work, pause after each major H2/H3 for user feedback.
- Treat user edits as project-level guardrails for the current workspace or article. Do not claim the model has permanently learned; persist reusable feedback only when the user wants a local style guide or guardrails update.
- At finish, review `finish.md` section `Standards Update Candidates`. For each reusable project-level rule the user accepts, persist it with:
  ```bash
  python skills/blog-brainstorm/scripts/spec.py add --title "<rule title>" --root <project-root>
  ```
  Provide the rule body on stdin or with `--from-file`. This writes only to `content/specs/`; never write project learnings back to the bundle `standards/` directory.

## References

- `references/execution-details.md`: detailed step-by-step execution.
- `references/failure-recovery.md`: failure handling.
- `references/data-flow.md`: artifact handoffs.
- `references/output-format.md`: final report format.

## Success Criteria

- Required steps complete or failures are explicitly reported.
- Final response includes the workflow receipt format from `references/output-format.md`: completed stages, artifact paths/names, skipped stages with explicit user waiver or inapplicability, blockers, and fact-check status.
- Context Pack validates or warnings are disclosed.
- Article word count is within target tolerance when specified.
- Quantitative claims are source-backed.
- Fact check is completed and issues are documented.
- Final output includes article, quality reports, and next step.

## Metadata

- Updated: 2026-06-11
- Industry: Domain-agnostic
- Version: governed by the release version in the manifests (see `VERSIONING.md`).
