---
name: tech-blog-orchestrator
description: Use when preparing a context_pack from a topic and/or files for the technical blog writing workflow.
---

# Technical Blog Orchestrator

## Overview

Orchestrate technical blog content preparation by coordinating research and file parsing workflows, then outputting a structured Context Pack. This skill serves as a router/orchestrator and does NOT generate article body text.

## Tavily Requirement

Online topic research must go through `tech-research`, which requires Tavily skills and Tavily CLI authentication.

Before triggering topic research, confirm Tavily is available:
- Tavily skills from `https://github.com/tavily-ai/skills`
- Tavily CLI `tvly`
- `tvly login` or `TAVILY_API_KEY`

If Tavily is unavailable and topic research is needed, stop and ask the user to install/authenticate Tavily. Do not silently fall back to generic web search.

## Industry Context

This skill is domain-agnostic. Before running it, fill in the context for the subject at hand:

- **Industry**: e.g. "Industrial Equipment", "Enterprise Software", "Materials Science"
- **Market segment**: e.g. "B2B [Product Category] for [Customer Segment]"
- **Core advantage**: The differentiating claim the article needs to support
- **Target audience**: e.g. "Engineers, procurement managers, project managers"

## Workflow Decision Tree

Upon receiving a user request to write a technical blog, follow this decision tree:

### 1. Input Analysis

Identify which inputs are present:

- **Topic-Only**: User provides a topic/theme description, no files
- **Files-Only**: User uploads files (PDF/Word/Excel), no topic
- **Topic + Files**: Both topic and files are provided
- **Style / Offering Materials**: User provides prior articles, brand/product notes, positioning docs, editorial guardrails, or author experience notes

### 2. Parallel Task Orchestration

Based on input type, trigger tasks **in parallel**:

#### If Topic is Present:
- **Trigger**: `tech-research` with Tavily-backed research
- **Purpose**: Conduct online research about the topic
- **Expected Output**: 
  - Industry trends and insights
  - Technical specifications
  - Competitive landscape
  - Market data
  - Relevant case studies

#### If Files are Present:
- **Trigger**: Parse Skill (or equivalent file parsing workflow)
- **Purpose**: Extract structured content from uploaded files
- **Expected Output**:
  - Text content from PDFs
  - Tables from Excel files (with sheet names)
  - Structured data from Word documents
  - Metadata (page numbers, sections, sources)

#### If Style / Offering Materials are Present:
- **Trigger**: Parse and classify the material before Context Pack assembly
- **Purpose**: Separate writing guidance from factual evidence
- **Expected Output**:
  - `style_exemplars`: prior articles or samples used for voice, structure, rhythm, and guardrails only
  - `core_offerings`: source-backed product/service names, value props, target users, and when-to-mention guidance
  - `author_experience_notes`: user-provided stories, edit preferences, and expert observations
  - `risk_notes`: any product claim, anecdote, or statistic that lacks a traceable source

### 3. Context Pack Assembly

Aggregate results from all triggered tasks into a unified JSON structure called the **Context Pack**.

## Context Pack Output Format

Use Context Pack v2.2.0. Keep this shape aligned with:
- `../../schemas/context_pack_schema.json`
- `assets/context_pack_template.json`
- `scripts/validate_context_pack.py`

Output the following JSON structure:

