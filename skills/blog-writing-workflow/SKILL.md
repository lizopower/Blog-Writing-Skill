---
name: blog-writing-workflow
description: Use when the user requests a full technical blog or article end-to-end and you need to run the complete workflow.
---

# Blog Writing Workflow - Master Orchestrator

## CRITICAL: Use This Skill First

**When user requests:**
- "写一篇关于X的博客" / "写博客关于X"
- "Create a blog about X" / "Write a blog about X"
- "Write an article about X" / "Create an article about X"
- "写一篇技术文章关于X"
- Provides topic + optional files for blog content

**YOU MUST invoke THIS skill immediately.**

## Purpose

This skill executes the complete blog writing pipeline automatically, coordinating all sub-skills in the correct order to produce a publication-ready technical article with quality assurance.

## Article Workspace Awareness

Before executing the workflow, check whether the user has an existing article workspace:

```text
content/articles/<slug>/
```

If an article workspace exists:
- Treat `article.json` as the workflow state source.
- Treat `brief.md` as the strategy source of truth.
- Read existing `research/`, `sources.jsonl`, `context_pack.json`, `strategy.md`, `outline.md`, `draft.md`, `fact_check.md`, and `editorial_review.md` before regenerating anything.
- Continue from `article.json.currentPhase` when possible.
- Do not overwrite workspace artifacts without user confirmation.

If no workspace exists and the request is still vague or strategic, invoke `blog-brainstorm` before this full workflow.

## Automatic Workflow Execution

This skill executes the complete blog writing pipeline in **8 steps** (v2.1):

**Progress Display**:
Each step shows real-time progress:
```
Step 1/8: Audience Research (audience-pain-point-research) [Optional]
├─ [████████░░] 80% Analyzing pain points...
└─ Estimated Time: 45s

Step 2/8: Content Preparation (tech-blog-orchestrator)
├─ [██████████] 100% Complete
└─ Duration: 30s
```

---

### Step 1: Audience Pain Point Research (Optional)
**Skill**: `audience-pain-point-research`
**Purpose**: Research real audience pain points from social platforms to guide content strategy

**When to run**:
- User requests "深入分析受众" or "audience research"
- User wants SEO-optimized content targeting real user concerns
- Creating content for a new topic area

**Action**:
```
Invoke Skill: audience-pain-point-research
Input: {topic, audience_segment (optional)}
Output: Pain Point Analysis Table (8-12 pain points with semantic queries)
```

**What happens**:
- Analyzes Reddit, Quora, YouTube, LinkedIn, PAA
- Identifies first-person pain point statements
- Maps search intent and SERP features
- Identifies content gaps and opportunities
- Outputs structured table for content strategy

**Decision Point**:
- Output feeds into Step 2 (orchestrator) to guide research focus
- If skipped, proceed directly to Step 2

---

### Step 2: Content Preparation (tech-blog-orchestrator)
**Skill**: `tech-blog-orchestrator`
**Purpose**: Research topic and/or parse files to create Context Pack

**Action**:
```
Invoke Skill: tech-blog-orchestrator
Input: {
  topic,
  files (if any),
  pain_points: from Step 1 (if available)
}
Output: Context Pack (JSON with key_claims, extracted_tables, glossary, etc.)
```

**What happens**:
- If topic provided → Triggers `tech-research` (online research)
- If files provided → Triggers `tech-file-parser` (file parsing)
- Both run in parallel if both inputs exist
- Incorporates pain points to focus research (if available)
- Outputs structured Context Pack with all data sources

---

### Step 3: Data Validation (data-validator)
**Skill**: `data-validator`
**Purpose**: Validate Context Pack quality before proceeding

**Action**:
```
Invoke Skill: data-validator
Input: {context_pack: from Step 2}
Output: Validation Report (JSON with quality_score, issues, recommendations)
```

