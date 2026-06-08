---
name: tech-blog-orchestrator
description: Use when preparing a context_pack from a topic and/or files for the technical blog writing workflow.
---

# Technical Blog Orchestrator

## Overview

Orchestrate technical blog content preparation by coordinating research and file parsing workflows, then outputting a structured Context Pack. This skill serves as a router/orchestrator and does NOT generate article body text.

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

### 2. Parallel Task Orchestration

Based on input type, trigger tasks **in parallel**:

#### If Topic is Present:
- **Trigger**: Research Skill (or equivalent research workflow)
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

### 3. Context Pack Assembly

Aggregate results from all triggered tasks into a unified JSON structure called the **Context Pack**.

## Context Pack Output Format

Output the following JSON structure:

```json
{
  "topic": "string - The main topic/theme of the blog article",
  "audience": ["Engineers", "Procurement Managers", "Project Managers"],
  "industry_context": {
    "industry": "string - e.g. 'Industrial Equipment', 'Enterprise Software'",
    "market_segment": "string - e.g. 'B2B [Product Category] for [Customer Segment]'",
    "core_advantage": "string - the differentiating claim the article needs to support"
  },
  "key_claims": [
    {
      "claim": "string - Key technical or business claim",
      "source": "string - URL, file name + page number, or 'Research: [date]'",
      "confidence": "high | medium | low"
    }
  ],
  "extracted_tables": [
    {
      "table_name": "string - Descriptive name for the table",
      "source": "string - Filename + sheet/page (e.g., 'data.xlsx:Sheet1' or 'report.pdf:p5')",
      "data": "array or structured representation of table data",
      "description": "string - What this table represents"
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
      "issue": "string - What is uncertain or needs verification",
      "reason": "string - Why this is flagged",
      "recommendation": "string - Suggested action for human review"
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
  }
}
```

## Key Rules

1. **No Article Writing**: Do NOT generate article body text, introductions, conclusions, or narrative content
2. **No Chart Generation**: Do NOT create visualizations, graphs, or diagrams
3. **No SEO Work**: Do NOT perform keyword optimization, meta descriptions, or SEO analysis
4. **Parallel Execution**: Always trigger research and file parsing concurrently when both inputs exist
5. **Source Attribution**: Every key_claim MUST include a traceable source
6. **Risk Flagging**: Flag any uncertain, contradictory, or unverified information in risk_notes
7. **Structured Output Only**: Always output the Context Pack as valid JSON

## Execution Steps

### Step 1: Analyze User Input
- Parse the user request
- Identify if topic is provided
- Identify if files are attached
- Determine workflow path (Topic-Only / Files-Only / Topic+Files)

### Step 2: Trigger Parallel Tasks
- If topic exists: Initiate research workflow to gather online information
- If files exist: Initiate file parsing workflow to extract content
- Execute both simultaneously if both inputs present

### Step 3: Aggregate Results
- Collect research findings (if applicable)
- Collect parsed file content (if applicable)
- Identify key claims and their sources
- Extract any tables with source metadata
- Build glossary of technical terms
- Flag any uncertainties or contradictions

### Step 4: Output Context Pack
- Format all aggregated data into the JSON Context Pack structure
- Validate JSON syntax
- Present to user with brief summary of what was processed

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

This skill does not include bundled scripts, references, or assets as it focuses purely on workflow orchestration. All actual research and parsing work should be delegated to appropriate downstream tools or skills.

## Important Notes

- **Role Clarity**: This skill is an orchestrator/router ONLY. It coordinates work but does not perform content generation.
- **Human Review**: The Context Pack output is designed for human review before article writing begins.
- **Extensibility**: If Research or Parse skills are not available, fallback to manual tool usage (web_fetch, read_file, etc.) to accomplish the same goals.
- **Quality Control**: Prioritize source attribution and risk flagging to ensure downstream content is trustworthy.
