# Blog Writing Workflow Execution Details

This reference contains the detailed execution instructions for `blog-writing-workflow`.

## Parse User Request

Extract:
- Topic
- Files
- Target word count
- Language
- Special requirements
- Audience research request
- Pressure-test request

## Step 1: Audience Research

Run when the user requests audience research, when the topic is new or unfamiliar, or when SEO/search-intent strategy matters.

Output feeds into `tech-blog-orchestrator` as `pain_points`.

## Step 2: Content Preparation

Invoke `tech-blog-orchestrator` with topic, files, and optional pain points.

Expected output: Context Pack v2.2.0.

If topic research is required, Tavily preflight must pass first.

## Step 3: Data Validation

Invoke `data-validator` with the Context Pack.

Decision:
- `passed`: continue.
- `passed_with_warnings`: show warnings and continue unless they affect strategy.
- `failed`: stop and report errors.

## Step 4: Strategy Pressure Test

Invoke `grill-me` when:
- The user explicitly asks for grilling, challenge, interrogation, stress test, or pressure test.
- Data validation warnings affect thesis, evidence, scope, or claims.
- Multiple plausible angles remain.
- The topic is high-risk, high-competition, strategically vague, or under-evidenced.

If `grill-me` finds missing evidence, return to research or orchestration before outlining.

## Step 5: Article Architecture

Invoke `tech-article-architect` with Context Pack, target word count, and optional strategy summary.

Expected output: `outline.md` and section plan.

## Step 6: Visualization

Invoke `tech-visualization-generator` only if the Context Pack has structured data suitable for visual treatment.

Expected output: charts manifest.

## Step 7: Article Writing

Invoke `tech-blog-writer` with:
- outline
- Context Pack
- charts manifest if available
- strategy summary if available
- target word count
- language and style constraints

Do not manually draft article content inside the orchestrator.

## Step 8: Fact Check

Invoke `fact-checker` with article and Context Pack.

Decision:
- `passed`: present as ready for review/publishing.
- `passed_with_warnings`: present article with warnings.
- `failed`: present issues and recommend fixes before publishing.

## Final Presentation

Report:
- Article path or content
- Word count
- Steps executed
- Data validation status
- Fact-check status
- Issues requiring human attention
- Recommended next step