**What happens**:
- Schema validation (required fields, data types)
- Data quality checks (units, sources, confidence levels)
- Consistency checks (duplicate values match, units unified)
- Completeness checks (data gaps identified)
- Generates quality score (0-100)

**Decision Point**:
- `status: "passed"` → Continue to Step 4
- `status: "passed_with_warnings"` → Show warnings, ask user to continue or fix
- `status: "failed"` → Stop workflow, report errors to user

---

### Step 4: Strategy Pressure Test (grill-me) [Conditional / Mandatory if Requested]
**Skill**: `grill-me`
**Purpose**: Pressure-test the content strategy before committing to the outline.

**When to run**:
- User explicitly asks for "grill me", "追问我", "拷问我", "pressure-test", "stress-test", "challenge this", or similar.
- Topic is high-risk, high-competition, under-evidenced, or strategically ambiguous.
- Data validation returns warnings that affect the thesis, evidence chain, or scope.
- Multiple plausible article angles remain after context_pack creation.

**Action**:
```
Invoke Skill: grill-me
Input: {
  topic,
  context_pack: from Step 2,
  validation_report: from Step 3,
  user_goal,
  known_audience,
  candidate_angles (if any)
}
Output: Strategy Pressure Test Summary (resolved decisions, evidence gaps, rejected angles, next-step recommendation)
```

**What happens**:
- Asks one pressure-testing question at a time
- Provides a recommended answer for each question
- Resolves audience, pain point, angle, evidence, scope, claims, visuals, CTA, and quality gate decisions
- Identifies whether more research, validation, or user input is needed before outlining

**Decision Point**:
- If `grill-me` identifies missing evidence -> return to Step 2 or invoke `tech-research` / `audience-pain-point-research`
- If `grill-me` identifies context_pack quality issues -> return to Step 3 after fixing
- If strategy is settled -> Continue to Step 5
- If not triggered -> Continue directly to Step 5

---

### Step 5: Article Architecture (tech-article-architect)
**Skill**: `tech-article-architect`
**Purpose**: Design article structure and outline based on validated Context Pack

**Action**:
```
Invoke Skill: tech-article-architect
Input: {
  context_pack,
  target_word_count,
  strategy_summary: from Step 4 (if available)
}
Output: outline.md + section_plan.json
```

**What happens**:
- Creates structured outline (≤20 sections)
- Allocates word budget per section
- Plans chart placement
- Documents data sources for each section
- Identifies risk points and data gaps

---

### Step 6: Visualization (tech-visualization-generator) [Conditional]
**Skill**: `tech-visualization-generator`
**Purpose**: Generate chart manifests from structured data

**When to run**: Only if context_pack has `extracted_tables` or suitable data

**Action**:
```
If context_pack has extracted_tables or suitable data:
  Invoke Skill: tech-visualization-generator
  Input: {context_pack}
  Output: charts_manifest.json
Else:
  Skip this step (charts_manifest = empty)
```

**What happens**:
- Converts tables/data into chart specifications
- Creates chart_01, chart_02, etc. with metadata
- Provides drawing instructions for each chart
- Documents data sources and limitations

---

### Step 7: Article Writing (tech-blog-writer)
**Skill**: `tech-blog-writer`
**Purpose**: Write the complete publication-ready article

**Action**:
```
Invoke Skill: tech-blog-writer
Input: {
  outline: from Step 5,
  context_pack: from Step 2,
  charts_manifest: from Step 6 (or empty),
  strategy_summary: from Step 4 (if available),
  target_word_count: user specified or default 2000
}
Output: final_article.md
```

**What happens**:
- Writes article body following outline structure
- Integrates charts at designated positions
- Ensures all quantitative claims have sources
- Maintains engineer-to-engineer tone
- Includes SEO components (title, meta, FAQ)
- Generates self-audit report

---

### Step 8: Fact Check (fact-checker)
**Skill**: `fact-checker`
**Purpose**: Validate article accuracy against Context Pack

