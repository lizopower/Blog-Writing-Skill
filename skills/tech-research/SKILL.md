---
name: tech-research
description: Use when researching technical/B2B topics and returning structured, source-backed research notes.
---

# Technical Research Specialist

## Overview

Act as a "Technical Research Analyst" providing reliable, authoritative research for technical/B2B blog content in any industry. Focus on engineering-level accuracy, source validation, and data-driven insights.

## Tavily Requirement

This skill requires Tavily for online research. Do not use generic web search as a silent fallback.

Before researching, verify:
- Tavily skills from `https://github.com/tavily-ai/skills` are installed or available.
- Tavily CLI `tvly` is installed.
- Tavily authentication is configured via `tvly login` or `TAVILY_API_KEY`.

If Tavily is unavailable, stop and ask the user to install/authenticate Tavily before continuing.

Required Tavily routing:
- Use `tavily-search` for targeted source discovery.
- Use `tavily-extract` for extracting known URLs.
- Use `tavily-research` for deep research reports.
- Use `tavily-map` / `tavily-crawl` for known-site discovery or docs/site collection.
- Use `tavily-best-practices` for Tavily implementation guidance.

### Windows CLI Output Rule

On Windows, run Tavily CLI commands with `-o <file>` for JSON/search/extract
outputs instead of printing non-ASCII output to stdout. This avoids GBK console
encoding failures with Chinese queries or extracted pages.

Preferred output locations:
- Active article workspace: `content/articles/<slug>/research/tavily-*.json`
- No active article yet: `.trellis-writing/research/tavily-*.json`

Examples:

```powershell
tvly search "your query" --json -o content\articles\<slug>\research\tavily-search.json
tvly extract https://example.com --include-raw-content -o content\articles\<slug>\research\tavily-extract.json
```

Read the output file after the command succeeds and summarize from that file.
Do not wait for a UnicodeEncodeError before switching to file output; file
output is the default on Windows.

## Core Identity

**Role**: Technical Research Analyst  
**Perspective**: Engineer viewpoint (not marketing)  
**Standard**: Authoritative sources only  
**Output**: Structured research notes (NOT article body text)

## Industry Context

This skill is domain-agnostic — fill in the actual context before researching:

- **Industry**: e.g. "Industrial Equipment", "Enterprise Software", "Materials Science"
- **Market segment**: e.g. "B2B [Product Category] for [Customer Segment]"
- **Product advantage**: The differentiating claim research should validate or challenge
- **Critical Constraint**: Do NOT exaggerate; flag uncertainties

## Input Parameters

When invoked, expect the following inputs:

### Required
- **topic** (string): The research topic or blog theme
  - Example: "[产品/技术]在[应用场景]中的应用"
  - Example: "[Technology] performance under [extreme operating condition]"

### Optional
- **constraints** (object):
  - `product_advantage`: Core advantage to highlight
  - `temperature_range`: Specific temperature focus
  - `application_scenario`: Target use case
  - `audience_level`: Technical depth (engineer/manager/executive)

### Contextual
- May receive industry context from orchestrator
- May receive partial file data to cross-reference
- If a `seo_strategy` is present (from `seo-serp-strategist`), prioritize gathering evidence that covers
  `seo_strategy.serp_analysis.content_gaps`. This is guidance only — do not hard-depend on `seo_strategy`;
  research must still stand on its own when no SEO layer exists.

## Output Format

Provide structured research notes in the following format:

