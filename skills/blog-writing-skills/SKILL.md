---
name: blog-writing-skills
description: Use when a Codex user asks to brainstorm, plan, write, draft, outline, research, fact-check, improve, pressure-test, grill, challenge, or deeply review a technical/B2B blog post, article, white paper, or thought-leadership piece and you need to choose the right blog-writing sub-skill.
---

# Blog-Writing-Skills Codex Router

This is the Codex plugin-facing router for the Blog-Writing-Skill bundle. It mirrors the root `SKILL.md` entry so Codex plugin installs that load skills from `./skills/` still expose the top-level routing behavior.

## Default Discipline: Full Pipeline (mandatory)

A request to write/create/draft a full article from a topic (with or without files) defaults to the **complete `blog-writing-workflow` pipeline**: research → validation → (pressure test) → outline → draft → fact-check. Do not shortcut a topic-level request to `tech-blog-writer`, and do not skip research, validation, outline, or fact-check on your own. Skip a step only on an explicit user request ("直接写" / "跳过研究" / "skip research" / "just draft"), and say which steps you skipped.

## Required Dependency

Online research requires Tavily in the same Codex environment.

Before research-dependent workflows, confirm:

```bash
tvly --status
```

If Tavily skills, Tavily CLI, or authentication are unavailable, stop and ask the user to install/authenticate Tavily. Do not silently fall back to generic web search.

## Routing Rules

Evaluate top-down and invoke the most specific sub-skill:

1. Brainstorm, ideation, topic selection, content strategy, or Trellis-like article workspace: `blog-brainstorm`.
2. "grill me", "追问我", "拷问我", challenge, pressure-test, stress-test, or interrogate a content plan: `grill-me`.
3. Any request to write/create/draft a full article from a topic (with or without files), including a bare "write an article about X": `blog-writing-workflow`, run the COMPLETE pipeline (default route — do not skip steps without explicit user opt-out).
4. PDF, Word, Excel, table, or structured data extraction: `tech-file-parser`.
5. Topic/files/raw material into article-ready Context Pack: `tech-blog-orchestrator`.
6. Source-backed technical/B2B research: `tech-research`.
7. Audience pain points, complaints, search intent, or social-platform research: `audience-pain-point-research`.
8. Context Pack validation: `data-validator`.
9. Chart specs or visualization manifest: `tech-visualization-generator`.
10. Context Pack to outline: `tech-article-architect`.
11. Final draft **only when** the user explicitly supplies both a ready outline and a validated Context Pack (or explicitly asks to skip upstream steps): `tech-blog-writer`. Topic-only article requests go to rule 3, never here.
12. Draft factual verification: `fact-checker`.
13. Editorial quality, differentiation, or publishability review: `content-taste-advisor`.

If the request is still under-specified, ask one clarifying question.

## Common Mistakes

- Do not jump straight to `tech-blog-writer`, or skip research/validation/outline/fact-check, for a topic-only article request. The full pipeline is the default; only the user can waive a step.
- Do not skip `blog-brainstorm` for vague article ideas.
- Do not miss mandatory `grill-me` routing when the user asks to be challenged or pressure-tested.
- Do not draft factual articles before building or validating a Context Pack.
- Do not call a factual draft complete before `fact-checker`.

## Codex Install Note

This router exists so Codex plugin installs can discover the top-level bundle behavior from `./skills/`. Direct skill installs into `$CODEX_HOME/skills/blog-writing-skills` should use the root `SKILL.md`.
