# AEO / GEO Citation Signals — Adopted, Adapted, Rejected

Version: 1.0.0

This standard records how the bundle treats "answer-engine / generative-engine
optimization" (AEO/GEO) advice — the practice of writing content that AI
assistants (ChatGPT, Perplexity, Google AI Overviews) quote. It is derived from
a 17-signal checklist that cites large studies (Indig 1.2M ChatGPT citations,
Semrush 337,785 URLs, Wix 75,000 answers, Ahrefs, Seer).

## Read this first: the evidence is weak-to-moderate

Apply these signals as **writing-quality hygiene, not a ranking hack.**

- The findings are **correlational, not causal.** "TL;DR correlates +32.83% with
  citation" does not mean adding a TL;DR causes citations. Cited pages may simply
  be better pages.
- **Survivorship bias**: studies look at already-cited / already-ranked pages.
- **Time-sensitive**: AI retrieval behavior shifts fast (one study saw listicle
  citations fall 30% in a single month).
- **Vendor self-interest**: much AEO advice is published by people selling AEO
  services.
- **Mechanism claims are speculation** ("`is` acts as a vector bridge", "the
  model treats the H2 as a prompt"). Plausible, unverified. Do not encode them
  as engineering fact.
- The numeric targets (Flesch-Kincaid grade 16, subjectivity 0.47, entity
  density 20.6%) are single-study medians and **false precision** — never hard
  gates, never applicable to Chinese or cross-industry text.

**Hard rule that overrides every signal below:** citation optimization may never
induce fabrication, keyword/entity stuffing, or stripping of evidence
qualifiers. For engineers, credibility comes from test conditions, standards,
limits, and traceable data — not from headline/H2/sentence tricks.

## Adopted — wired into skills

| Signal | Where | Rule |
|---|---|---|
| Front-load the answer | architect | Answer-first placement |
| Format matches query intent | architect | Intent-to-Format gate |
| Outcome-naming headline | architect | Outcome title |
| One idea per section | architect | Section atomicity |
| H2 as real question (selectively) | architect | Selective question headers |
| Claim + source adjacency | architect | Evidence adjacency |
| Update before writing new | architect / workflow | Freshness gate |
| Definitions use "is/means" | tech-blog-writer | Rule 15 |
| Entity echo under question-H2 | tech-blog-writer | Rule 16 |
| Named entities (sourced only) | tech-blog-writer | Rule 17 |
| Primary source + date + sample size | tech-blog-writer | Rule 18 |
| Strip empty hedges, keep evidence hedges | tech-blog-writer | Rule 14 (amended) |
| Analyst voice: fact + implication | tech-blog-writer | existing engineering-advisor tone |
| Source metadata / primary-vs-secondary | data-validator / fact-checker | validation checks below |

## Rejected or down-scoped — and why

- **Grade-16 / Flesch-Kincaid target (Signal 7)** — rejected as a gate. Useless
  for Chinese, not comparable across industries, and pushes against plain
  technical clarity. (Also rejects the opposite "Flesch 60–70 / grade 8" advice.)
  Keep: business-grade prose, not dumbed-down, not jargon soup.
- **Every H2 as a question (Signal 2)** — down-scoped. Blanket question headers
  read like an SEO farm in advanced engineering content; use them only for
  FAQ/definition/selection/comparison sections.
- **Entity density ~20% (Signal 9)** — down-scoped. Raise entity richness
  naturally via real tool/version/standard/metric names; never stuff to hit a
  number (stuffing is itself an AI tell).
- **One original data point per section (Signal 13)** — down-scoped. Forcing it
  induces fabrication. Adapted to: if the context_pack holds firsthand evidence,
  prioritize placing it in key sections; otherwise mark a data_gap.
- **Author-bio credential (Signal 12)** — optional metadata only; never pad body
  text with it.

## Validation checks (data-validator / fact-checker)

- Research/web sources should carry `publisher`, `published_at`, `sample_size`,
  and `primary_or_secondary`. Missing fields → downgrade confidence.
- A claim sourced only to a blog that re-reports a study → Warning: go upstream.
- Causal language ("causes / proves / leads to / guarantees") on top of a merely
  correlational source → flag as a logic risk.
- A self-authored "best/comparison" list that ranks the author's own product
  first → require disclosure of criteria and interest.