**Action**:
```
Invoke Skill: fact-checker
Input: {
  article: from Step 7,
  context_pack: from Step 2
}
Output: Fact Check Report (JSON with issues, severity, recommendations)
```

**What happens**:
- Numeric consistency check (same values across sections)
- Unit consistency check (°C vs °F, Ah vs kWh)
- Logic contradiction detection
- Source traceability verification (all claims traceable to context_pack)
- Range reasonability check (percentages 0-100%, valid temperatures)

**Decision Point**:
- `status: "passed"` → Workflow complete, present article
- `status: "passed_with_warnings"` → Present article with warnings for review
- `status: "failed"` → Flag critical issues, recommend fixes before publishing

---

## Execution Instructions

When this skill is invoked, follow these steps:

### 1. Parse User Request

Extract from user message:
- **Topic**: Main subject (e.g., "[product/technology] in [application scenario]")
- **Files**: Any uploaded PDF/Word/Excel files
- **Target word count**: Specified number or default 2000
- **Language**: Chinese or English (default: follow topic language)
- **Special requirements**: Keyword density, specific focus areas, etc.
- **Audience research requested**: Does user want pain point analysis?

### 2. Execute Step 1 - Audience Research (Optional)

```
If user requests audience research OR topic is new/unfamiliar:
  Use Skill tool to invoke: audience-pain-point-research
  Pass parameters: {
    topic: extracted topic,
    audience_segment: "engineers, procurement managers" (or as specified)
  }
  Wait for output: Pain Point Analysis Table
Else:
  Skip this step, set pain_points = null
```

**Announce to user**: "Step 1/8: Researching audience pain points..." (if executed)

### 3. Execute Step 2 - Orchestrator

```
Use Skill tool to invoke: tech-blog-orchestrator
Pass parameters: {
  topic: extracted topic,
  files: uploaded files (if any),
  pain_points: from Step 1 (if available)
}
Wait for output: Context Pack (JSON)
```

**Announce to user**: "Step 2/8: Researching topic and preparing context pack..."

### 4. Execute Step 3 - Data Validation

```
Use Skill tool to invoke: data-validator
Pass parameters: {
  context_pack: from Step 2
}
Wait for output: Validation Report (JSON)
```

**Announce to user**: "Step 3/8: Validating data quality..."

**Decision Logic**:
```
If validation_result.status == "failed":
  Report errors to user
  Ask: "Data quality issues found. Fix and retry, or proceed with caution?"
  If user wants to fix → Stop workflow
  If user wants to proceed → Continue with warnings

If validation_result.status == "passed_with_warnings":
  Show warnings to user
  Continue to Step 4

If validation_result.status == "passed":
  Continue to Step 4
```

### 5. Execute Step 4 - Strategy Pressure Test (Conditional / Mandatory if Requested)

```
If user explicitly requested grilling/pressure-testing OR validation warnings affect strategy OR topic is high-risk/high-competition/under-evidenced OR multiple plausible angles remain:
  Use Skill tool to invoke: grill-me
  Pass parameters: {
    topic: extracted topic,
    context_pack: from Step 2,
    validation_report: from Step 3,
    user_goal: extracted goal,
    known_audience: from user input or context_pack,
    candidate_angles: any plausible angles discovered so far
  }
  Wait for output: Strategy Pressure Test Summary
Else:
  Skip this step
  Set strategy_summary = empty
```

**Announce to user**: "Step 4/8: Pressure-testing content strategy..." (if executed)

### 6. Execute Step 5 - Architect

```
Use Skill tool to invoke: tech-article-architect
Pass parameters: {
  context_pack: from Step 2,
  target_word_count: user specified or 2000,
  strategy_summary: from Step 4 (if available)
}
Wait for output: outline.md + section_plan.json
```

**Announce to user**: "Step 5/8: Designing article structure and outline..."

### 7. Execute Step 6 - Visualization (Conditional)