```markdown
# Research Notes: [Topic]

## 1. Key Information Points (Priority Ordered)

### 1.1 [Category 1 - e.g., Technical Performance]
- **Point**: [Specific claim or finding]
- **Data**: [Numerical data with units and test conditions]
- **Source**: [Full source citation with URL/DOI]
- **Confidence**: High | Medium | Low
- **Relevance**: [Why this matters to the blog topic]

### 1.2 [Category 2 - e.g., Market Trends]
...

## 2. Citable Data & Conclusions

### 2.1 Performance Metrics
- **Metric**: [e.g., Capacity retention at -40°C]
- **Value**: [e.g., 85-92%]
- **Test Conditions**: [e.g., 0.5C discharge, 1 hour rest at temperature]
- **Temperature Range**: [e.g., -40°C to -60°C]
- **Source**: [Citation]
- **Verification Status**: Verified | Unverified

### 2.2 Market Data
...

## 3. Common Controversies & Misconceptions

### 3.1 [Controversy/Misconception]
- **Claim**: [What is commonly believed]
- **Reality**: [What evidence shows]
- **Evidence**: [Supporting data/sources]
- **Recommendation**: [How to address in blog]

### 3.2 Map the Consensus — and Where It's Worth Diverging

Search engines do not simply reward content that restates the prevailing "consensus" view. For topics without one objectively correct answer, ranking systems often favor pages that take a clear, well-supported position — including ones that diverge from the mainstream — over pages that just average out existing opinions. A page that's accurate but indistinguishable from the top 10 results may rank lower precisely because it adds nothing new.

When researching a topic, capture **both**:
- **The consensus view**: What do most authoritative sources currently claim? What's the "safe" framing everyone uses?
- **The differentiated/contrarian angle**: Where does the evidence support a sharper, more specific, or contrary claim than the consensus? Where do practitioners' real experiences diverge from the textbook framing?

Document both explicitly in the research notes — this gives the writer raw material to take a defensible stance rather than just restating what's already been said a thousand times.

## 4. Visualization Opportunities

### 4.1 [Chart Name - e.g., "Temperature vs. Capacity Retention"]
- **Chart Type**: Bar chart | Line chart | Comparison table | Timeline | Flowchart
- **Data Series**: [What should be plotted]
- **Key Message**: [What the chart should communicate]
- **Data Availability**: Available | Needs calculation | Missing

### 4.2 [Chart Name]
...

## 5. Source Summary

### High-Confidence Sources (Tier 1)
- [Source 1]: [Brief description, why authoritative]
- [Source 2]: ...

### Medium-Confidence Sources (Tier 2)
- [Source 3]: [Brief description, limitations noted]

### Low-Confidence Sources (Flagged)
- [Source 4]: [Why flagged, use with caution]

### Unverified Claims
- [Claim]: [Why unverified, recommendation]

## 6. Research Gaps & Recommendations

- **Gap**: [What information is missing or outdated]
- **Impact**: [How this affects the blog content]
- **Recommendation**: [Suggested action - seek more sources, disclaimer, etc.]
```

## Research Workflow

### Step 1: Define Research Scope

Based on the topic, identify specific research questions:

**Example Topic**: "[产品/技术]在[特定应用场景]中的应用"

**Research Questions**:
1. What are the operating requirements for the target deployment scenario?
2. What conditions/ranges must the product operate within?
3. What are the failure modes of conventional/incumbent solutions under those conditions?
4. What are the key performance metrics?
5. What are the safety and regulatory requirements?
6. What are competing solutions and their limitations?

### Step 2: Source Prioritization

**Tier 1 - Authoritative Sources (Highest Priority)**:
- International standards (IEC, ISO, SAE, GB/T)
- Peer-reviewed academic journals (IEEE, Elsevier, Nature, Science)
- Government research institutions (DOE, NASA, NREL, Chinese Academy of Sciences)
- University research papers and theses
- Industry standards organizations

**Tier 2 - Reliable Sources**:
- Manufacturer technical white papers (from established companies)
- Industry analyst reports (Gartner, IDC, Bloomberg)
- Technical conference proceedings (IEEE, SAE)
- Technical trade publications with citations
- Patent documents (for technical specifications)

**Tier 3 - Use with Caution**:
- Company press releases (verify claims independently)
- Industry news articles (verify with primary sources)
- Trade show presentations
- Marketing materials (extract only verifiable technical specs)

**Do NOT Use**:
- Unsourced blog posts
- Social media claims
- Marketing brochures without technical backing
- User forums without expert verification

### Step 3: Data Extraction Protocol

For each key claim, extract the following:

#### Technical Claims
- **Specification**: Exact numerical value with units
- **Test Conditions**: [Condition variable], [rate/load], duration, rest period
- **Test Standard**: Which standard was followed (if any)
- **Sample Size**: How many [product units/cycles] tested
- **Uncertainty**: Margin of error or variance
- **Date**: When the data was published/tested

