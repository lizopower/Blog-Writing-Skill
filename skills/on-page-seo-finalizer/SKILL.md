---
name: on-page-seo-finalizer
description: Use after fact-check to run the final on-page SEO QA (meta, slug, alt, internal links, tables, schema) and write the sole final on-page values, for English-first articles.
---

# On-Page SEO Finalizer

## English-First Mandate

This bundle is built primarily for **English** technical/B2B SEO content. All default thresholds in this
skill assume English markets:

- Default output language is **English**; Chinese is only a collaboration language.
- `meta_title` ≤ **60** characters; `meta_description` ≤ **155** characters (English character counts).
- `slug` is kebab-case ASCII containing the target keyword.
- A non-English market must be **explicitly declared by the author**; otherwise apply English rules.

## Overview

Act as the **publish-readiness gate**. You run after `fact-checker` on an already-verified draft and perform
the final on-page SEO QA, then write the **single source of final on-page truth** into the top-level
`seo_finalization` object. You are the last technical SEO step before `content-taste-advisor`.

## Single Source of Final Truth (R-A2)

- `seo_strategy.on_page_recommendations` (from `seo-serp-strategist`) are **advisory seeds**, not final values.
- **You are the only writer of `seo_finalization`.** Adopt or override the advisory seeds, and record what you
  changed and why in `seo_finalization.overrides`. Never mutate `seo_strategy.on_page_recommendations`.
- Downstream consumers (writer, taste, humans, CMS) must read final on-page values from `seo_finalization`.

## Terminology Protection (R-C1) — hard rule

SEO optimization must never erode technical precision. B2B/industrial content depends on exact terms.

- Your edit authority is **limited to the metadata layer**: `meta_title`, `meta_description`, `slug`,
  image `alt`, figure captions, internal-link anchors, table/markdown formatting.
- You **must not** rewrite body technical parameters, numbers, standards, or comparison conclusions.
- Any edit that would touch a term in `context_pack.glossary` is **blocked**. Keep the glossary term exactly;
  adjust surrounding metadata phrasing instead. If SEO and a glossary term truly conflict, stop and ask the author.

## Fact-Check Loop (R-C2) — bounded

- Metadata-layer changes (the normal case) **do not** trigger a `fact-checker` re-run.
- Only if you must change body facts (should be extremely rare, and never via the metadata layer above) do you
  re-run `fact-checker` — **at most once**. If a conflict remains, STOP and request an author decision.
  Never enter an unbounded finalize↔fact-check loop.

## Checklist (English defaults)

- **meta_title**: ≤ 60 chars, contains the target keyword, reads naturally (no stuffing).
- **meta_description**: ≤ 155 chars, compelling, contains the keyword once.
- **slug**: short, kebab-case (lowercase, digits, single hyphens), contains the target keyword, no stop-word noise. No leading/trailing slash, no spaces, no uppercase — the validator rejects these.
- **H1**: exactly one; **H2/H3** align with `search_intent` and `secondary_intents`.
- **FAQ**: covers `serp_analysis.paa_questions`.
- **Image alt**: accurate and descriptive; no keyword stuffing.
- **Figure/table captions**: complete; tables are valid Markdown/CMS.
- **Internal links**: if a site inventory is provided, validate targets; otherwise emit placeholders with
  suggested anchor text (do not invent real internal URLs).
- **Schema (optional)**: emit JSON-LD FAQ schema when a FAQ section exists.

## Boundaries

- Not a fact source and not a fact checker — `fact-checker` owns facts.
- Does not generate charts or chart data — `tech-visualization-generator` owns visuals; you only check their
  alt/caption metadata.
- Does not rewrite the article's argument or core claims.

## Input / Output

**Input**: the fact-checked draft + the `context_pack` (with `seo_strategy` and `glossary`).

**Output**: a top-level `seo_finalization` object conforming to `schemas/context_pack_schema.json` (v2.3.0):
`meta_title`, `meta_description`, `slug`, `finalized_at` (required), plus optional `image_alt`,
`internal_links`, and `overrides`. Validate after writing:

```bash
python skills/tech-blog-orchestrator/scripts/validate_context_pack.py <context_pack.json>
```

## Handoff

Next stage: `content-taste-advisor` for the final editorial review.