```
Check if context_pack has extracted_tables or suitable data:

If YES:
  Use Skill tool to invoke: tech-visualization-generator
  Pass parameters: {
    dataset_json: context_pack
  }
  Wait for output: charts_manifest.json

If NO:
  Skip this step
  Set charts_manifest = empty
```

**Announce to user**: "Step 6/8: Generating visualization specifications..." (if executed)

### 8. Execute Step 7 - Writer

```
Use Skill tool to invoke: tech-blog-writer
Pass parameters: {
  outline: from Step 5,
  target_word_count: user specified or 2000,
  context_pack: from Step 2,
  charts_manifest: from Step 6 (or empty),
  strategy_summary: from Step 4 (if available),
  brand_constraints: {
    industry: "[fill in — e.g. 'Industrial Equipment']",
    segment: "[fill in — e.g. 'B2B [Product Category] for [Customer Segment]']",
    core_advantage: "[fill in — the differentiating claim the article supports]",
    caution: "Do not exaggerate; mark uncertain conditions"
  },
  style_constraints: {
    language: detected language,
    tone: "Engineer-to-engineer, direct, verifiable",
    formatting: "Lists, comparison tables, bold for key conclusions"
  }
}
Wait for output: final_article.md
```

**Announce to user**: "Step 7/8: Writing publication-ready article..."

### 9. Execute Step 8 - Fact Check

```
Use Skill tool to invoke: fact-checker
Pass parameters: {
  article: from Step 7,
  context_pack: from Step 2
}
Wait for output: Fact Check Report (JSON)
```

**Announce to user**: "Step 8/8: Fact-checking article..."

**Decision Logic**:
```
If fact_check_report.status == "failed":
  Present article with critical issues flagged
  List all issues with severity and location
  Recommend: "Please review and fix these issues before publishing"

If fact_check_report.status == "passed_with_warnings":
  Present article with warnings
  List warnings for human review

If fact_check_report.status == "passed":
  Present article as publication-ready
```

### 10. Present Final Output

Present to user:
- **final_article.md**: Complete article with all sections
- **Word count summary**: Actual vs. target
- **Data validation report**: Quality score and any issues
- **Fact check report**: Consistency verification results
- **Next steps**: Suggestions for review/editing

---

## Example Invocations

### Example 1: Topic Only (Chinese) - Standard Flow

**User says**: "写一篇关于[产品/技术]的1000字文章，需要合适的关键词密度"

**Your immediate response**:
```
I'll use the blog-writing-workflow to create a 1000-word technical article about [topic] with appropriate keyword density.

[Invoke Skill tool with: blog-writing-workflow]
```

**Then execute**:
1. Parse: topic="[product/technology]", target_word_count=1000, language="English"
2. Skip Step 1 (no audience research requested)
3. Invoke tech-blog-orchestrator (research only, no files)
4. Invoke data-validator (validate Context Pack)
5. Invoke tech-article-architect (1000-word outline)
6. Invoke tech-visualization-generator (if data available)
7. Invoke tech-blog-writer (write article)
8. Invoke fact-checker (verify accuracy)
9. Present final_article.md with quality reports

### Example 2: Topic + Files + Audience Research

**User says**: "写一篇关于[产品/场景]的博客，我上传了测试报告。请先分析一下目标受众的痛点"
**User uploads**: product_test_report.pdf

**Your immediate response**:
```
I'll use the blog-writing-workflow to create a technical article about [topic]. I'll first analyze audience pain points, then incorporate data from your test report.

[Invoke Skill tool with: blog-writing-workflow]
```

**Then execute**:
1. Parse: topic="[product/scenario]", files=[product_test_report.pdf], audience_research=true
2. Invoke audience-pain-point-research (analyze pain points)
3. Invoke tech-blog-orchestrator (research + file parsing, guided by pain points)
4. Invoke data-validator (validate Context Pack)
5. Invoke tech-article-architect
6. Invoke tech-visualization-generator (likely has data from PDF)
7. Invoke tech-blog-writer
8. Invoke fact-checker
9. Present final_article.md with quality reports