```json
{
  "version": "2.2.0",
  "generated_at": "ISO-8601 timestamp",
  "workflow_id": "wf_YYYYMMDD_HHMMSS",
  "topic": "string - The main topic/theme of the blog article",
  "audience": ["Engineers", "Procurement Managers", "Project Managers"],
  "industry_context": {
    "industry": "string - e.g. 'Industrial Equipment', 'Enterprise Software'",
    "market_segment": "string - e.g. 'B2B [Product Category] for [Customer Segment]'",
    "core_advantage": "string - the differentiating claim the article needs to support"
  },
  "style_exemplars": [
    {
      "reference": "string - file path, URL, or artifact id for the style sample",
      "scope": "style_only",
      "what_to_emulate": ["array - voice, structure, rhythm, framing, formatting traits"],
      "what_to_avoid": ["array - author-specific guardrails or weak patterns"]
    }
  ],
  "core_offerings": [
    {
      "name": "string - product or service name",
      "value_prop": "string - source-backed value statement",
      "target_user": "string - role or audience segment",
      "when_to_mention": "string - reader problem or article section where it is relevant",
      "source_ref": "string - traceable source for positioning and value claim"
    }
  ],
  "author_experience_notes": [
    {
      "note": "string - user-provided story, expert observation, edit preference, or guardrail",
      "source_ref": "string - interview note, user instruction, or document reference",
      "usable_as": "story_anchor | expert_commentary | guardrail | preference"
    }
  ],
  "key_claims": [
    {
      "claim": "string - Key technical or business claim",
      "source": {
        "type": "pdf | excel | word | web | research | user_provided",
        "reference": "string - URL, file name + page number, or research note reference",
        "url": "optional URL",
        "credibility": "high | medium | low",
        "verified_by": "skill or reviewer name",
        "verified_at": "ISO-8601 timestamp"
      },
      "confidence": "high | medium | low",
      "data": "optional structured numeric data"
    }
  ],
  "extracted_tables": [
    {
      "table_id": "table_1",
      "source": "string - Filename + sheet/page (e.g., 'data.xlsx:Sheet1' or 'report.pdf:p5')",
      "title": "string - Descriptive name for the table",
      "description": "string - What this table represents",
      "columns": [
        {
          "name": "Column name",
          "type": "string | number | date | boolean",
          "unit": "required for numeric columns"
        }
      ],
      "data": [
        {
          "Column name": "value"
        }
      ],
      "data_format": "array_of_objects",
      "extracted_at": "ISO-8601 timestamp"
    }
  ],
  "glossary": [
    {
      "term": "string - Technical term or acronym",
      "definition": "string - Clear definition",
      "context": "string - Why this term matters to the audience"
    }
  ],
  "risk_notes": [
    {
      "risk_type": "data_gap | uncertainty | conflict | limitation",
      "description": "string - What is uncertain or needs verification",
      "severity": "high | medium | low",
      "mitigation": "string - Suggested action for human review"
    }
  ],
  "research_summary": {
    "sources_count": "number - Total sources consulted",
    "last_updated": "string - ISO timestamp",
    "key_findings": ["array of strings - Top 3-5 findings from research"]
  },
  "file_summary": {
    "files_processed": ["array of strings - Filenames processed"],
    "total_pages": "number - Total pages across all files",
    "extraction_notes": ["array of strings - Any issues or special notes during extraction"]
  },
  "metadata": {
    "files_processed": "number",
    "research_sources": "number",
    "total_data_points": "number",
    "processing_time_seconds": "number"
  }
}
```

## Key Rules

1. **No Article Writing**: Do NOT generate article body text, introductions, conclusions, or narrative content
2. **No Chart Generation**: Do NOT create visualizations, graphs, or diagrams
3. **No SEO Work**: Do NOT perform keyword optimization, meta descriptions, or SEO analysis
4. **Parallel Execution**: Always trigger Tavily-backed research and file parsing concurrently when both inputs exist
5. **Source Attribution**: Every key_claim MUST include a traceable source
6. **Risk Flagging**: Flag any uncertain, contradictory, or unverified information in risk_notes
7. **Structured Output Only**: Always output the Context Pack as valid JSON
8. **Style Exemplar Boundary**: Style exemplars shape voice and structure only; never promote their facts, stats, case studies, or claims into `key_claims` without an independent traceable source
9. **Product Context Boundary**: Core offerings may guide contextual mentions, but unsupported value claims must become `risk_notes`, not article-ready claims
10. **Experience Boundary**: Author stories and first-person lessons must come from `author_experience_notes`, `key_claims`, or `extracted_tables`; never derive them from `style_exemplars` or invent them

## Execution Steps

### Step 1: Analyze User Input
- Parse the user request
- Identify if topic is provided
- Identify if files are attached
- Identify if style exemplars, product/offering docs, editorial guardrails, or author experience notes are attached
- Determine workflow path (Topic-Only / Files-Only / Topic+Files / Style+Offering Materials)

### Step 2: Trigger Parallel Tasks
- If topic exists: Initiate research workflow to gather online information
- If files exist: Initiate file parsing workflow to extract content
- If style/offering materials exist: Classify them into `style_exemplars`, `core_offerings`, `author_experience_notes`, and unsupported claims in `risk_notes`
- Execute both simultaneously if both inputs present

