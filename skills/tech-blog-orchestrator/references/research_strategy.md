# Research Strategy for Technical Blog Orchestrator

## Overview

This reference provides guidance on conducting effective online research when a topic is provided for technical blog content orchestration. Focus on gathering high-quality, verifiable information relevant to your specific technical/B2B industry — replace the bracketed placeholders below with your own product category, performance dimensions, and target deployment scenarios.

## Research Objectives

When conducting research for a blog topic, aim to gather:

1. **Industry Context**: Current trends, market size, competitive landscape
2. **Technical Information**: Specifications, standards, best practices
3. **Use Cases**: Real-world applications and case studies
4. **Challenges & Solutions**: Common problems and how they're addressed
5. **Innovation Trends**: Emerging technologies and future directions

## Research Workflow

### Step 1: Define Research Scope

Based on the user's topic, identify specific research questions:

**Example Topic**: "[Product/Technology] for [Extreme-Condition Deployment Scenario]"

**Research Questions**:
- What are the typical [resource/output] requirements for [target deployment scenario]?
- What [condition] ranges does [target deployment scenario] experience?
- What are the current [product category] solutions used in [extreme-condition environments]?
- What are the failure modes of conventional [product category] under [extreme condition]?
- What are the key performance metrics for [product category] in this application?

### Step 2: Conduct Targeted Searches

Use web search and web_fetch tools to gather information:

**Search Strategy**:
1. **Technical specifications**: "[product category] [extreme condition threshold] performance", "[product category] [extreme-condition] specifications"
2. **Industry standards**: "[product category] [extreme-condition] standards", "[standards body] [product category] [condition] rating"
3. **Use cases**: "[deployment scenario] power/system requirements", "[extreme-environment] [product category] solutions"
4. **Competitive landscape**: "[product category] manufacturers", "[extreme-condition] [product category] comparison"
5. **Academic research**: "[product category] [extreme condition] research paper"

**Prioritize Sources**:
- Academic journals and papers (high credibility)
- Industry standards organizations (ISO, IEC, etc.)
- Manufacturer technical datasheets
- Government research institutions
- Industry trade publications
- Reputable tech news sites

### Step 3: Extract Key Information

For each source, extract:

**Key Claims**:
- Specific technical claims with numbers (e.g., "operates at [extreme threshold]")
- Comparative statements (e.g., "50% better than conventional [product category]")
- Limitations or constraints (e.g., "requires [special core material/component]")

**Data Points**:
- Performance metrics (capacity, voltage, discharge rate)
- Environmental specifications (temperature range, humidity)
- Regulatory compliance (certifications, standards)
- Market data (growth rate, market size, adoption rate)

**Context**:
- Why this information matters to the target audience
- How it relates to your product's core value proposition
- What problems it solves

### Step 4: Verify and Cross-Reference

**Verification Checklist**:
- [ ] Is the source credible and recent?
- [ ] Can the claim be verified from multiple sources?
- [ ] Are numbers and specifications consistent across sources?
- [ ] Is the information relevant to your [target deployment scenario]?
- [ ] Does this align with known product advantages ([core capability])?

**Conflict Resolution**:
- If sources disagree, flag in risk_notes with all perspectives
- Prefer primary sources (research papers, standards) over secondary (news articles)
- Note the date of information if specifications may have changed

## Information Organization

### Key Claims Structure

Format each claim with full traceability:

```json
{
  "claim": "[Our solution category] can operate efficiently at [extreme condition threshold] without [auxiliary system]",
  "source": "[Journal name], Vol. [N], [year], https://...",
  "confidence": "high",
  "relevance": "Directly supports core product advantage",
  "context": "Conventional [product category] requires [auxiliary systems] that add weight and consume resources"
}
```

### Glossary Building

Extract and define technical terms for the target audience:

```json
{
  "term": "[Core Capability Term, e.g., Direct-Charge Operation]",
  "definition": "[Definition of the capability — what it lets the product do without an auxiliary system, even under extreme conditions]",
  "context": "Critical for [target deployment scenario] where [auxiliary systems] add complexity and cost",
  "audience_note": "Engineers will understand the technical benefit; procurement needs to know it reduces system complexity"
}
```

## Industry-Specific Research Focus

For [your product category] content, prioritize (replace each bracketed item with the dimension that matters for your product):

### 1. Technical Performance
- Operating [condition] range
- [Performance metric] retention under [extreme condition]
- [Secondary capability] rates under [extreme condition]
- [Longevity metric] in extreme environments
- Safety characteristics ([failure mode], etc.)

### 2. Application Scenarios
- [Most-extreme deployment scenario, e.g., remote/polar installations]
- [Deployment scenario 2, e.g., cold storage facilities]
- [Deployment scenario 3, e.g., high-altitude communications equipment]
- [Deployment scenario 4, e.g., aerospace and transportation systems]
- [Deployment scenario 5, e.g., region-specific infrastructure]
- [Deployment scenario 6, e.g., outdoor industrial infrastructure]

### 3. Competitive Advantages
- Comparison with [auxiliary-system-dependent] systems
- Cost-benefit analysis (no [auxiliary system] = lower complexity)
- [Resource] efficiency improvements
- Weight and space savings
- Reliability and maintenance advantages

