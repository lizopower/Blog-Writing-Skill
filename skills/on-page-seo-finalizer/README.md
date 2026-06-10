# On-Page SEO Finalizer Skill

## Overview

The end-of-pipeline publish-readiness gate for **English-first** technical/B2B articles. Runs after
`fact-checker`, performs the final on-page SEO QA, and writes the **single source of final on-page truth**
into the top-level `seo_finalization` object.

**Core principle**: optimize the metadata layer only; never erode technical precision. Glossary terms are protected.

## Position in the Pipeline

```
... → tech-blog-writer → fact-checker
  → on-page-seo-finalizer   ← this skill (writes seo_finalization)
  → content-taste-advisor
```

## Key Rules

- **Sole writer of `seo_finalization`** (R-A2). `seo_strategy.on_page_recommendations` are advisory seeds only.
- **Terminology protection** (R-C1): edits limited to the metadata layer; any change touching a
  `context_pack.glossary` term is blocked.
- **Bounded fact-check loop** (R-C2): metadata changes do not re-run `fact-checker`; body-fact changes (rare)
  re-run it at most once, else stop and ask the author.

## Output

A top-level `seo_finalization` object per `schemas/context_pack_schema.json` (v2.3.0). Required:
`meta_title` (≤ 60), `meta_description` (≤ 155), `slug` (kebab-case), `finalized_at`. Optional: `image_alt`,
`internal_links`, `overrides`.

## Boundaries

Not a fact checker, not a chart generator, does not rewrite the article's argument.