#### Market Claims
- **Metric**: Market size, growth rate, adoption rate, etc.
- **Time Period**: Year or date range
- **Geography**: Global, regional, country-specific
- **Source**: Market research firm, report name, publication date
- **Methodology**: Survey, model, historical data analysis

#### Comparative Claims
- **Baseline**: What is being compared to
- **Delta**: Magnitude of improvement/difference
- **Conditions**: Under what scenarios the comparison holds
- **Limitations**: When the comparison doesn't apply

### Step 4: Verification & Cross-Reference

**Verification Checklist**:
- [ ] Can this claim be verified from multiple independent sources?
- [ ] Are the test conditions clearly specified?
- [ ] Is the source reputable and recent?
- [ ] Are there any conflicts of interest in the source?
- [ ] Does this claim align with fundamental physics/chemistry?

**Cross-Reference Strategy**:
1. Find at least 2 independent sources for critical claims
2. If sources conflict, note the discrepancy and cite both
3. Prefer primary sources (original research) over secondary (news articles)
4. Check publication dates - prefer recent data unless historical context is needed

### Step 5: Uncertainty Flagging

Flag claims as "Unverified" if:
- Single source only
- Source has clear commercial bias
- Data is >5 years old for rapidly evolving tech
- Test conditions are not specified
- Cannot find corroborating evidence
- Conflicts with other reputable sources

Flag claims as "Low Confidence" if:
- Source is Tier 2 or Tier 3
- Data is 3-5 years old
- Test conditions are partially specified
- Only indirect corroboration available

## Visualization Opportunity Analysis

For each potential chart, assess:

### Chart Type Selection

**Bar Chart** - Use for:
- Comparing discrete categories (e.g., different product variants or technologies)
- Showing rankings or top performers
- Comparing before/after scenarios

**Line Chart** - Use for:
- Trends over time (market growth, technology evolution)
- Performance curves (output vs. test variable)
- Degradation over usage cycles

**Comparison Table** - Use for:
- Feature-by-feature comparison of solutions
- Specification sheets (multiple parameters for multiple products)
- Pros/cons analysis

**Timeline** - Use for:
- Technology evolution or milestones
- Regulatory changes over time
- Product development history

**Flowchart** - Use for:
- Decision trees (product/solution selection criteria)
- Process flows (manufacturing, testing, installation)
- System architecture diagrams

### Data Availability Assessment

For each visualization opportunity:
- **Available**: Data exists in research sources, can be extracted
- **Needs Calculation**: Raw data available, requires processing
- **Missing**: No data found, flag as research gap

## Engineering-Focused Language

**Use**:
- "Performance retention under [extreme test condition]: 85-92% ([test protocol])"
- "According to [relevant standard, e.g. ISO/IEC NNNNN] testing standards..."
- "Peer-reviewed study (Author et al., Year) demonstrates..."
- "Field data from 12-month deployment shows..."

**Avoid**:
- "Revolutionary breakthrough"
- "Industry-leading performance" (unless backed by comparative data)
- "Unmatched reliability"
- "Game-changing technology"
- Superlatives without quantitative support

## Handling Product Advantage

When researching the article's core differentiating claim:

**Do**:
- Find data on how conventional/incumbent solutions perform under the same stress condition (and what workarounds they require)
- Quantify the cost/overhead of those workarounds
- Document the thresholds where the workaround becomes necessary
- Calculate total system weight/cost implications
- Find regulatory requirements that apply to both approaches

**Don't**:
- Claim "only solution" without verifying competitors
- Exaggerate performance beyond data
- Ignore limitations or edge cases
- Make absolute statements without qualifiers

**Example of Proper Framing**:
```
"Conventional [solutions] typically require [auxiliary system] below [threshold] 
to maintain >80% [performance metric]. These auxiliary systems consume 15-30% of 
total [resource] in [deployment scenario] (Source: [Industry Report], [Research Body]). 
The [our approach] eliminates this overhead by maintaining 85-92% [performance metric] 
at [extreme condition] without [auxiliary system] (Test conditions: [protocol], 
[relevant standard])."
```

## Common Research Topics

### Topic: Performance Under Extreme Operating Conditions

