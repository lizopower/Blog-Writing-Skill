# SEO SERP Strategist Skill

## Overview

The front-of-pipeline SEO strategy layer for **English-first** technical/B2B articles. It turns an English
keyword or topic into a SERP-grounded `seo_strategy` object that constrains the H structure (architect) and
seeds on-page metadata (finalizer).

**Core principle**: live SERP data (Tavily) + structured intent/competitor analysis — never fabricated SERPs,
never technical facts, never static keyword lists baked into the bundle.

## Position in the Pipeline

```
blog-brainstorm
  → seo-serp-strategist   ← this skill (produces seo_strategy)
  → tech-research / audience-pain-point-research / tech-file-parser
  → tech-blog-orchestrator (carries seo_strategy into context_pack; no SEO analysis)
  → data-validator
  → grill-me
  → tech-article-architect (consumes search_intent / content_gaps / paa_questions)
  → tech-visualization-generator
  → tech-blog-writer
  → fact-checker
  → on-page-seo-finalizer (finalizes meta/slug into top-level seo_finalization)
  → content-taste-advisor
```

## Relationship to `audience-pain-point-research`

Independent and complementary. Pain-point research mines social platforms for the audience's real language;
this skill analyzes search competition and intent on the SERP. Use both for a strong article, but they are
separate skills with separate output contracts.

## Output

A `seo_strategy` object per `schemas/context_pack_schema.json` (v2.3.0). Required: `target_keyword`,
`search_intent`, `target_market.locale`, `serp_analysis.checked_at`, structured `serp_analysis.competitors`.
On-page values produced here are **advisory only**; `on-page-seo-finalizer` owns the final values.

## Dependency

Requires Tavily (hard prerequisite). See `standards/tavily_research_engine.md`.