### Example 3: English Article with Full Quality Assurance

**User says**: "Create a 2000-word blog about [topic]. Make sure all facts are verified."

**Your immediate response**:
```
I'll use the blog-writing-workflow to create a comprehensive 2000-word technical article about [topic] with full fact-checking.

[Invoke Skill tool with: blog-writing-workflow]
```

**Then execute**:
1. Parse: topic="[topic]", target_word_count=2000, language="English"
2. Skip Step 1 (no audience research requested)
3. Invoke tech-blog-orchestrator
4. Invoke data-validator (validate Context Pack quality)
5. Invoke tech-article-architect (2000-word outline)
6. Invoke tech-visualization-generator (if data available)
7. Invoke tech-blog-writer
8. Invoke fact-checker (full fact verification as requested)
9. Present final_article.md with detailed fact check report

---

## Critical Rules

### 1. Never Skip Required Steps
- **Steps 2, 5, 7, 8 are mandatory** (orchestrator, architect, writer, fact-checker)
- Step 1 (audience research) is optional but recommended for new topics
- Step 3 (data validation) should always run but can be overridden by user
- Step 4 (strategy pressure test) is mandatory when explicitly requested and conditional for strategic-risk cases
- Step 6 (visualization) is conditional on data availability
- Each step depends on outputs from previous steps
- Do not attempt to write article manually

### 2. Wait for Outputs
- **Block and wait** for each skill to complete before proceeding
- Do not proceed to next step until current step returns output
- If a step fails, report error to user and stop workflow

### 3. Pass Data Forward
- **Pain Points** from Step 1 → Step 2 (Orchestrator) - guides research focus
- **Context Pack** from Step 2 → Steps 3, 4, 5, 7, 8
- **Validation Report** from Step 3 → Decision gate and Step 4 pressure test
- **Strategy Summary** from Step 4 → Steps 5 and 7 (if available)
- **Outline** from Step 5 → Step 7 (Writer)
- **Charts Manifest** from Step 6 → Step 7 (Writer)
- **Article** from Step 7 → Step 8 (Fact Checker)
- Never fabricate or modify intermediate outputs

### 4. Handle Errors Gracefully
- If audience research fails → Skip and proceed to Step 2
- If research fails → Report to user, ask if they want to proceed with limited data
- If file parsing fails → Report error, suggest file format check
- If validation fails → Show issues, ask user to fix or proceed with caution
- If architect fails → Report error, check Context Pack validity
- If writer fails → Report error, check all inputs are valid
- If fact check fails → Present article with issues flagged for review

### 5. No Manual Writing
- **Never write article content manually**
- Always delegate to tech-blog-writer skill
- Your role is orchestration only, not content generation

### 6. Respect User Parameters
- **Word count**: Use exact number specified by user
- **Language**: Follow user's language preference
- **Keyword density**: Pass requirement to writer skill
- **Special focus**: Include in context for all sub-skills
- **Audience research**: Execute if user requests or topic is new

---

## Success Criteria

The workflow is successful when:

✅ All required steps executed without critical errors
✅ Audience pain points identified (if Step 1 executed)
✅ Context Pack contains research data and/or file data
✅ Data validation passed or passed with warnings
✅ Outline matches target word count allocation
✅ Charts manifest generated (if data available)
✅ Final article is publication-ready
✅ Article word count within ±10% of target
✅ All quantitative claims have sources
✅ Fact check passed or issues clearly flagged
✅ User receives complete final_article.md with quality reports

---

## Failure Scenarios & Recovery

### Scenario 1: Audience Research Fails
**Problem**: audience-pain-point-research cannot find relevant discussions

**Recovery**:
1. Report to user: "Limited audience data found for this topic"
2. Skip Step 1, proceed to Step 2 without pain point guidance
3. Note in final output: "Article written without audience pain point analysis"