### Step 3: Aggregate Results
- Collect research findings (if applicable)
- Collect parsed file content (if applicable)
- Identify key claims and their sources
- Extract any tables with source metadata
- Classify prior articles as `style_exemplars` only unless their factual claims are independently sourced
- Extract source-backed product/service context into `core_offerings`
- Capture user-provided stories, expert edits, and voice preferences as `author_experience_notes`
- Build glossary of technical terms
- Flag any uncertainties or contradictions

### Step 4: Output Context Pack
- Format all aggregated data into the JSON Context Pack structure
- Validate JSON syntax
- Run `python scripts/validate_context_pack.py <context_pack.json>` when a local file is available
- Present to user with brief summary of what was processed
- When working inside `content/articles/<slug>/`, save the context pack to `context_pack.json`, then advance lifecycle state with:
  ```bash
  python skills/blog-brainstorm/scripts/article.py advance --to context_building --slug <slug> --root <project-root>
  python skills/blog-brainstorm/scripts/article.py advance --to strategy_pressure_test --slug <slug> --root <project-root>
  ```
  If the command exits non-zero, stop and report the gate reason instead of editing `article.json.currentPhase` manually.

### Step 5: Validate Context Pack (NEW - v2.0)
- **Trigger**: data-validator skill
- **Purpose**: Ensure Context Pack quality before passing to downstream skills
- **Validation checks**:
  - Schema compliance (required fields, data types)
  - Data quality (units, sources, confidence levels)
  - Consistency (no conflicting data)
  - Completeness (no critical gaps)

**Validation outcomes**:
- ✅ **Status: passed** → Continue to next step
- ⚠️ **Status: passed_with_warnings** → Display warnings, ask user if they want to continue
- ❌ **Status: failed** → Stop workflow, display errors and recommendations

**Example validation output**:
```
✅ Context Pack Validation: PASSED (Quality Score: 92/100)

Summary:
- 15 key claims validated
- 8 tables extracted with proper sources
- 0 critical errors
- 2 warnings (see below)

Warnings:
⚠️ extracted_tables[2].columns[0]: Missing unit for "Temperature"
   Recommendation: Add unit: '°C'
```

## Example Interactions

### Example 1: Topic-Only

**User Input**: "写一篇关于[产品/技术]在[应用场景]中应用的技术博客"

**Orchestrator Actions**:
1. Identify: Topic-Only workflow
2. Trigger: Research about "[product/technology] in [application scenario]"
3. Aggregate: Research findings, technical specs, use cases
4. Output: Context Pack JSON with research_summary populated, file_summary empty

### Example 2: Files-Only

**User Input**: [Uploads: `product_test_data.xlsx`, `certification_report.pdf`]

**Orchestrator Actions**:
1. Identify: Files-Only workflow
2. Trigger: Parse both files
3. Extract: Test data tables, certification details, technical specifications
4. Output: Context Pack JSON with extracted_tables and file_summary populated, research_summary minimal

### Example 3: Topic + Files

**User Input**: "写一篇关于我们产品在[关键使用场景]下性能优势的博客" + [Uploads: `performance_comparison.xlsx`]

**Orchestrator Actions**:
1. Identify: Topic+Files workflow
2. Trigger (parallel): 
   - Research the product's performance in the stated scenario
   - Parse performance_comparison.xlsx
3. Aggregate: Combine research insights with actual test data
4. Output: Complete Context Pack JSON with both research and file data

## Resources

- `assets/context_pack_template.json`: Context Pack v2.2.0 example.
- `scripts/validate_context_pack.py`: dependency-free Context Pack validator.
- `references/research_strategy.md`: research planning guide.
- `references/file_parsing_guide.md`: file parsing guide.

## Important Notes

- **Role Clarity**: This skill is an orchestrator/router ONLY. It coordinates work but does not perform content generation.
- **Human Review**: The Context Pack output is designed for human review before article writing begins.
- **Extensibility**: If a Parse skill is not available, use local file-reading/parsing tools where possible. Online research still requires Tavily and must not fall back to generic web search.
- **Quality Control**: Prioritize source attribution and risk flagging to ensure downstream content is trustworthy.
