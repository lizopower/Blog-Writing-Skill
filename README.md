# Blog Writing Skill

`Blog-Writing-Skill` is a Claude Skills bundle for technical and B2B article production. It is designed for source-backed writing workflows: brainstorm an article, create an article workspace, research with Tavily, pressure-test the strategy, build a context pack, outline, draft, fact-check, and review the final article.

The bundle is domain-agnostic. It can be used for industrial equipment, software, manufacturing, materials science, logistics, finance, energy, and other technical or B2B topics. The user must provide or confirm the real industry context, audience, business goal, and source material.

## What This Repository Contains

This repository is a skill bundle, not an application server.

- `SKILL.md`: the entry router that selects the right sub-skill.
- `skills/blog-brainstorm/`: early ideation and article workspace creation.
- `skills/blog-writing-workflow/`: full 8-step writing workflow with long-form details in `references/`.
- `skills/grill-me/`: one-question-at-a-time strategy pressure test.
- `skills/tech-research/`: Tavily-backed technical/B2B research.
- `skills/tech-blog-orchestrator/`: context pack preparation from a topic and/or files.
- `skills/tech-file-parser/`: extraction from PDF, Word, Excel, and structured files.
- `skills/data-validator/`: context pack schema and quality validation.
- `skills/tech-article-architect/`: outline and section planning.
- `skills/tech-visualization-generator/`: chart and visualization manifest planning.
- `skills/tech-blog-writer/`: final article drafting from an outline and context pack.
- `skills/fact-checker/`: claim, number, unit, and source verification.
- `skills/content-taste-advisor/`: editorial taste, differentiation, and publishability review.
- `standards/`: shared contracts for workspaces, source attribution, Tavily usage, progress, errors, and caching.
- `schemas/context_pack_schema.json`: JSON schema for structured article evidence.
- `templates/article_templates.md`: reusable article templates.
- `commands/`: command-style wrappers for common workflow steps.

## Required Dependency: Tavily

Online research in this bundle requires Tavily. Tavily is a hard prerequisite for research-dependent workflows, not an optional enhancement.

Install Tavily skills first:

```bash
npx skills add https://github.com/tavily-ai/skills
```

Install and authenticate the Tavily CLI:

```bash
curl -fsSL https://cli.tavily.com/install.sh | bash
tvly login --api-key tvly-YOUR_KEY
```

Alternative CLI installs:

```bash
uv tool install tavily-cli
# or
pip install tavily-cli
```

Alternative authentication:

```bash
tvly login
# or
export TAVILY_API_KEY=tvly-YOUR_KEY
```

Verify Tavily before using online research:

```bash
tvly --status
```

Research-dependent skills must stop if Tavily skills, `tvly`, or authentication are unavailable. They should not silently fall back to generic web search.

Local file-only parsing can run without Tavily until the workflow needs online topic research, source discovery, or claim verification beyond the provided files.

## Install Blog-Writing-Skill

OpenAI Skills are supported in Codex and follow the Agent Skills open standard, but skills do not automatically sync across products. If you installed this bundle for Claude or ChatGPT, install it separately for Codex.

### Install for Codex

Clone this repository:

```bash
git clone https://github.com/lizopower/Blog-Writing-Skill.git
```

Option A: ask Codex to install from GitHub:

```text
Use skill-installer to install https://github.com/lizopower/Blog-Writing-Skill into Codex.
```

Option B: install manually into Codex skills:

```bash
mkdir -p ~/.codex/skills
cp -R Blog-Writing-Skill ~/.codex/skills/blog-writing-skills
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills"
Copy-Item -Recurse -Force ".\Blog-Writing-Skill" "$HOME\.codex\skills\blog-writing-skills"
```

The final Codex skill folder should look like:

```text
~/.codex/skills/blog-writing-skills/
  SKILL.md
  skills/
  standards/
  schemas/
  templates/
  commands/
  .codex-plugin/
```

After installing, restart Codex or start a new Codex thread so the skill index is refreshed.

### Install for Codex as a Plugin Bundle

This repository also includes:

```text
.codex-plugin/plugin.json
```

