# Tech-Blog-Writer Style Guide

**Detailed formatting and style reference for technical article writing**

---

## Overview

This style guide provides detailed formatting rules, tone guidelines, and examples for writing engineer-to-engineer technical content. The examples below use bracketed placeholders (`[product]`, `[extreme condition]`, `[performance metric]`) — replace them with your own product category and domain specifics; the formatting and tone rules apply to any technical/B2B industry.

---

## Core Principles

1. **Engineer-to-Engineer**: Write for technical decision-makers who will verify every claim
2. **Data-Driven**: Every quantitative statement must have a source
3. **Actionable**: Provide checklists, tables, formulas, and decision frameworks
4. **Transparent**: Explicitly mark assumptions and data gaps
5. **No Marketing Fluff**: Direct, verifiable language only

---

## Tone & Voice

### ✅ Preferred Tone

**Characteristics**:
- Direct and clear
- Technically precise
- Consultative (not promotional)
- Balanced (acknowledges trade-offs)
- Honest about limitations

**Example**:
> Testing shows [Z]% [performance metric] retention at [extreme threshold] under [test parameter] (PDF p.[N], Table [N]). This represents a significant improvement over standard units (<[W]% at this condition), but comes with a [X-Y]% cost premium (Sheet:CostAnalysis).

### ❌ Avoid

**Characteristics**:
- Marketing superlatives
- Unqualified claims
- Promotional language
- One-sided comparisons
- Unsupported assertions

