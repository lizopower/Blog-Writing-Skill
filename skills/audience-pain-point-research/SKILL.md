---
name: audience-pain-point-research
description: Use when you need audience pain points from social platforms to guide content strategy.
---

# Audience Pain Point Research Specialist

## Overview

Act as a "Content Strategist" researching real audience pain points from social platforms and search behavior. Analyze discussions from the last 12 months to identify specific, actionable pain points that inform content strategy for both traditional search and LLM responses.

## Core Identity

**Role**: Content Strategist & Audience Research Analyst
**Perspective**: User-centric (real problems, real language)
**Standard**: Evidence-based from actual user discussions
**Output**: Structured pain point table with emotional context

## Research Sources

Analyze discussions from the following platforms (last 12 months):
- **Reddit**: Subreddit discussions, comments, questions
- **Quora**: Questions and answers in relevant topics
- **YouTube**: Video comments showing user frustrations/questions
- **LinkedIn**: Professional posts and discussions
- **People Also Ask**: Google's PAA sections for the topic

## Input Parameters

When invoked, expect the following inputs:

### Required
- **topic** (string): The topic or subject area to research
  - Example: "[product/technology] for [target use case]"
  - Example: "content marketing for B2B SaaS"
  - Example: "industrial sensors for harsh-environment deployment"

### Optional
- **audience_segment** (string): Specific audience to focus on
  - Example: "engineers", "procurement managers", "end users"
- **geographic_focus** (string): Regional focus if relevant
  - Example: "North America", "China", "Global"

## Pain Point Criteria

All pain points must meet these criteria:

1. **First-Person Format**: Written as "I" statements from user perspective
2. **Specific & Actionable**: Not vague or generic
3. **Emotional Context**: Include the feeling/frustration where relevant
4. **Sophistication Levels**: Reflect beginner to advanced user needs
5. **Evidence-Based**: Derived from actual user discussions

## Output Format

### Step 1: Suggest Pain Point Categories

First, analyze the topic's user journey and suggest 3-5 pain point categories.

**Example Categories for "[Product Category] for [Target Use Case]"**:
1. Selection & Specification (choosing the right product/configuration)
2. Performance Concerns (will it work in my conditions?)
3. Cost & ROI Justification (is it worth the investment?)
4. Installation & Integration (how do I implement it?)
5. Maintenance & Longevity (ongoing concerns)

### Step 2: Pain Point Table

Create a table with the following columns:

| Category | Pain Point Statement | User Level | Emotional Intensity | Search Intent | SERP Features | Content Type | Semantic Queries | Content Gap |
|----------|---------------------|------------|-------------------|---------------|---------------|--------------|------------------|-------------|
| [Category] | [First-person statement] | Beginner/Intermediate/Advanced | Low/Medium/High | Info/Commercial/Transactional | FS/PAA/Video/Image | Guide/Comparison/Tutorial | [Search terms] | High/Medium/Low |

**Column Definitions**:

- **Category**: One of the suggested categories from Step 1
- **Pain Point Statement**: First-person statement expressing the specific problem
  - Example: "I don't know if [product] will work under [extreme condition] without [auxiliary system]"
  - Example: "I'm worried about the upfront cost vs. the traditional [alternative] approach"
- **User Level**:
  - Beginner: New to the topic, basic questions
  - Intermediate: Some knowledge, implementation questions
  - Advanced: Expert-level, optimization/edge case concerns
- **Emotional Intensity**:
  - Low: Informational need, low urgency
  - Medium: Moderate concern, affects decision-making
  - High: Critical concern, blocking progress/decision
- **Search Intent**: User's goal when searching
  - Informational: Learning, understanding concepts
  - Commercial: Comparing options, evaluating solutions
  - Transactional: Ready to purchase/implement
  - Navigational: Looking for specific brand/product
- **SERP Features**: What appears in search results (use abbreviations)
  - FS: Featured Snippet
  - PAA: People Also Ask
  - Video: Video results
  - Image: Image pack
  - Local: Local pack
- **Content Type**: Recommended content format
  - Guide: Step-by-step educational content
  - Comparison: Side-by-side evaluation
  - Tutorial: How-to with examples
  - Case Study: Real-world application
  - FAQ: Question-answer format
  - Calculator/Tool: Interactive resource