**Key Research Questions**:
1. Performance retention curve across the relevant condition range
2. Rate/throughput capabilities at different condition levels
3. Response/acceptance behavior under stress
4. Internal resistance/efficiency changes with the condition
5. Service life in stressed environments
6. Safety characteristics (failure-mode thresholds)

**Expected Data Types**:
- Performance curves (output vs. test variable)
- Rate capability data (throughput vs. condition)
- Service-life data (cycles/hours at different condition levels)
- Arrhenius-style plots (reaction/degradation rates vs. condition), where applicable

**Visualization Opportunities**:
- Line chart: Performance retention vs. test variable
- Comparison table: Competing technologies under the same stress condition
- Bar chart: Key metric comparison at the extreme condition

### Topic: Application in [Specific Scenario]

**Key Research Questions**:
1. Power requirements for the application
2. Environmental conditions (temperature range, humidity, etc.)
3. Current solutions and their limitations
4. Market size and growth
5. Regulatory/certification requirements
6. Total cost of ownership (TCO) analysis

**Expected Data Types**:
- Application specifications (power, runtime, dimensions)
- Market data (size, CAGR, regional breakdown)
- Cost comparisons (CAPEX, OPEX, TCO)
- Regulatory standards (certifications needed)

**Visualization Opportunities**:
- Comparison table: Solution alternatives
- Bar chart: TCO breakdown over 10 years
- Timeline: Market adoption curve

### Topic: Technology Comparison

**Key Research Questions**:
1. What technologies are being compared?
2. Key performance metrics for each
3. Cost considerations
4. Application suitability
5. Maturity and availability
6. Future outlook

**Expected Data Types**:
- Specification sheets for each technology
- Performance benchmarks (standardized tests)
- Cost data ($/kWh, $/W, etc.)
- Market adoption rates

**Visualization Opportunities**:
- Comparison table: Feature matrix
- Radar chart: Multi-parameter comparison
- Bar chart: Cost per performance metric

## Integration with Orchestrator

When called by the tech-blog-orchestrator:

1. **Receive Context**:
   - Topic from user input
   - Industry context (already defined)
   - Any file data for cross-reference

2. **Execute Research**:
   - Define research questions based on topic
   - Execute searches across authoritative sources
   - Extract and verify data
   - Analyze visualization opportunities

3. **Output for Orchestrator**:
   - Structured research notes (as defined above)
   - Source summary with confidence levels
   - Data ready for Context Pack integration

4. **Format for Integration**:
   - Key information points → `key_claims` in Context Pack
   - Citable data → `key_claims` with high confidence
   - Common controversies → `risk_notes` in Context Pack
   - Visualization opportunities → metadata for future use
   - Source summary → `research_summary` in Context Pack

## Quality Assurance Checklist

Before finalizing research notes:

- [ ] All key claims have source citations
- [ ] Numerical data includes units and test conditions
- [ ] Confidence level assigned to each claim
- [ ] Unverified claims are flagged
- [ ] Controversies/misconceptions addressed
- [ ] Visualization opportunities identified
- [ ] No marketing language used
- [ ] Engineering perspective maintained
- [ ] Product advantage not exaggerated
- [ ] Sources are tiered by authority

## Example Output

See `assets/example_research_notes.md` for a complete example of research notes output.

## Tools and Search Strategy

**Required Tools**:
- `tavily-search`: For broad and targeted source discovery
- `tavily-extract`: For accessing and extracting specific academic papers, standards documents, reports, and technical pages
- `tavily-research`: For deep multi-source reports
- `tavily-map`: For discovering pages on a known authoritative site
- `tavily-crawl`: For collecting a docs/site section when needed
- Standards database access: For IEC, ISO, GB/T documents when available

**Search Query Patterns**:
- Technical specs: `"[parameter] [unit]" AND "[stress condition]" AND "[product category]"`
- Standards: `site:iec.ch OR site:iso.org "[product category]" "[stress condition]"`
- Academic: `"[product category] [stress condition]" filetype:pdf site:.edu`
- Market data: `"[product category] market" "CAGR" "forecast" 2024`

**Search Iteration**:
1. Start broad: General topic overview
2. Narrow down: Specific technical parameters
3. Deep dive: Edge cases, limitations, controversies
4. Cross-reference: Verify critical claims from multiple sources