### 4. Market Intelligence
- Market size and growth projections for [target deployment segment]
- Key competitors and their solutions
- Regulatory requirements in target markets
- Customer pain points in current solutions
- Emerging applications and opportunities

### 5. Technical Challenges
- [Core material/formulation] for [extreme condition]
- [Component A/Component B] choices for extreme-condition performance
- [Control system] requirements
- Safety testing and certification
- Manufacturing considerations

## Research Quality Standards

### High-Quality Sources (Preferred)
- Peer-reviewed academic papers (IEEE, Elsevier, etc.)
- Industry standards (IEC, ISO, SAE)
- Government research labs (DOE, NASA, NREL)
- Manufacturer technical white papers
- Industry analyst reports (Gartner, IDC, etc.)

### Medium-Quality Sources (Use with Caution)
- Industry trade publications
- Technology news sites (TechCrunch, ArsTechnica)
- Company press releases
- Conference proceedings
- Patents and patent applications

### Low-Quality Sources (Flag as Low Confidence)
- General news sites without technical expertise
- Blog posts without citations
- Marketing materials without technical details
- Social media posts
- Unverified user forums

## Risk Flagging During Research

Flag the following scenarios in risk_notes:

1. **Conflicting Information**:
   ```json
   {
     "issue": "Operating [condition] range varies across sources",
     "reason": "Source A claims [threshold A], Source B claims [threshold B]",
     "recommendation": "Verify with product engineering team for accurate specification"
   }
   ```

2. **Outdated Information**:
   ```json
   {
     "issue": "Most research papers are from 2018-2020",
     "reason": "[Product category] technology evolves rapidly; newer solutions may exist",
     "recommendation": "Search for 2023-2024 publications or contact manufacturers"
   }
   ```

3. **Unverified Claims**:
   ```json
   {
     "issue": "Single source claims 'industry-leading performance'",
     "reason": "No independent verification or comparative data",
     "recommendation": "Seek third-party test results or certifications"
   }
   ```

4. **Missing Context**:
   ```json
   {
     "issue": "Technical specification lacks testing conditions",
     "reason": "Performance at [extreme threshold] mentioned but no [test parameter, e.g. rate/load] specified",
     "recommendation": "Clarify testing methodology and conditions"
   }
   ```

## Integration with Context Pack

Map research findings to Context Pack fields:

```json
{
  "topic": "Extracted from user input",
  "key_claims": [
    /* All verified claims from research with sources */
  ],
  "glossary": [
    /* Technical terms encountered and defined */
  ],
  "risk_notes": [
    /* Any uncertainties or verification needs */
  ],
  "research_summary": {
    "sources_count": 15,
    "last_updated": "[YYYY-MM-DDTHH:MM:SSZ]",
    "key_findings": [
      "[Deployment scenario] requires [resource range] continuous [output]",
      "Conventional [product category] loses [X]% [performance metric] below [threshold]",
      "[Our solution] eliminates [X]% of system weight from [auxiliary system]",
      "Market for [target deployment segment] growing at [X]% CAGR",
      "Key certifications: [Standard 1], [Standard 2], [Standard 3]"
    ]
  }
}
```

## Example Research Output

**Topic**: "[Product/Technology] for [Target Deployment Scenario] Backup/Support Systems"

**Research Process**:
1. Search: "[deployment scenario] [resource] backup requirements"
2. Search: "[extreme-condition environment] [product category] systems"
3. Search: "[product category] [target industry] backup specifications"
4. Extract technical requirements, market data, competitive solutions
5. Identify key terms (OPEX, CAPEX, TCO, [industry-specific acronyms], etc.)
6. Flag any conflicting specifications or uncertain claims

**Output to Context Pack**:
```json
{
  "key_claims": [
    {
      "claim": "[Deployment scenario] requires [resource spec] with [duration] runtime",
      "source": "[Standards body] [standard number] specification, https://...",
      "confidence": "high"
    },
    {
      "claim": "[Extreme-condition] deployments face [X]% higher operational costs due to [auxiliary system]",
      "source": "[Industry report name] [year], https://...",
      "confidence": "medium"
    }
  ],
  "glossary": [
    {
      "term": "OPEX",
      "definition": "Operational Expenditure - ongoing costs to run and maintain equipment",
      "context": "[Our solution] reduces OPEX by eliminating [auxiliary systems]"
    }
  ],
  "research_summary": {
    "sources_count": 12,
    "key_findings": [
      "[Industry trend] increases the number of remote sites in [extreme-condition regions]",
      "[Auxiliary system] can consume [X-Y]% of total site [resource]",
      "[Our solution] reduces TCO by [X-Y]% over [N] years",
      "Market size: $[X]B for [target deployment segment] by [year]"
    ]
  }
}
```

## Tools and Techniques

**Recommended Tools**:
- `web_fetch`: For retrieving specific URLs and extracting content
- Web search: For broad information gathering
- PDF reader: For accessing research papers and technical documents
- Translation: For accessing Chinese-language technical resources

**Search Tips**:
- Use quotation marks for exact phrases: "[product category] [extreme condition]"
- Use site: operator for specific domains: site:ieee.org [product category] [condition keyword]
- Use date filters to get recent information
- Search in both English and Chinese for comprehensive coverage

**Efficiency Tips**:
- Conduct multiple searches in parallel when possible
- Cache or save key information to avoid re-searching
- Build a library of trusted sources for the industry
- Create search templates for common research topics
