---
name: blog-writing-skills
description: Use when a user asks to brainstorm, plan, write, draft, outline, research, fact-check, improve, pressure-test, grill, challenge, or deeply review a technical/B2B blog post, article, white paper, or thought-leadership piece and you need to choose the right blog-writing sub-skill.
---

# Blog-Writing-Skills Entry

## Overview
This is an entry skill that routes requests to the right blog-writing sub-skill in this bundle. The bundle is domain-agnostic: it works for technical or B2B subject matter such as industrial equipment, software, materials science, manufacturing, logistics, finance, or energy. Always ground the workflow in the user's source material, audience context, and stated business goal.

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
- Validate context_pack schema, completeness, and data quality: `data-validator`
- Generate chart specs or a visualization manifest from structured data: `tech-visualization-generator`
- Build an outline and section plan from a context_pack: `tech-article-architect`
- Write the final article from an outline + context_pack: `tech-blog-writer`
- Check a draft against context_pack facts, numbers, units, and logic: `fact-checker`
- Review editorial quality, taste, and whether content is worth making: `content-taste-advisor`

## Routing Rules

Evaluate these rules top-down. Prefer the most specific matching sub-skill over a general one. If multiple steps are required, invoke the first needed sub-skill and make the next handoff explicit.

1. If the user asks to brainstorm, ideate, choose a topic, define content strategy, create an article workspace, or says "头脑风暴", invoke `blog-brainstorm`.
2. If the user asks to "grill me", "追问我", "拷问我", pressure-test, stress-test, challenge, interrogate, or relentlessly question a content idea, outline, strategy, or plan, invoke `grill-me`. This route is mandatory and takes priority over drafting, research, or review routes unless the user is still asking for open-ended brainstorm.
3. If the user asks for "the whole article," "from research to draft," or an end-to-end workflow, invoke `blog-writing-workflow`.
4. If the user's primary ask is to pull tables, values, or structured information out of PDF, Word, or Excel files, invoke `tech-file-parser`.
5. If the user provides files, research notes, or raw material and wants them turned into article-ready context, invoke `tech-blog-orchestrator`.
6. If the user asks for technical/B2B source research, market context, competitor examples, or source-backed notes for a topic, invoke `tech-research`.
7. If the user asks what the target audience cares about, complains about, searches for, or discusses on social platforms, invoke `audience-pain-point-research`.
8. If the user asks whether a context_pack is complete, valid, clean, or ready for writing, invoke `data-validator`.
9. If the user provides structured data and asks for charts, visual treatment, chart specs, or a visualization manifest, invoke `tech-visualization-generator`.
10. If the user provides a context_pack but no outline, invoke `tech-article-architect`.
11. If the user provides an outline but no context_pack, invoke `tech-blog-orchestrator` or `tech-research` first to build evidence before drafting.
12. If the user provides both an outline and a context_pack, invoke `tech-blog-writer`.
13. If the user asks whether facts, numbers, units, or reasoning are correct in a draft, invoke `fact-checker`.
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

### Example 3: Final Draft
User: "I have an outline and context_pack. Write the final article."
Action: Invoke `tech-blog-writer`.
Acceptance: The article uses only the provided context_pack for factual claims and does not add new data.

### Example 4: Full Workflow
User: "Create a technical blog post about warehouse automation ROI from these reports, including research and a final draft."
Action: Invoke `blog-writing-workflow`.
Acceptance: The workflow produces research/context, an outline, a draft, and fact-checking steps as needed.

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