That manifest lets Codex plugin workflows identify this repository as the `blog-writing-skills` plugin bundle. When using a local plugin marketplace workflow, point the plugin source at this repository root and reinstall/restart Codex according to your Codex plugin setup.

Codex plugin installs load skills from `./skills/`. For that path, this repository includes `skills/blog-writing-skills/SKILL.md` as a Codex-facing router. Direct skill installs into `$CODEX_HOME/skills/blog-writing-skills` use the root `SKILL.md` router.

### Install for Claude

For Claude-style local skills, the final folder should look like:

```text
~/.claude/skills/blog-writing-skills/
  SKILL.md
  skills/
  standards/
  schemas/
  templates/
  commands/
```

On Windows, that is commonly:

```text
C:\Users\<you>\.claude\skills\blog-writing-skills\
```

If your environment supports installing skills directly from a GitHub repository, install from:

```text
https://github.com/lizopower/Blog-Writing-Skill
```

After installation, restart or reload your agent session so it can discover the new skills.

## Codex Setup Checklist

After installing for Codex, verify:

```text
Ask Codex: "Do you see the blog-writing-skills skill? Summarize its routing rules."
```

Then confirm Tavily in the same Codex environment:

```bash
tvly --status
```

Codex must have access to both:

- this skill bundle in `$CODEX_HOME/skills/blog-writing-skills` or `~/.codex/skills/blog-writing-skills`;
- Tavily skills from `https://github.com/tavily-ai/skills`;
- Tavily CLI authentication through `tvly login` or `TAVILY_API_KEY`.

If Codex cannot see the skill after installation, start a new thread or restart the Codex app/CLI. If Codex can see this skill but research stops, install/authenticate Tavily in the Codex environment.

## Quick Start

Use the entry skill naturally. The router in `SKILL.md` will select the sub-skill when the user asks for brainstorming, research, article creation, pressure testing, outlining, drafting, fact-checking, or editorial review.

Example prompts:

```text
帮我头脑风暴一篇关于工业视觉检测软件的文章方向，要像 Trellis 一样建工作区。
```

```text
Create a 2000-word technical article about warehouse automation ROI. Use Tavily research and fact-check all claims.
```

```text
Grill me on this article angle until the positioning is defensible.
```

```text
I have a context_pack and outline. Write the final article, then fact-check it.
```

## Recommended Workflow

For a serious article, use this path:

1. `blog-brainstorm`: turn a vague topic into a confirmed brief and article workspace.
2. `tech-research` or `audience-pain-point-research`: gather source-backed evidence with Tavily.
3. `tech-blog-orchestrator`: assemble source material into `context_pack.json`.
4. `data-validator`: check the context pack before writing.
5. `grill-me`: pressure-test the strategy if the angle is risky, vague, competitive, under-evidenced, or explicitly requested.
6. `tech-article-architect`: create the outline and section plan.
7. `tech-visualization-generator`: plan charts when structured data is available.
8. `tech-blog-writer`: write the article from the outline and context pack.
9. `fact-checker`: verify numbers, units, claims, and source traceability.
10. `content-taste-advisor`: review differentiation, clarity, and publishability.

If the user asks for a complete article directly, use `blog-writing-workflow`. It coordinates the full pipeline.

## Full Article Workflow

`blog-writing-workflow` runs an 8-step pipeline:

1. Audience Pain Point Research, optional.
2. Content Preparation with `tech-blog-orchestrator`.
3. Data Validation with `data-validator`.
4. Strategy Pressure Test with `grill-me`, conditional and mandatory when requested.
5. Article Architecture with `tech-article-architect`.
6. Visualization planning with `tech-visualization-generator`, conditional.
7. Article Writing with `tech-blog-writer`.
8. Fact Check with `fact-checker`.

Required steps are content preparation, validation, architecture, writing, and fact-checking. Visualization depends on available data. Audience research depends on the topic and user request. `grill-me` must run when the user explicitly asks to be grilled, challenged, pressure-tested, or deeply questioned.

## Article Workspace Contract

`blog-brainstorm` creates a Trellis-like article workspace in the user's current project:

```text
content/articles/<slug>/
  article.json
  brief.md
  research/
  sources.jsonl
  context_pack.json
  strategy.md
  outline.md
  draft.md
  fact_check.md
  editorial_review.md
  finish.md
```