### Scenario 2: Research Returns No Data
**Problem**: tech-blog-orchestrator returns empty or minimal Context Pack

**Recovery**:
1. Report to user: "Research yielded limited data for this topic"
2. Ask user: "Would you like to proceed with available data, or provide additional files?"
3. If user provides files → Re-run Step 2 with files
4. If user wants to proceed → Continue with limited data, flag in article

### Scenario 3: File Parsing Fails
**Problem**: tech-file-parser cannot extract data from uploaded files

**Recovery**:
1. Report specific error (e.g., "PDF is scanned image, OCR failed")
2. Ask user to provide alternative format or manual data
3. If alternative provided → Re-run Step 2
4. If not → Proceed with research data only

### Scenario 4: Data Validation Fails
**Problem**: data-validator returns status "failed"

**Recovery**:
1. Show validation report with all issues
2. Present options to user:
   - "Fix issues and re-run orchestrator"
   - "Proceed with caution (issues will be flagged in article)"
3. If user chooses to fix → Stop workflow, await new data
4. If user proceeds → Continue with warnings attached

### Scenario 5: Insufficient Data for Charts
**Problem**: Context Pack lacks structured data for visualization

**Recovery**:
1. Skip Step 6 (visualization)
2. Set charts_manifest = empty
3. Proceed to Step 7 with text-only article
4. Note in final output: "No charts generated due to insufficient structured data"

### Scenario 6: Fact Check Finds Issues
**Problem**: fact-checker returns status "failed" or "passed_with_warnings"

**Recovery**:
1. Present article with fact check report attached
2. Highlight all issues with severity and location
3. For "failed" status:
   - "Critical inconsistencies found. Please review before publishing."
   - List specific corrections needed
4. For "passed_with_warnings":
   - "Minor issues found for your review."
   - Article is usable but recommend human verification

---

## When to Use This Skill

**Invoke immediately when user requests:**
- "写博客" / "write blog" / "create blog"
- "写文章" / "write article" / "create article"
- "技术文章" / "technical article"
- Any variation of blog/article creation request

**Do NOT use for:**
- Editing existing articles (use direct editing instead)
- Answering questions about blog writing (provide guidance directly)
- Creating outlines only (user can invoke tech-article-architect directly)
- Quick content snippets (this is for complete articles)

---

## Output Format

After completing all steps, present to user:

```markdown
# Blog Writing Workflow Complete

## Article Generated Successfully

**Topic**: [extracted topic]
**Word Count**: [actual] words (Target: [target] words)
**Language**: [detected language]
**Processing Time**: [time taken]
**Steps Executed**: [list of steps run]

## Quality Reports

### Data Validation (Step 3)
- **Status**: [passed/passed_with_warnings/failed]
- **Quality Score**: [0-100]
- **Issues**: [count] ([high/medium/low severity breakdown])

### Fact Check (Step 8)
- **Status**: [passed/passed_with_warnings/failed]
- **Claims Checked**: [count]
- **Consistent**: [count] | **Inconsistent**: [count] | **Untraceable**: [count]

## Final Output

The complete article has been saved to: `final_article.md`

### Article Structure:
- SEO Title & Meta Description
- TL;DR (3-5 key points)
- [X] main sections
- [Y] subsections
- FAQ ([Z] questions)
- Self-Audit Report

### Data Sources:
- Audience pain points: [count] (if Step 1 executed)
- Research sources: [count]
- Extracted tables: [count]
- Charts generated: [count]

### Quality Metrics:
✅ Data validation: [status]
✅ Fact check: [status]
✅ Word count within target range
✅ Engineering tone maintained
✅ All quantitative claims sourced

## Issues Requiring Attention (if any)

[List any warnings or issues from validation and fact check]

## Next Steps

1. Review the article for accuracy
2. Address any flagged issues from quality reports
3. Verify all source citations
4. Make any necessary edits
5. Publish when ready

---

[Attach: final_article.md content]
```

