---
name: blog-writing-skills
description: Use when a user asks to brainstorm, plan, write, draft, outline, research, fact-check, improve, pressure-test, grill, challenge, or deeply review a technical/B2B blog post, article, white paper, or thought-leadership piece and you need to choose the right blog-writing sub-skill.
---

# Blog-Writing-Skills Entry

## Overview
This is an entry skill that routes requests to the right blog-writing sub-skill in this bundle. The bundle is domain-agnostic: it works for technical or B2B subject matter such as industrial equipment, software, materials science, manufacturing, logistics, finance, or energy. Always ground the workflow in the user's source material, audience context, and stated business goal.

## Default Discipline: Full Pipeline (mandatory)

When the user asks to write, create, or draft a full article, blog post, or white paper from a topic — with or without files — the **default is the complete `blog-writing-workflow` pipeline**: research/orchestration → validation → (pressure test) → outline → draft → fact-check. Running the whole pipeline is the norm, not the exception.

- **Execution contract**: When this skill routes to `blog-writing-workflow`, execute the workflow stages. This bundle describes a production pipeline with evidence-gathering, validation, outline, drafting, and fact-check gates; treating it as a style reference skips those gates and produces unsupported output.
- Do not extract writing-style or voice guidance from any file in this skill bundle (including sub-skill `SKILL.md` files, references, assets, templates, or examples) and use it to draft directly.
- Disabling or declining CCG, project management, task archival, or any other process framework, whether by user instruction or configuration, does **not** disable this skill's article workflow. Continue the Blog-Writing-Skill pipeline unless the user explicitly waives specific Blog-Writing-Skill stages.
- If a required dependency blocks a stage (for example Tavily is unavailable for online research), stop and report that the complete workflow is blocked. Ask whether the user wants to install/authenticate the dependency, provide local sources, or explicitly accept a degraded non-workflow draft.
- **Never** shortcut a topic-level article request straight to `tech-blog-writer`. That skill is the final drafting stage only; it requires an upstream validated context_pack and outline.
- **Research momentum is not a waiver.** Successful Tavily search/extract results, deep-research notes, or a clear mental structure are not a Context Pack, not validation, not an outline, and not permission to draft.
- **Rich input is not a waiver.** A complete-looking user brief — title, audience, angle, keyword list, desired structure, source links, pasted notes, CTA, tone, and word count — is raw material for the workflow. It is not a validated `context_pack`, not an approved outline, and not permission to write article body text directly.
- **Never** skip research, validation, outline, or fact-check on your own initiative to "save time." A request that merely names a topic, audience, word count, or keyword density is **not** permission to skip steps.
- **Pre-draft gate**: Before any article body text is written, verify that a validated `context_pack` and an `outline` exist or were explicitly waived by the user. If either is missing, stop and route back to `blog-writing-workflow`.
- **Workflow receipts are mandatory** for full article work. After each stage, state the stage, artifact, status, and next allowed skill. Do not keep intermediate artifacts only in memory.
- Skip a step **only** when the user explicitly asks for it — e.g. "直接写" / "跳过研究" / "不用查资料" / "skip research" / "just draft it" / "no fact-check". When you do skip on explicit request, say which steps you skipped and why.
- When a conditional step (audience research, visualization) is genuinely inapplicable (no data for charts, etc.), announce that you are skipping it and why — do not skip silently.

## Required Dependency

Online research in this bundle requires Tavily.

Before using research-dependent workflows, install:

```bash
npx skills add https://github.com/tavily-ai/skills
```