The slug should be lowercase kebab-case, derived from the topic or working title.

When scripts are available, create and validate the workspace with:

```bash
python skills/blog-brainstorm/scripts/create_article_workspace.py "<Working Title>" --slug <slug> --root <project-root>
python skills/blog-brainstorm/scripts/validate_article_workspace.py <project-root>/content/articles/<slug>
```

`article.json` is the workflow state file. It tracks the article id, title, status, current phase, next action, article type, business goal, audience, keyword, angle, and timestamps. Update it after each meaningful phase.

The normal lifecycle is:

```text
brainstorming
brief_confirmed
research_planning
context_building
strategy_pressure_test
outlining
drafting
fact_checking
editorial_review
completed
```

Do not overwrite an existing article workspace. If `content/articles/<slug>/` already exists, read `article.json` and continue from the current phase.

## Key Artifacts

- `brief.md`: human-readable article strategy, audience, pain, angle, CTA, and success criteria.
- `research/`: durable notes grouped by topic or source cluster.
- `sources.jsonl`: one source inventory record per line.
- `context_pack.json`: structured claims, sources, data, glossary, risk notes, and metadata.
- `strategy.md`: pressure-test decisions, rejected angles, evidence gaps, and risk tradeoffs.
- `outline.md`: article structure and reader decision path.
- `draft.md`: article body.
- `fact_check.md`: factual, numerical, unit, source, and logic review.
- `editorial_review.md`: taste, differentiation, SEO, CTA, and publishability review.
- `finish.md`: final summary, reusable learnings, weak sources, and follow-up article ideas.

## Skill Routing Guide

Use the most specific skill that matches the user's intent:

| User Intent | Use |
|---|---|
| Vague idea, topic selection, content strategy, Trellis-like workspace | `blog-brainstorm` |
| Full article from topic/files to final draft | `blog-writing-workflow` |
| "Grill me", pressure-test, challenge, interrogate, deeply question | `grill-me` |
| Source-backed technical or B2B research | `tech-research` |
| Audience pain, social listening, real search intent | `audience-pain-point-research` |
| Convert topic and/or files into a context pack | `tech-blog-orchestrator` |
| Extract data from PDF, Word, Excel, or tables | `tech-file-parser` |
| Validate context pack completeness and quality | `data-validator` |
| Turn context pack into an outline | `tech-article-architect` |
| Plan charts from structured data | `tech-visualization-generator` |
| Draft from outline plus context pack | `tech-blog-writer` |
| Check facts, numbers, units, sources, and logic | `fact-checker` |
| Judge whether content is compelling or publishable | `content-taste-advisor` |

When the request is unclear, ask one clarifying question instead of guessing.

## How `blog-brainstorm` Works

`blog-brainstorm` is designed to feel closer to Trellis than a simple ideation prompt.

It should:

1. Create the full article workspace up front.
2. Recommend a direction before asking the user to decide.
3. Ask exactly one question at a time.
4. Update `brief.md` and `article.json` after each answer.
5. Converge on a confirmed brief.
6. End with exactly two options:
   - Continue to research / workflow
   - Stop at confirmed brief

Default decision sequence:

```text
business goal -> target audience -> reader pain -> article angle -> evidence available -> CTA -> scope boundary -> success criteria
```

## How `grill-me` Works

`grill-me` pressure-tests a plan one branch at a time. It is mandatory before drafting when the user explicitly asks to be grilled, challenged, pressure-tested, or relentlessly questioned.

It should:

1. Inspect available files, workspace state, context pack, outline, and prior discussion first.
2. Ask exactly one pressure-testing question at a time.
3. Include the assistant's recommended answer and rationale with each question.
4. Walk the decision tree in this order:

```text
goal -> audience -> pain -> angle -> evidence -> structure -> claims -> visuals -> CTA -> quality gate
```

5. Finish with resolved decisions, unresolved risks, and the next sub-skill recommendation.

## Tavily Research Behavior

Research work maps to Tavily skills as follows:

- `tavily-search`: targeted source discovery.
- `tavily-extract`: clean extraction from known URLs.
- `tavily-research`: deeper multi-source reports.
- `tavily-map`: URL discovery on a known site.
- `tavily-crawl`: bulk collection from a docs or site section.
- `tavily-best-practices`: implementation and usage reference.

For technical claims, prefer authoritative sources such as standards bodies, peer-reviewed papers, government or university research, manufacturer technical white papers, credible analyst reports, and technical conference proceedings.

Avoid unsupported blog posts, marketing-only brochures, unsourced social media claims, or superlatives without evidence.

Every key claim should carry:

- the claim text,
- source reference,
- source type,
- confidence level,
- relevant units and test conditions if numerical,
- uncertainty or limitations when applicable.

## Context Pack Expectations

`context_pack.json` is the evidence object passed downstream to the architect, writer, chart planner, and fact checker. The current contract is Context Pack v2.1.0.

At minimum, it should include:

- `version`
- `generated_at`
- `topic`
- `audience`
- `key_claims`
- `extracted_tables`
- `glossary`
- `risk_notes`
- metadata about files and research sources when available

Validate against `schemas/context_pack_schema.json` and run `data-validator` before drafting.

If using the bundled validator directly:

```bash
python skills/tech-blog-orchestrator/scripts/validate_context_pack.py <context_pack.json>
```

## Example Prompts

Brainstorm:

```text
帮我头脑风暴一篇关于 B2B SaaS 数据治理的文章，先推荐方向，再问我问题，创建完整文章工作区。
```

Full workflow:

```text
写一篇 1800 字中文技术博客，主题是预测性维护软件如何降低停机成本。请用 Tavily 做研究，输出事实检查结果。
```

Topic plus files:

```text
根据我提供的测试报告和 Excel 数据，写一篇关于新材料耐温性能的技术文章。需要图表建议和事实检查。
```

Research only:

```text
Research credible sources for an article about cold-chain logistics software ROI. Return structured notes, source tiers, and research gaps.
```

Pressure test:

```text
Grill me on this outline. Keep asking one question at a time until the angle, evidence, CTA, and quality gate are solid.
```

Fact check:

```text
Check this draft against the context_pack. Flag unsupported claims, unit issues, logic gaps, and source mismatches.
```

Editorial review:

```text
This article feels generic. Review it with content-taste-advisor and tell me whether it is worth publishing.
```

## Troubleshooting

### Tavily is missing

Symptom: the agent stops before research and asks for Tavily setup.

Fix:

```bash
npx skills add https://github.com/tavily-ai/skills
curl -fsSL https://cli.tavily.com/install.sh | bash
tvly login --api-key tvly-YOUR_KEY
tvly --status
```

### `tvly` is installed but not authenticated

Fix:

```bash
tvly login
# or
export TAVILY_API_KEY=tvly-YOUR_KEY
```

Then re-run:

```bash
tvly --status
```

### The agent wants to use generic web search

Stop the workflow and remind it:

```text
This Blog-Writing-Skill requires Tavily for online research. Do not use generic web search. Run Tavily preflight first.
```

### The article feels unsupported

Run:

```text
Use data-validator on the context_pack, then run grill-me before outlining.
```

If evidence is missing, return to `tech-research` or `audience-pain-point-research`.

### The draft has facts that are not in the context pack

Run:

```text
Use fact-checker against the draft and context_pack. Remove or source every unsupported claim.
```

### A workspace already exists

Do not regenerate from scratch. Ask the agent to inspect:

```text
content/articles/<slug>/article.json
content/articles/<slug>/brief.md
content/articles/<slug>/context_pack.json
```

Then continue from `article.json.currentPhase`.

## Maintenance Notes

When adding a new sub-skill:

1. Add its directory under `skills/<skill-name>/SKILL.md`.
2. Add a routing rule and quick reference entry in root `SKILL.md`.
3. Add usage guidance to this README if users need to invoke it directly.
4. Update standards or schemas if the new skill changes shared artifacts.

When changing research behavior:

1. Update `standards/tavily_research_engine.md`.
2. Update affected skills such as `tech-research`, `tech-blog-orchestrator`, and `blog-writing-workflow`.
3. Keep the hard dependency rule explicit: no silent fallback from Tavily to generic web search.

## License

MIT. See `LICENSE`.
