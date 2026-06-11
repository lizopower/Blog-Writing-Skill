---
name: seo-serp-strategist
description: Use when you need a SERP-grounded keyword and search-intent strategy (the seo_strategy layer) before research and outlining, for English-first B2B/technical SEO articles.
---

# SEO SERP Strategist

## English-First Mandate

This bundle is built primarily for **English** technical/B2B SEO content (外贸 / industrial export
audiences). Every default in this skill targets English:

- Default output language is **English**; Chinese is only a collaboration language with the author.
- Default `target_market.locale` is an **English market** (e.g. `en-US`, `en-GB`, `en-AU`).
- All length thresholds (meta title ≤ 60, meta description ≤ 155) and slug rules assume English.
- A non-English target market must be **explicitly declared by the author**. Never infer an English
  market's SERP from a Chinese-environment search — locale and language drive completely different results.

## Overview

Act as an **SEO strategist** who turns an English keyword or topic into a SERP-grounded strategy. You
analyze the live search results for the target keyword and market, then produce a structured
`seo_strategy` object that downstream stages consume:

- `tech-article-architect` uses `search_intent`, `content_gaps`, and `paa_questions` to shape the H structure.
- `on-page-seo-finalizer` uses `on_page_recommendations` as **advisory seeds** (not final values).
- `tech-research` may use `content_gaps` to prioritize what evidence to gather.

You produce **strategy**, not article prose and not technical facts.

## Required Dependency: Tavily (hard prerequisite)

SERP analysis requires **live** data. You must use Tavily for real search results; never reconstruct a
SERP from model memory — SERP data is time- and locale-sensitive, and a fabricated SERP is worse than none.

Follow `standards/tavily_research_engine.md` for install/auth/preflight. If Tavily is unavailable, **stop**
and ask the author to install/authenticate it. Do not fall back to generic guessing.

On Windows, follow the standard's output discipline: Tavily CLI SERP/search/extract
commands must write JSON/raw output to a file with `-o` (for example under
`content/articles/<slug>/research/` or `.trellis-writing/research/`) instead of
printing non-ASCII JSON to stdout. Read the file after the command succeeds.

## Boundaries (what this skill must NOT do)

- **No technical facts.** SERP competitors are used only to read intent, content format, and structure
  gaps. Any technical claim, number, standard, or performance figure must still come from `tech-research`
  and live in `key_claims`. Never treat a competitor page as a factual source.
- **No static keyword lists in the bundle.** The keyword list belongs to the article's `context_pack`,
  never to this skill's files or examples. Keywords change with product, country, language, and time.
- **No outline writing.** You hand constraints to `tech-article-architect`; you do not author H2/H3 bodies.
- **Independent from `audience-pain-point-research`.** That skill mines social platforms for user language;
  this skill analyzes search competition and intent. They are complementary inputs to the same article but
  are separate skills with separate contracts. Do not merge them.

## Input Parameters

### Required
- **primary_topic_or_keyword** (string): The English seed keyword or topic.

### Optional
- **target_market** (object): `{ country, language, locale }`. Defaults to `{ language: "en", locale: "en-US" }`.
- **device** (`desktop` | `mobile` | `unknown`): Defaults to `desktop`.
- **secondary_keyword_seeds** (string[]): Author-supplied candidates to validate against the SERP.

## Procedure

1. **Preflight Tavily** (per the standard). Stop and ask if unavailable.
2. **Confirm market.** Resolve `target_market`. If the author wants a non-English market, require an explicit
   declaration and record it; otherwise default to English.
3. **Run live SERP queries** for the primary keyword (and seeds) scoped to the market. Capture the top
   competitors, SERP features, People-Also-Ask, and related queries.
4. **Classify intent.** Pick the primary `search_intent`; B2B queries are frequently mixed, so record any
   additional intents in `secondary_intents` and an optional `intent_confidence` (0–1). Do not force a single bucket.
5. **Analyze competitors structurally.** For each top result record `rank`, `url`, `title`, `content_type`,
   `strengths`, `weaknesses`. Derive `content_gaps` (what no competitor covers well) and `must_answer` items.
6. **Draft advisory on-page seeds** in `on_page_recommendations`: a candidate `meta_title` (≤ 60),
   `meta_description` (≤ 155), kebab-case `slug` containing the keyword, and image-alt requirements. Mark these
   clearly as advisory — `on-page-seo-finalizer` owns the final values.
7. **Record freshness.** Always set `serp_analysis.checked_at`; optionally set `serp_freshness_policy`
   (`max_age_days`, `on_stale`). Stale SERP data must not silently flow downstream.
8. **Optionally record metrics** in `keyword_metrics` (search_volume, difficulty, cpc, source) when available.
   These are optional — Tavily may not provide them, and the author can fill them manually.

## Output Contract

Emit a `seo_strategy` object conforming to `schemas/context_pack_schema.json` (v2.3.0). It is merged into the
`context_pack` by `tech-blog-orchestrator` (which performs no SEO analysis of its own — it only carries this
object through). Required keys: `target_keyword`, `search_intent`, `target_market` (with `locale`), and
`serp_analysis` (with `checked_at` and structured `competitors`).

Run the validator after producing the object:

```bash
python skills/tech-blog-orchestrator/scripts/validate_context_pack.py <context_pack.json>
```

## Handoff

Next stage: `tech-research` (evidence for `key_claims`, optionally guided by `content_gaps`), then
`tech-blog-orchestrator` to assemble the `context_pack`.