Then install and authenticate Tavily CLI:

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash
tvly login --api-key tvly-YOUR_KEY
```

If Tavily is unavailable, research-dependent skills must stop and ask the user to install/authenticate Tavily instead of falling back to generic web search.

## When to Use This Skill

Use when the user asks for a technical or B2B content task and the correct sub-skill is unclear, including:
- Early article ideation, topic selection, content strategy, or Trellis-like article workspace creation.
- End-to-end blog or article creation.
- Research notes, source gathering, or audience pain-point discovery.
- PDF, Word, Excel, table, or data extraction for an article.
- Context pack preparation, validation, outline design, final drafting, chart planning, or fact checking.
- Editorial judgment, content quality review, or taste-driven content decisions.
- Pressure-testing a content plan, interrogating an outline, or asking "grill me" / "追问我".

Do not use this entry skill when the user already named a specific sub-skill. Invoke that sub-skill directly.

## Not For / Boundaries

- Do not invent statistics, case studies, quotes, citations, or product claims. If source material is missing, ask for it or route to `tech-research`.
- Do not provide professional legal, medical, financial, safety, or regulatory advice as final authority. For high-risk domains, require source-backed claims and route through `fact-checker`.
- Do not treat any industry as the default. Infer the industry from the user's topic or files, then carry that context through the selected sub-skill.
- Route factual or technical drafts through `fact-checker` before treating them as complete.

## Quick Reference
- Trellis-like brainstorm from vague idea to article workspace + brief: `blog-brainstorm`
- Relentlessly question or pressure-test a blog/content plan: `grill-me`
- Full end-to-end article workflow: `blog-writing-workflow`
- Extract tables or structured data from PDF, Word, or Excel files: `tech-file-parser`
- Prepare a context_pack only, from a topic and/or files: `tech-blog-orchestrator`
- Research technical/B2B sources and return structured notes: `tech-research`
- Research audience pain points from social platforms: `audience-pain-point-research`
- Produce a SERP-grounded keyword + search-intent strategy (`seo_strategy`) before research/outline: `seo-serp-strategist`
- Validate context_pack schema, completeness, and data quality: `data-validator`
- Generate chart specs or a visualization manifest from structured data: `tech-visualization-generator`
- Build an outline and section plan from a context_pack: `tech-article-architect`
- Write the final article from an outline + context_pack: `tech-blog-writer`
- Check a draft against context_pack facts, numbers, units, and logic: `fact-checker`
- Final on-page SEO QA (meta, slug, alt, internal links, schema) after fact-check: `on-page-seo-finalizer`
- Review editorial quality, taste, and whether content is worth making: `content-taste-advisor`

## Routing Rules

Evaluate these rules top-down. Prefer the most specific matching sub-skill over a general one. If multiple steps are required, invoke the first needed sub-skill and make the next handoff explicit.

1. If the user asks to brainstorm, ideate, choose a topic, define content strategy, create an article workspace, or says "头脑风暴", invoke `blog-brainstorm`.
2. If the user asks to "grill me", "追问我", "拷问我", pressure-test, stress-test, challenge, interrogate, or relentlessly question a content idea, outline, strategy, or plan, invoke `grill-me`. This route is mandatory and takes priority over drafting, research, or review routes unless the user is still asking for open-ended brainstorm.
3. If the user asks to write, create, or draft a full article, blog post, or white paper from a topic (with or without files) — including a bare "write an article about X" / "写一篇关于 X 的文章" — invoke `blog-writing-workflow` and run the COMPLETE pipeline. Do not skip steps unless the user explicitly asks to (see Default Discipline). This is the default route for article-creation requests.
4. If the user's primary ask is to pull tables, values, or structured information out of PDF, Word, or Excel files, invoke `tech-file-parser`.
5. If the user provides files, research notes, or raw material and wants them turned into article-ready context, invoke `tech-blog-orchestrator`.
6. If the user asks for technical/B2B source research, market context, competitor examples, or source-backed notes for a topic, invoke `tech-research`.
7. If the user asks what the target audience cares about, complains about, searches for, or discusses on social platforms, invoke `audience-pain-point-research`.
7b. If the user asks for SERP analysis, keyword/search-intent strategy, competitor SERP structure, or an `seo_strategy` for an English keyword/topic, invoke `seo-serp-strategist`. This is the SEO strategy layer that runs before research and outline; it is independent from `audience-pain-point-research`.
8. If the user asks whether a context_pack is complete, valid, clean, or ready for writing, invoke `data-validator`.
9. If the user provides structured data and asks for charts, visual treatment, chart specs, or a visualization manifest, invoke `tech-visualization-generator`.
10. If the user provides a context_pack but no outline, invoke `tech-article-architect`.
11. If the user provides an outline but no context_pack, invoke `tech-blog-orchestrator` or `tech-research` first to build evidence before drafting.
12. Invoke `tech-blog-writer` **only** when the user explicitly supplies BOTH a ready outline AND a validated context_pack and asks only to draft, OR explicitly asks to skip upstream research/validation. A topic-only or "write an article" request must go to `blog-writing-workflow` (rule 3), never directly to `tech-blog-writer`.
13. If the user asks whether facts, numbers, units, or reasoning are correct in a draft, invoke `fact-checker`.
13b. After fact-check, if the user asks for final on-page SEO QA — meta title/description, URL slug, image alt, internal links, table formatting, or FAQ schema — invoke `on-page-seo-finalizer`. It writes the sole final on-page values and protects glossary terms.
14. If the user asks whether the content is compelling, differentiated, or worth publishing, invoke `content-taste-advisor`.
15. If the request remains under-specified after these rules, ask one clarifying question instead of guessing.

## Examples

### Example 1: Grill Me
User: "Grill me on this technical blog idea until the angle is solid."
Action: Invoke `grill-me`.
Acceptance: The assistant asks one pressure-testing question at a time, gives a recommended answer, and ends with resolved decisions plus the next sub-skill.

### Example 2: Blog Brainstorm
User: "帮我头脑风暴一篇关于工业视觉检测软件的文章方向，要像 Trellis 一样建工作区。"
Action: Invoke `blog-brainstorm`.
Acceptance: The assistant creates `content/articles/<slug>/`, writes the full skeleton, recommends direction, asks one question at a time, and converges to a confirmed brief.

### Example 3: Final Draft (artifacts already provided)
User: "I have an outline and a validated context_pack. Write only the final article."
Action: Invoke `tech-blog-writer`.
Acceptance: The article uses only the provided context_pack for factual claims and does not add new data. (If the user had only given a topic, this would route to `blog-writing-workflow` instead.)

### Example 4: Full Workflow
User: "Create a technical blog post about warehouse automation ROI from these reports, including research and a final draft."
Action: Invoke `blog-writing-workflow`.
Acceptance: The workflow produces research/context, an outline, a draft, and fact-checking steps as needed.

### Example 4b: Rich Input Still Uses the Workflow
User: "Here is the title, target audience, keyword list, section outline, source links, CTA, tone, and word count. Write the article."
Action: Invoke `blog-writing-workflow`.
Acceptance: Treat the rich input as raw material. Create or update workflow artifacts, validate/build the Context Pack, produce/confirm the outline, then draft and fact-check. Do not draft directly unless the user explicitly waives upstream workflow stages.

### Example 5: File Extraction
User: "Pull the useful tables from this PDF and spreadsheet so we can use them in an article."
Action: Invoke `tech-file-parser`.
Acceptance: The output is structured extracted data with page/sheet references where available.

### Example 6: Source Research
User: "Research the main technical arguments and credible sources for an article about predictive maintenance software."
Action: Invoke `tech-research`.
Acceptance: The output is structured, source-backed research notes without unsupported claims.

### Example 7: Audience Pain Points
User: "Find what supply chain managers complain about when choosing cold-chain logistics software."
Action: Invoke `audience-pain-point-research`.
Acceptance: The output groups real audience concerns into pain-point themes and usable query angles.

### Example 8: Data Validation
User: "Before we write, check whether this context_pack is complete and internally consistent."
Action: Invoke `data-validator`.
Acceptance: The output flags schema gaps, missing source fields, weak evidence, or data-quality issues.

### Example 9: Visualization Manifest
User: "Turn this comparison table into chart specs for the article."
Action: Invoke `tech-visualization-generator`.
Acceptance: The output proposes visualizations from provided data only and does not invent values.

### Example 10: Fact Check
User: "Check whether this draft's numbers and claims match the context_pack."
Action: Invoke `fact-checker`.
Acceptance: The output flags mismatches, unsupported claims, unit issues, and logic gaps.

### Example 11: Editorial Taste
User: "This article feels generic. Tell me whether it is worth publishing and how to sharpen it."
Action: Invoke `content-taste-advisor`.
Acceptance: The output identifies weak angles, stronger positioning, and concrete editorial changes.

## Common Mistakes
- **Treating this bundle as a writing-style reference instead of executing the routed sub-skill workflow. If the user asks for a full article, produce workflow artifacts or clearly say the full workflow was blocked/waived.**
- **Jumping straight to `tech-blog-writer`, or skipping research / validation / outline / fact-check, for a topic-only article request. The full `blog-writing-workflow` pipeline is the default; only the user can waive a step (see Default Discipline).**
- **Treating a detailed user brief as if it were already a validated Context Pack and approved outline. Completeness of the prompt is not a workflow waiver.**
- **Treating successful Tavily/deep-research output as enough to draft. Research notes must be converted into a Context Pack, validated, outlined, drafted through `tech-blog-writer`, and fact-checked.**
- Invoking `blog-writing-skills` directly instead of the specific sub-skill.
- Sending vague ideation or Trellis-like article workspace creation directly to `blog-writing-workflow` instead of `blog-brainstorm`.
- Missing mandatory `grill-me` routing when the user asks to be grilled, challenged, pressure-tested, or relentlessly questioned.
- Skipping `fact-checker` before calling a draft complete.
- Using `tech-research` when the request is file parsing (use `tech-file-parser`).
- Using `tech-blog-orchestrator` for the full end-to-end article workflow when `blog-writing-workflow` is the better route.
- Treating `tech-blog-orchestrator` as a full pipeline runner; it prepares a context_pack only.
- Sending audience sentiment, complaints, or social-platform pain-point work to generic `tech-research` instead of `audience-pain-point-research`.

## Maintenance

- Keep this entry file as a router, not a documentation dump.
- When adding a new sub-skill to the bundle, add it to Quick Reference and include a routing rule if it overlaps with existing skills.
- Last reviewed: 2026-06-08