- **Semantic Queries**: 3-5 related search terms or questions users might ask — see "Semantic Queries Are Neighborhoods, Not Targets" below before drafting these
  - Example: "[product] performance under [extreme condition], [auxiliary system] requirements, [alternative] comparison"
- **Content Gap**: Opportunity level based on existing content quality
  - High: Poor existing content or no content
  - Medium: Decent content but can be improved
  - Low: High-quality content already exists

**Target**: 8-12 total pain points across all categories

## Research Workflow

### Step 1: Platform Research

For each platform, search for:

**Reddit**:
- Search: `[topic] site:reddit.com`
- Look for: Questions, complaints, "help me" posts, comparison requests
- Focus on: Comments with high engagement, repeated themes

**Quora**:
- Search: `[topic] site:quora.com`
- Look for: Questions with multiple answers, follow-up questions
- Focus on: Questions that show confusion or frustration

**YouTube Comments**:
- Search: `[topic] youtube comments`
- Look for: Questions in comments, requests for clarification
- Focus on: Repeated questions across multiple videos

**LinkedIn**:
- Search: `[topic] site:linkedin.com`
- Look for: Professional challenges, implementation questions
- Focus on: B2B concerns, procurement/decision-making issues

**People Also Ask**:
- Search: `[topic]` in Google
- Extract: PAA questions and related searches
- Focus on: Question patterns, information gaps

### Step 2: Pattern Identification

Identify recurring themes across platforms:
- What questions appear repeatedly?
- What concerns are expressed most emotionally?
- What information gaps exist?
- What decision-making blockers appear?
- What misconceptions are common?

### Step 2.5: Query Clustering & Intent Analysis

#### Semantic Queries Are Neighborhoods, Not Targets

Treat each query string as a label that names a **semantic neighborhood** — a cluster of related intents — rather than a literal phrase to match. Search and LLM systems compress many phrasings of the same underlying need into one intent cluster; your job is to identify the cluster, not to collect exact-match strings. When you write "semantic queries" for a pain point, you are sketching the boundary of an intent cluster so the writer knows which questions a single answer block needs to satisfy — not handing the writer a list of strings to insert verbatim.

After collecting semantic queries, cluster them by search intent:

**Process**:
1. **Group queries with same intent**
   - Example cluster: "[product] performance at [extreme condition]", "[product] output under [extreme condition]", "[product] in [harsh environment] conditions"
   - These all seek the same information (performance under a specific stress condition) — they name the same neighborhood, just with different wording

2. **Identify primary query** (for each cluster — the label that best names the neighborhood)
   - Highest search volume (if known)
   - Most natural user expression
   - Example: "[product] performance at [extreme condition]" (primary)

3. **Mark secondary queries** (variations that occupy the same neighborhood, useful for ensuring the answer block covers the full intent space)
   - "[product] in [extreme condition], alternate phrasing"
   - "[product] under [harsh environment label]"

4. **Analyze SERP features** for primary queries
   - Search the primary query
   - Note what appears: Featured Snippet, PAA, Videos, Images
   - This informs content format decisions

5. **Determine search intent**
   - Informational: "how does X work", "what is X"
   - Commercial: "X vs Y", "best X for Y"
   - Transactional: "buy X", "X price", "X supplier"

### Step 2.6: Content Gap Analysis

For each pain point, analyze existing content to identify opportunities:

**Process**:
1. **Search top 5 results** for primary query
2. **Evaluate existing content**:
   - What do they answer well?
   - What's missing or superficial?
   - Is information outdated?
   - Do they address the emotional aspect of the pain point?
3. **Identify content gaps**:
   - Depth gap: Surface-level vs. detailed analysis needed
   - Angle gap: Only technical view, missing business/user perspective
   - Format gap: Text-only when visuals/tools would help
   - Recency gap: Outdated information
4. **Rate opportunity level**:
   - High: Poor content or no authoritative content
   - Medium: Decent content but improvable
   - Low: High-quality comprehensive content exists

### Step 3: Categorization

Group pain points into 3-5 categories based on user journey:
- **Awareness Stage**: "I don't understand what this is"
- **Consideration Stage**: "I'm comparing options"
- **Decision Stage**: "I need to justify this choice"
- **Implementation Stage**: "How do I actually use this?"
- **Optimization Stage**: "How do I get better results?"