**Example (Don't do this)**:
> Our revolutionary [products] are the best solution for [extreme conditions], delivering amazing performance that blows away the competition!

---

## Label lines repealed (plain-language override)

Signal-word label lines (`**Key Insight:**`, `**Non-negotiable:**`, `**Common Mistake:**`, `**Trade-off:**`, and similar) are **repealed**. See `content/specs/writing-plain-language.md`.

Put the same meaning in a complete sentence. Bold a short clause inside the sentence if you need stress.

**Examples (use these shapes)**:

> The [performance metric] degradation is not linear. Small condition changes near [extreme threshold] cause dramatic performance shifts and define a hard operational boundary.

> Any system [triggering operation] below [threshold] must include condition-based [rate/load] limiting. Skipping it causes irreversible [degradation/damage mode].

> Do not assume [operation A] and [operation B] are symmetric. Many [products] that can [operation A] at [extreme threshold] can only safely [operation B] above [milder threshold].

### Trade-off framing (still valid as prose, not as a label)
**Purpose**: Present balanced analysis of competing factors  
**Usage**: For decision points with no clear winner — still write full sentences, not a `**Trade-off:**` label line

**Example**:
> Specialized [our-solution] units cost [X-Y]% more but eliminate [auxiliary-system] complexity. Choose based on whether your application prioritizes initial cost ([auxiliary-system-equipped] standard units) or long-term simplicity (specialized units).

---

## Formatting Standards

### Headers

**H1**: Article title only (one per document)
```markdown
# [Product Category] Selection: Complete Engineering Guide
```

**H2**: Major sections
```markdown
## Understanding [Extreme-Condition] Failure Modes
```

**H3**: Subsections
```markdown
### [Failure Mechanism] Effects
```

**Limit**: Keep total section count ≤20 (H2+H3 combined)

---

### Lists

**Bulleted Lists**: For unordered items
```markdown
Key considerations:
- Operating [condition] range
- [Secondary capability] limits
- [Longevity metric] requirements
```

**Numbered Lists**: For sequential steps or ranked items
```markdown
Implementation steps:
1. Validate [condition] requirements
2. Request vendor test data
3. Conduct sample testing
4. Finalize [control system] configuration
```

**Checklist Format**: For selection/validation tasks
```markdown
- [ ] Operating [condition] range specified
- [ ] [Control system] [monitoring parameter] sensors validated (±[X][unit] accuracy)
- [ ] [Rate/load] derating implemented
```

---

### Tables

**Comparison Tables**: For multi-variable analysis

```markdown
| Factor | Low-Temp Cells | Heated Standard Cells | Source |
|--------|----------------|----------------------|--------|
| Capacity at -40°C | 87% | 60-70% | PDF p.12 vs. p.18 |
| System Cost | +15-30% | +40-60% | Sheet:Cost / A5:C12 |
| Cold Start Time | Instant | 5-30 min | PDF p.20 |
```

**Data Tables**: For test results or specifications

```markdown
| Temperature | Capacity | Internal Resistance | Source |
|-------------|----------|---------------------|--------|
| +25°C | 100% | 15 mΩ | PDF p.10, Table 2 |
| 0°C | 98% | 18 mΩ | PDF p.10, Table 2 |
| -20°C | 92% | 28 mΩ | PDF p.11, Table 3 |
| -40°C | 87% | 45 mΩ | PDF p.12, Table 4 |
```

---

### Emphasis

**Bold**: For key clauses inside complete sentences, not as label lines
```markdown
**Temperature monitoring** is required for this duty cycle.
```

**Italic**: For emphasis or definitions (use sparingly)
```markdown
The *State of Charge* (SoC) must be monitored continuously.
```

**Code formatting**: For specifications, formulas, or structured data
```markdown
Target operating range: `-40°C to +60°C`
```

---

### Links

**Internal Links** (use placeholders):
```markdown
For detailed [control system] configuration, see [Internal Link: control-system-setup-guide].
```

**External Links** (with context):
```markdown
According to [Standard number] standards ([Standards Body Website](https://example.org)), [extreme-condition] testing requires...
```

---

## Source Attribution

### In-Text Citations

**Format**: `(Source: Type + Location)`

**Examples**:
```markdown
Testing shows [Z]% [performance metric] at [extreme threshold] (PDF p.[N], Table [N]).

Cost analysis indicates [X-Y]% premium (Sheet:CostAnalysis / Range:[cell range]).

Industry standards require safety testing below [threshold] ([standard number], Section [N]).

Field data from [extreme-deployment regions] shows [N1]-[N2] [cycles/hours] (Customer Report #[ID]).
```

### Source Types

| Source Type | Format | Example |
|-------------|--------|---------|
| PDF | `PDF p.XX, Table/Section Y` | `PDF p.12, Table 3` |
| Excel | `Sheet:Name / Range:A1:D10` | `Sheet:TestData / Range:B2:E15` |
| Word | `Word: Heading Path + Para #` | `Word: Methods > Testing > Para 3` |
| Web | `URL + Publication Info` | `[Industry Reference] ([year])` |
| Internal | `Report #ID` | `Test Report #[ID]` |

### No Source = No Number

**If source cannot be located**:
- ❌ Don't write the quantitative claim
- ✅ Rewrite qualitatively + mark "To Verify"

**Example**:
```markdown
❌ Wrong: Most applications see 20-30% cost savings.

✅ Correct: Applications with difficult maintenance access often favor simpler systems despite higher initial costs. **To Verify**: Quantitative ROI analysis requires project-specific data.
```

---

## Chart Integration

### With charts_manifest

**Full Integration**:
```markdown
![Capacity vs Temperature](chart_01)
*Figure 1: Capacity retention across temperature range (Sheet:TestResults / Range:B2:E15)*

The chart shows three distinct operating zones:
- **Zone 1 (0°C to -20°C)**: >95% capacity retention
- **Zone 2 (-20°C to -40°C)**: 87-95% capacity retention
- **Zone 3 (<-40°C)**: Rapid degradation begins

For applications that must run below -40°C, additional thermal management is required.
```

**Components**:
1. Image reference: `![Alt Text](chart_id)`
2. Caption: `*Figure X: Description (Source)*`
3. Explanation: What it shows + implications
4. Action: What decision-makers should do

### Without charts_manifest

**Placeholder**:
```markdown
[Chart TBD: chart_TBD_01 - Capacity vs Temperature]
*Missing data: Test conditions, sample size, temperature intervals*

**Qualitative Discussion**: Based on available data, capacity decreases non-linearly below -20°C, with critical threshold around -40°C.

**To Verify**: Full characterization requires temperature sweep test data with ≤5°C intervals.

→ See "Assumptions / To Verify" section
```

---

## Assumptions & Data Gaps

### When to Mark "Assumption / To Verify"

**Always mark when**:
- Data is missing but needed for complete analysis
- Extrapolating beyond tested conditions
- Using estimates or approximations
- Relying on industry typical values without specific source

### Format

**In-text**:
```markdown
[Product] lifetime is projected at [N]+ years under continuous extreme-condition operation. **Assumption / To Verify**: This is based on accelerated lab testing; field validation requires [N-2]+ years of actual deployment data.
```

**In Self-Audit section**:
```markdown
### Assumptions / To Verify

1. **Assumption**: [Product] lifetime exceeds [N] years under [extreme condition]
   - **Missing Data**: Long-term field test data (>[N-2] years)
   - **Source Needed**: Customer deployment reports, [most-extreme deployment regions]
   - **Impact**: High (affects TCO and replacement planning)
   - **Current Basis**: Accelerated lab testing (PDF p.[N])
```

---

## FAQ Structure

### Requirements
- **Minimum**: 6 questions
- **Style**: PAA (People Also Ask) format
- **Content**: Answer with sources, acknowledge limitations

### Question Types

1. **"How" questions**: Mechanism or process
2. **"What" questions**: Definition or specification
3. **"Can I" questions**: Feasibility or constraints
4. **"Why" questions**: Rationale or trade-offs
5. **"When" questions**: Timing or conditions
6. **"Should I" questions**: Decision guidance

### Example

```markdown
## FAQ

### 1. How do [our-solution-category] units work without [auxiliary system]?

[Our-solution-category] units use specialized [materials/components] that maintain [core property] at [extreme conditions]. Key technologies include:
- Modified [formulation] with [improved property characteristic]
- [Structural innovation] with [improved physical characteristic]
- Advanced [component] materials optimized for [extreme-condition transport/operation]

Unlike conventional [products] that require pre-[conditioning] systems, these units enable direct operation down to [extreme threshold] (tested under [standard number], PDF p.[N]).

Specialized materials increase cost by [X-Y]% compared to standard units (Sheet:CostAnalysis / Range:[cell range]).

### 2. Can I [secondary operation] at [extreme threshold]?

**Short answer**: Not recommended without special precautions.

Even specialized [our-solution] units have [secondary-operation] limitations:
- [threshold range 1]: Max [conservative value] [rate/load]
- [threshold range 2]: Max [more conservative value] [rate/load]
- Beyond [threshold]: Max [most conservative value] or [alternative method]

Any [secondary operation] below [threshold] requires a [control system] with condition-based [rate/load] limiting. Skipping that control causes [degradation mode] and permanent [capacity/output] loss.

[... 4 more questions ...]
```

---

## Call-to-Action (CTA)

### ✅ Good CTA: Consultative

```markdown
## Next steps

Every application has unique requirements. Our engineering team can help you:
- Evaluate if your use case requires specialized [our-solution-category] units
- Design appropriate [supporting-system] strategies
- Specify [control-system] requirements for your operating range

Request a technical consultation (no commitment required):
- Email: engineering@yourcompany.com
- Phone: +1-XXX-XXX-XXXX
- Download: [Technical Specification Sheet](link)

Bring these details if you have them:
1. Operating [condition] range (min/max)
2. Required [performance metric] at extreme conditions
3. Expected [longevity metric]

Our team typically responds within 1 business day.
```

### ❌ Bad CTA: Hard Sell

```markdown
## Buy Now and Save 20%!

Limited-time offer on our revolutionary [products]!

**Order Today**: [Link]
**Call Now**: 1-800-XXXXXXX
```

---

## Self-Audit Report

### Structure

**Three Required Sections**:
1. High-Risk Statements
2. Assumptions / To Verify
3. Data Gaps Requiring Follow-up

### High-Risk Statements

**Format**:
```markdown
### High-Risk Statements

1. **Statement**: "87% capacity retention at -40°C"
   - **Risk**: Test conditions not fully specified
   - **Mitigation**: Added reference to full test protocol
   - **Source**: PDF p.12, Table 3 (verified)
   - **Confidence**: High

2. **Statement**: "Suitable for [most-extreme deployment scenario]"
   - **Risk**: May imply broader capability than tested
   - **Mitigation**: Specified conditions and limits
   - **Source**: None (qualitative)
   - **Confidence**: Medium
```

### Assumptions / To Verify

**Format**:
```markdown
### Assumptions / To Verify

1. **Assumption**: [Product] lifetime exceeds [N] years
   - **Missing Data**: Long-term field test data (>[N-2] years)
   - **Source Needed**: Customer deployment reports
   - **Impact**: High (affects TCO calculation)
   - **Current Basis**: Accelerated lab testing
```

### Data Gaps

**Format**:
```markdown
### Data Gaps Requiring Follow-up

**Immediate Priority**:
- [ ] [Condition] cycling data ([extreme]-to-[nominal])
- [ ] [Secondary environmental factor] impact assessment
- [ ] Detailed [secondary capability] curves

**Short-term ([N1]-[N2] months)**:
- [ ] Field data from representative applications
- [ ] Updated cost data ([quarter/year])

**Long-term (1+ year)**:
- [ ] Extended [longevity metric] validation ([N]+ [cycles/hours])
```

---

## Front Matter (YAML)

**Required fields**:
```yaml
---
title: [SEO Title ≤60 characters]
description: [Meta Description ≤155 characters]
keywords: [keyword1, keyword2, keyword3]
author: [Team/Company Name]
date: [YYYY-MM-DD]
---
```

**Example**:
```yaml
---
title: "[Product Category] Selection: Complete Engineering Guide"
description: "Data-driven framework for selecting [products] that work under [extreme condition] without [auxiliary system]. Includes failure modes, performance data, and selection checklist."
keywords: "[product category], [extreme-condition deployment], [product] [condition threshold], [auxiliary system] elimination"
author: TechBlog Engineering Team
date: "[YYYY-MM-DD]"
---
```

---

## Common Formatting Mistakes

### ❌ Mistake 1: Unsourced Numbers

**Wrong**:
```markdown
Testing shows 87% capacity at -40°C.
```

**Correct**:
```markdown
Testing shows 87% [performance metric] at [extreme threshold] (PDF p.12, Table 3).
```

### ❌ Mistake 2: Marketing Language

**Wrong**:
```markdown
Our revolutionary [product category] delivers amazing performance!
```

**Correct**:
```markdown
Our [product unit] maintains 87% [performance metric] at [extreme threshold] (PDF p.12), reducing system complexity compared to [auxiliary-system-dependent] alternatives.
```

### ❌ Mistake 3: Vague Comparisons

**Wrong**:
```markdown
Much better than standard [product category].
```

**Correct**:
```markdown
87% [performance metric] retention vs. <60% for standard units at [extreme threshold] (PDF p.12 vs. p.18).
```

### ❌ Mistake 4: Missing Chart Context

**Wrong**:
```markdown
![Chart](chart_01)
```

**Correct**:
```markdown
![Capacity vs Temperature](chart_01)
*Figure 1: Capacity retention across temperature range (Sheet:TestData / Range:B2:E15)*

Note the inflection point at -40°C where degradation accelerates.
```

---

## Quality Checklist

Before finalizing, verify:

### Content
- [ ] Every quantitative claim has source
- [ ] No fabricated data or page numbers
- [ ] All assumptions explicitly marked
- [ ] Data gaps documented in self-audit

### Structure
- [ ] Front matter complete (title, description, keywords)
- [ ] H1 title (one only)
- [ ] ≤20 total sections (H2+H3)
- [ ] FAQ includes ≥6 questions
- [ ] CTA is consultative (not hard-sell)
- [ ] Self-audit report complete

### Style
- [ ] Engineer-to-engineer tone throughout
- [ ] No signal-word label lines; meaning in full sentences (writing-plain-language.md)
- [ ] Short paragraphs (3-5 sentences)
- [ ] Lists and tables for complex info
- [ ] Bold used for key conclusions

### Charts
- [ ] All charts have captions + alt text
- [ ] Charts explained in body text
- [ ] Source attribution for all charts
- [ ] TBD placeholders if manifest missing

### Sources
- [ ] All sources use correct format
- [ ] Sources traceable to context_pack
- [ ] No generic "see documentation" references
- [ ] Internal links use placeholder format

---

## Example Paragraph Breakdown

**Bad Example**:
> [Our-solution-category] units are much better than regular [product category] under [extreme condition]. They work great down to very [extreme] conditions and don't need [auxiliary system]. Our [product unit] is the best solution for [most-extreme deployment scenario].

**Problems**:
- No specific data
- No sources
- Marketing language ("best solution")
- Vague claims ("much better", "work great")

**Good Example**:
> Specialized [our-solution] units maintain [Z]% [performance metric] retention at [extreme threshold] (PDF p.[N], Table [N]), compared to <[W]% for standard units at the same condition ([Industry Reference], [year]). This performance enables direct operation without pre-[conditioning] systems, reducing system complexity by eliminating [auxiliary-system components] and controllers. Specialized units cost [X-Y]% more than standard units (Sheet:CostAnalysis / Range:[cell range]), but that premium is typically offset by savings on [auxiliary-system hardware] ($[A-B]/[unit]) and reduced [resource] consumption ([C-D]% loss per cycle).

**Strengths**:
- Specific quantitative data ([Z]%, <[W]%, [X-Y]%, $[A-B]/[unit])
- Source attribution for all numbers
- Balanced analysis (trade-off)
- Technical language
- Actionable insight

---

## Language Conventions

### Numbers
- **Percentages**: 87% (no space)
- **Conditions with sign/unit**: -40°C, +60°C (with sign and unit)
- **Ranges**: -40°C to +60°C (use "to", not "-")
- **Approximations**: ~5 years, ≈100 cycles (use appropriate symbol)

### Units
- Always include units with numbers
- Use standard SI units or industry conventions specific to your field
- Be consistent throughout document

**Examples** (replace with the units relevant to your product category):
- Condition: °C (not F or K unless specified)
- Capacity/output: [domain-specific unit]
- Energy: Wh or kWh
- Power: W or kW
- Resistance/impedance: [domain-specific unit]
- Rate: [domain-specific unit]

### Acronyms
- Define on first use: `[Full Term] ([Acronym])`
- Use acronym consistently after definition
- Include common acronyms in glossary if provided

---

## Section Length Guidelines

**Target lengths**:
- **H2 section**: 200-500 words
- **H3 subsection**: 100-300 words
- **Paragraph**: 50-100 words (3-5 sentences)

**When to split a section**:
- Exceeds 600 words
- Covers multiple distinct subtopics
- Includes >2 charts/tables

**When to combine sections**:
- <100 words each
- Highly related topics
- Sequential steps in a process

---

## Final Reminders

1. **Every number needs a source** - No exceptions
2. **Engineer tone** - Direct, verifiable, no fluff
3. **Balanced analysis** - Acknowledge trade-offs and limitations
4. **Transparent** - Explicitly mark assumptions and gaps
5. **Actionable** - Provide checklists, tables, decision frameworks
6. **Complete** - Include all required components (SEO, FAQ, CTA, Self-Audit)

---

**This style guide ensures your technical articles are trusted, actionable, and publication-ready.**

*Tech-Blog-Writer Style Guide v1.0.0*  
*Last Updated: 2024-12-26*