---

## Quality Assurance Checklist

Before presenting final output, verify:

- [ ] All required workflow steps completed successfully
- [ ] Audience pain points analyzed (if Step 1 executed)
- [ ] Context Pack contains valid data
- [ ] Data validation passed or issues documented
- [ ] Strategy pressure test completed when requested or when strategic-risk triggers are present
- [ ] Outline structure is logical and complete
- [ ] Charts manifest generated (if applicable)
- [ ] Final article includes all required sections
- [ ] Word count within ±10% of target
- [ ] All quantitative claims have sources
- [ ] Fact check completed and issues documented
- [ ] No manual content generation occurred
- [ ] All sub-skills invoked via Skill tool

---

## Integration Notes

### Sub-Skills Required
This workflow depends on:
1. `audience-pain-point-research` - Optional (audience analysis)
2. `tech-blog-orchestrator` - **Required** (content preparation)
3. `data-validator` - **Required** (quality gate)
4. `tech-article-architect` - **Required** (structure design)
5. `tech-visualization-generator` - Optional (conditional on data)
6. `tech-blog-writer` - **Required** (article writing)
7. `fact-checker` - **Required** (accuracy verification)

### Nested Dependencies
- `tech-blog-orchestrator` internally calls:
  - `tech-research` (online research)
  - `tech-file-parser` (file parsing)

### Data Flow
```
User Input (topic + files + options)
    │
    ├─[Optional]─→ audience-pain-point-research
    │                    ↓
    │              Pain Point Analysis
    │                    ↓
    └────────────→ tech-blog-orchestrator ←── pain_points (if available)
                         ↓
                   Context Pack (JSON)
                         ↓
                   data-validator
                         ↓
                   Validation Report ──[Decision Gate]
                         ↓
              [Conditional / Mandatory if Requested] grill-me ← Context Pack + Validation Report
                         ↓
                   Strategy Pressure Test Summary (or empty)
                         ↓
                   tech-article-architect ← Context Pack + strategy_summary
                         ↓
                   outline.md + section_plan.json
                         ↓
              [Conditional] tech-visualization-generator ← Context Pack
                         ↓
                   charts_manifest.json (or empty)
                         ↓
                   tech-blog-writer ← outline + Context Pack + charts_manifest + strategy_summary
                         ↓
                   final_article.md
                         ↓
                   fact-checker ← article + Context Pack
                         ↓
                   Fact Check Report ──[Quality Gate]
                         ↓
                   Present to User
```

---

## Version & Metadata

**Version**: 2.1.0
**Updated**: 2026-01-19
**Industry**: Domain-agnostic — supply your own industry context
**Role**: Master Workflow Orchestrator
**Output**: Complete publication-ready technical articles with quality assurance
**Steps**: 8 (4 optional/conditional)

---

## Summary

This skill is the **single entry point** for all technical blog writing requests. It automatically coordinates the entire content creation pipeline from audience research to final fact-checked article, ensuring:

- **Audience-centric content** (optional pain point research)
- **Comprehensive research and data collection** (orchestrator)
- **Data quality assurance** (validation before writing)
- **Structured article architecture** (architect)
- **Data-driven visualizations** (conditional)
- **Publication-ready content with source attribution** (writer)
- **Fact-checked accuracy** (final verification)

**8-Step Pipeline**:
1. Audience Pain Point Research (Optional)
2. Content Preparation (Orchestrator)
3. Data Validation (Quality Gate)
4. Strategy Pressure Test (Conditional / Mandatory if Requested)
5. Article Architecture (Outline)
6. Visualization (Conditional)
7. Article Writing (Content)
8. Fact Check (Accuracy Gate)

**Remember**: Always invoke this skill first when user requests blog/article creation. Never attempt manual writing - let the workflow handle it.

---

*End of blog-writing-workflow skill definition*