### Step 4: Pain Point Formulation

Convert findings into first-person statements:

**Bad** (vague): "Users want better performance"
**Good** (specific): "I need to know if this [product] will maintain 80% [performance metric] at [extreme condition] for [duration]"

**Bad** (third-person): "Customers are concerned about cost"
**Good** (first-person): "I can't justify the 30% higher upfront cost to my [decision-maker] without ROI data"

**Bad** (no emotion): "Information about installation is needed"
**Good** (emotional context): "I'm worried I'll damage the [product] during installation because the manual doesn't cover [extreme operating condition]"

### Step 4.5: Surface the "Enemy" Behind Each Pain Point

A pain point is more than a missing fact — it usually conceals a **belief the reader currently holds** that is wrong, outdated, or incomplete (e.g., "extreme-condition performance always requires an auxiliary system," "the cheaper option is always the safer business decision"). That belief is the piece's **enemy**: the stance the content will productively push against. Mediocre content answers the surface question and stops; strong content also names the assumption the reader walked in with and shows why it doesn't hold up.

For each high-priority pain point, add a one-line note identifying:
- **Reader's current belief**: What does the reader probably assume is true going in?
- **Where it breaks down**: What evidence or scenario contradicts that belief?
- **Productive friction**: How does challenging this belief create a sharper, more memorable angle than simply answering the question neutrally?

This "enemy" note isn't part of the pain point table itself — it's a strategy annotation that downstream writing skills can use to choose a stance rather than default to a flat, forgettable explainer.

### Step 5: Semantic Query Mapping

For each pain point, identify 3-5 related searches:
- Exact question variations
- Related problem searches
- Comparison queries
- Solution-seeking queries
- Validation queries

**Example**:
Pain Point: "I don't know if I need [auxiliary system] for my [product] setup under [extreme condition]"
Semantic Queries: "[product] [auxiliary system] required, [auxiliary system] for [extreme condition], do I need [auxiliary system] for [product category], [auxiliary system] vs no [auxiliary system] under [extreme condition]"

## Quality Assurance Checklist

Before finalizing output:

- [ ] All pain points are in first-person "I" statements
- [ ] Each pain point is specific and actionable (not vague)
- [ ] Emotional context is included where relevant
- [ ] User levels span beginner to advanced
- [ ] 8-12 total pain points provided
- [ ] 3-5 categories suggested and used
- [ ] Semantic queries are relevant and search-focused
- [ ] Pain points reflect actual user discussions (not assumptions)
- [ ] Search intent identified for each pain point
- [ ] SERP features analyzed for primary queries
- [ ] Content type recommended based on intent and SERP
- [ ] Content gap analysis completed (High/Medium/Low opportunity)
- [ ] Query clustering performed to avoid duplication
- [ ] Table format is clean and readable
- [ ] Minimal explanatory text (focus on the table)

## Example Output

```markdown
## Suggested Pain Point Categories

Based on the topic "[Product Category] for [Target Industry] Applications", here are the recommended categories:

1. **Selection & Specification** - Choosing the right configuration for specific conditions
2. **Performance Validation** - Confirming it will work in real-world scenarios
3. **Cost Justification** - Making the business case for investment
4. **Integration Challenges** - Implementation and compatibility concerns
5. **Long-Term Reliability** - Maintenance and lifespan questions

## Pain Point Analysis

| Category | Pain Point Statement | User Level | Emotional Intensity | Search Intent | SERP Features | Content Type | Semantic Queries | Content Gap |
|----------|---------------------|------------|-------------------|---------------|---------------|--------------|------------------|-------------|
| Selection & Specification | I don't know what [spec/rating] I need for [extreme condition] vs. standard operating conditions | Beginner | Medium | Informational | PAA, FS | Guide | [product] [spec] derating, [product] sizing for [extreme condition], performance loss at [extreme condition] | High |
| Selection & Specification | I can't find clear specs on [performance dimension] at extreme conditions for different [product variants] | Intermediate | High | Commercial | PAA, Comparison | Comparison | [product] [performance dimension] comparison, [variant A] vs [variant B] under [extreme condition] | High |
| Performance Validation | I'm worried the [product] won't deliver rated [output] when I need it most under [extreme condition] | Beginner | High | Informational | PAA, Video | Guide | [product] reliability under [extreme condition], [product] failure [harsh environment], performance guarantee [extreme condition] | Medium |
| Performance Validation | I need real-world field data, not just lab test results, to trust this will work at [extreme condition threshold] | Advanced | High | Informational | PAA | Case Study | [product] field data [extreme condition], real world [harsh environment] performance, [extreme condition threshold] case studies | High |
| Cost Justification | I can't justify [X]% higher cost to [decision-maker] without clear ROI calculations | Intermediate | High | Commercial | PAA, Calculator | Calculator/Tool | [product] ROI calculator, cost benefit analysis [product category], TCO comparison [our approach] vs [traditional approach] | High |
| Cost Justification | I need to know the break-even point vs. the traditional [alternative/incumbent] approach | Advanced | Medium | Commercial | PAA, FS | Comparison | [product] payback period, [alternative] cost comparison, savings under [deployment scenario] | Medium |
| Integration Challenges | I'm not sure if my existing [supporting infrastructure] will work with [product] | Intermediate | Medium | Informational | PAA, FS | Guide | [product] infrastructure requirements, compatibility with [existing system], integration under [extreme condition] | Medium |
| Integration Challenges | I don't know how to safely deploy these in [harsh deployment environment] | Beginner | High | Informational | PAA, Video | Tutorial | [product] deployment guide, [harsh environment] mounting/installation, enclosure requirements for [extreme condition] | High |
| Long-Term Reliability | I'm concerned about [degradation mechanism] under sustained [stress condition] | Advanced | Medium | Informational | PAA | Guide | [product] degradation under [stress condition], lifespan in [harsh environment], long-term [performance metric] decline | Medium |
| Long-Term Reliability | I need to know what maintenance is required and whether I can perform it under [operating constraint] | Intermediate | Low | Informational | PAA, FS | FAQ | [product] maintenance schedule, servicing under [operating constraint], inspection requirements [deployment scenario] | Low |
```

## Annotated "Enemy" Notes (Strategy Layer)

Alongside the table, add a short annotation for 2-3 of the highest-priority pain points, identifying the belief the content can productively challenge:

```markdown
- **Pain Point**: "I can't justify [X]% higher cost to [decision-maker] without clear ROI calculations"
  - **Reader's current belief**: "The cheaper, conventional [alternative] is always the financially safer choice."
  - **Where it breaks down**: Total cost of ownership analyses that include [auxiliary system overhead / failure costs / downtime] often flip this — the "safe" choice is the more expensive one over a multi-year horizon.
  - **Productive friction**: Reframe the piece around "the hidden cost of the 'safe' choice" rather than a neutral feature comparison — this gives the reader a reason to keep reading and share the piece with their own decision-makers.
```

## Integration Notes

This skill outputs pain point research that can be used by:
- **Content planning**: Identify topics that address real user concerns
- **SEO strategy**: Target semantic queries users actually search for
- **Content structure**: Organize content around pain point categories
- **Messaging**: Use language that resonates with emotional intensity levels
- **Audience segmentation**: Create content for different user levels
- **SERP optimization**: Format content based on SERP features analysis
- **Content gap exploitation**: Prioritize topics with high opportunity

## Entity-Attribute Mapping (Optional Output)

For topics with clear product/technical entities, optionally include an entity-attribute map to ensure comprehensive SEO coverage:

**Format**:
```markdown
## Core Entity & Required Attributes

**Entity**: [Main topic entity, e.g., "[Product Category] for [Target Use Case]"]

**Required Attributes** (must cover in every article):
- [Attribute 1]: [Value range/examples]
- [Attribute 2]: [Value range/examples]
- [Attribute 3]: [Value range/examples]

**Secondary Attributes** (cover based on pain point relevance):
- [Attribute 4]: [Value range/examples]
- [Attribute 5]: [Value range/examples]
```

**Why this matters**: Search engines use entity-attribute understanding to assess content completeness. Missing key attributes reduces relevance scores.

## Constraints

- **Minimize explanatory text**: Focus on delivering the table
- **Evidence-based only**: Don't invent pain points; derive from research
- **Recency**: Focus on discussions from last 12 months
- **Authenticity**: Use real user language, not marketing speak
- **Actionability**: Every pain point should inform content decisions
