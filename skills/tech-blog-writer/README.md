# Tech-Blog-Writer Skill

**Transform technical outlines into publication-ready articles with strict numerical governance.**

---

## Overview

Tech-Blog-Writer is the **final content generation stage** in the technical blog production pipeline. It takes structured outlines and context packs and produces **publication-ready Markdown articles** that engineers trust.

### Role in Pipeline

```
Orchestrator → Research + Parser → Visualization → Architect → Writer ✅
                                                                    ↓
                                                          final_article.md
```

---

## What It Does

### ✅ Writes Publication-Ready Content
- Transforms `outline.md` + `context_pack` into complete articles
- Maintains engineer-to-engineer tone (no marketing fluff)
- Integrates charts, tables, and data visualizations
- Includes SEO components (Title, Meta, FAQ)
- Adds call-to-action (consultative, not hard-sell)

### ✅ Enforces Numerical Governance
- **Every quantitative claim must have a traceable source**
- No fabricated data or unsupported numbers
- Explicit marking of assumptions and data gaps
- Self-audit report identifying high-risk statements

### ✅ Ensures Brand Alignment
- Industry: [Your Industry] - B2B [Your Product Category]
- Core advantage: [Your core differentiator, e.g. extreme-condition direct operation]
- Caution: No exaggeration, always specify conditions

---

## What It Doesn't Do

### ❌ No New Data Creation
- Cannot add quantitative claims not in `context_pack`
- Cannot fabricate sources or page numbers
- Cannot extrapolate from incomplete data

### ❌ No Marketing Language
- No superlatives without data support
- No promotional fluff or hard-sell tactics
- No unsupported competitive claims

### ❌ No Structure Changes
- Follows `outline.md` structure (≤20 sections)
- Cannot add major new sections
- Can only add small "Data Gap / Assumption" blocks

---

## Input Requirements

### Required Inputs

1. **outline.md** (from Architect)
   - Structured section hierarchy
   - ≤20 sections (H2/H3)
   - Includes: TL;DR, Failure Modes, Data & Evidence, Comparison, Selection Checklist, FAQ

2. **context_pack** (from Orchestrator)
   ```json
   {
     "topic": "string",
     "key_claims": [{
       "claim": "string",
       "source": "PDF p.xx / Sheet:xx / URL",
       "confidence": "high|medium|low"
     }],
     "extracted_tables": [],
     "glossary": [],
     "visualization_recommendations": [],
     "risk_notes": []
   }
   ```

3. **brand_constraints**
   - Industry, segment, core advantage
   - Cautions and limitations

4. **style_constraints**
   - Language (default: English US)
   - Tone, formatting, signal words
   - Internal link strategy, CTA approach

### Optional Inputs

5. **charts_manifest** (from Visualization Generator)
   - If provided: Reference charts with `chart_id`
   - If missing: Use TBD placeholders + document gaps

---

## Output

### Single File: `final_article.md`

**Structure**:
```markdown
---
title: [SEO Title ≤60 chars]
description: [Meta Description ≤155 chars]
keywords: [list]
---

# [H1 Title]

**TL;DR**:
- [3-5 key takeaways]

## [Section 1]
[Content with sources, charts, tables]

## [Section 2]
...

## FAQ
[≥6 questions]

## Next Steps
[CTA - consultative]

## Self-Audit Report
[High-risk statements + Assumptions + Data gaps]
```

---

## Numerical Governance Rules

### Rule 1: Every Number Needs a Source

**✅ Correct**:
> Testing shows 87% capacity retention at -40°C (PDF p.12, Table 3).

**❌ Wrong**:
> Testing shows 87% capacity retention at -40°C.

### Rule 2: No Fabricated Sources

**Only use source formats from `context_pack`**:
- `PDF p.xx / Table x / Section x`
- `Sheet:xx / Range:A1:D20`
- `Word: Heading + Paragraph #`
- `URL + Publication Info`

**❌ Prohibited**:
- "See documentation" (too vague)
- "Industry typical" (no source)
- Fabricated page numbers

### Rule 3: Mark Assumptions Explicitly

**When data is missing**:
```markdown
**Assumption / To Verify**: [Product unit] lifetime exceeds [N] years under [extreme condition].

**Missing Data**: Long-term field test data (>2 years)
**Source Needed**: Customer deployment reports
**Impact**: High (affects TCO calculation)
```

---

## Chart Integration

### With `charts_manifest` ✅

```markdown
![Capacity vs Temperature](chart_01)
*Figure 1: Capacity retention across temperature range (Sheet:TestData / Range:A1:D20)*

**Key Insight**: The chart reveals a non-linear degradation pattern below -30°C, with a critical inflection point at -40°C where capacity drops sharply.
```

### Without `charts_manifest` ✅

```markdown
[Chart TBD: chart_TBD_01 - Capacity vs Temperature]
*Missing data: Test conditions, sample size, temperature intervals*

→ See "Assumptions / To Verify" section
```

---

## Style Guidelines

### Tone: Engineer-to-Engineer
- Direct, clear, verifiable
- No marketing fluff
- Short paragraphs (3-5 sentences)

### Signal Words
- **Key Insight**: Critical understanding points
- **Non-negotiable**: Hard requirements
- **Common Mistake**: Pitfalls to avoid
- **Trade-off**: Balanced analysis

### Formatting
- ✅ Bulleted/numbered lists
- ✅ Comparison tables
- ✅ **Bold** for key conclusions
- ✅ Code blocks for specs/formulas
- ✅ Internal link placeholders: `[Internal Link: topic-slug]`

---

## Self-Audit Report

**Mandatory section at end of article**:

```markdown
## Self-Audit Report

### High-Risk Statements
1. [Statement] - **Risk**: [Issue] - **Mitigation**: [Action]

### Assumptions / To Verify
1. **Assumption**: [Description]
   - **Missing Data**: [Fields needed]
   - **Source Needed**: [Type]
   - **Impact**: [High/Medium/Low]

### Data Gaps Requiring Follow-up
- [ ] [Specific data needed]
- [ ] [Test required]
```

---

## Quality Checklist

Before finalizing, verify:

### Content Quality
- [ ] Every quantitative claim has source
- [ ] No fabricated data
- [ ] All charts referenced properly
- [ ] Charts have captions + alt text

### Structure
- [ ] Follows outline.md (≤20 sections)
- [ ] Includes: SEO, TL;DR, FAQ (≥6), CTA, Self-Audit
- [ ] Internal links use placeholders

### Style
- [ ] Engineer-to-engineer tone
- [ ] Short paragraphs
- [ ] Lists/tables for complex info
- [ ] Signal words used appropriately

### Brand
- [ ] No exaggeration
- [ ] Conditions clearly stated
- [ ] Core advantage mentioned appropriately

### Governance
- [ ] All numbers have sources
- [ ] Source formats match context_pack
- [ ] Data gaps explicitly marked
- [ ] Assumptions clearly labeled

---

## Example Usage

### Input

**outline.md** (excerpt):
```markdown
# [Product Category] Selection Guide

## TL;DR
- [Points]

## Understanding [Extreme-Condition] Failure Modes
- [Section plan]

## Data & Evidence
- Insert chart_01: [Performance Metric] vs [Condition Variable]
- Insert chart_02: [Longevity Metric] Comparison
```

**context_pack** (excerpt):
```json
{
  "key_claims": [
    {
      "claim": "[X]% [performance metric] retention at [extreme threshold]",
      "source": "PDF p.12, Table 3",
      "confidence": "high"
    }
  ]
}
```

**charts_manifest** (excerpt):
```json
{
  "charts": [
    {
      "chart_id": "chart_01",
      "title": "[Performance Metric] vs [Condition Variable]",
      "source_ref": "Sheet:TestResults / Range:B2:E15"
    }
  ]
}
```

### Output

**final_article.md** (excerpt):
```markdown
---
title: [Product Category] Selection: Complete Engineering Guide
description: Data-driven framework for selecting [product category] that work under [extreme condition] without [auxiliary system]. Includes failure modes, performance data, and selection checklist.
keywords: [product category], [extreme-condition deployment], [core technology] [extreme threshold]
---

# [Product Category] Selection: Complete Engineering Guide

**TL;DR**:
- Standard [product category] loses 40-60% [performance metric] below [moderate threshold]
- Specialized [our solution] maintains [X]% [performance metric] at [extreme threshold] without [auxiliary system] (PDF p.12, Table 3)
- Critical selection factors: operating range, [secondary capability], [auxiliary system] requirements

---

## Understanding [Extreme-Condition] Failure Modes

Standard [product category] faces three primary failure mechanisms under [extreme condition]:

1. **[Failure Mechanism 1]**: Below [threshold A], [internal property] drops exponentially
2. **[Failure Mechanism 2]**: [Triggering operation] below [threshold B] can cause irreversible [degradation effect]
3. **[Performance Loss Mechanism]**: Condition-dependent [internal resistance/property] reduces usable [output]

**Key Insight**: These mechanisms are NOT uniform across [product variants]. Understanding which limitation dominates in your operating range is **non-negotiable** for system design.

---

## Performance Data & Evidence

Our testing reveals critical performance characteristics across the operating range.

![Performance Metric vs Condition Variable](chart_01)
*Figure 1: [Performance metric] retention at various [condition values] (Sheet:TestResults / Range:B2:E15)*

**Key Insight**: The data shows three distinct operating zones:
- **Zone 1 ([baseline] to [threshold A])**: >95% [performance metric] retention
- **Zone 2 ([threshold A] to [threshold B])**: 87-95% [performance metric] retention
- **Zone 3 (beyond [threshold B])**: Rapid degradation begins

Testing shows [X]% [performance metric] retention at [extreme threshold] (PDF p.12, Table 3), which is **significantly higher** than the <60% typical for standard units.

**Non-negotiable**: For applications requiring operation beyond [extreme threshold], additional [auxiliary system] becomes mandatory regardless of [core material/variant].

---

[... rest of article ...]

---

## FAQ

### 1. How do [our-solution-category] units work without [auxiliary system]?

[Our-solution-category] units use specialized [core materials/components] that maintain [key internal property] under [extreme condition]. Unlike conventional [product category] that requires [auxiliary system], these units enable [core capability] down to [extreme threshold] (tested under XX conditions, PDF p.12).

**Trade-off**: Specialized [core materials] typically increase cost by 15-30% compared to standard units (Sheet:CostAnalysis / Range:A5:C12).

[... 5 more questions ...]

---

## Ready to Solve Your [Extreme-Condition Deployment] Challenge?

Every application has unique requirements. Our engineering team can help you:
- Evaluate if your use case requires specialized [our-solution-category] units
- Design appropriate [auxiliary system] strategies
- Specify [control system] requirements for your operating range

**Request a Technical Consultation**:
- 📧 Email: engineering@yourcompany.com
- 📞 Phone: +1-XXX-XXX-XXXX
- 📄 Download Spec Sheet: [Link]

*No commitment required. We're here to help you make the right technical decision.*

---

## Self-Audit Report

### High-Risk Statements

1. **Statement**: "[X]% [performance metric] retention at [extreme threshold]"
   - **Risk**: Test conditions not fully specified in article body
   - **Mitigation**: Added reference to PDF p.12, Table 3 which contains full protocol
   - **Source**: PDF p.12, Table 3 (verified)

2. **Statement**: "Suitable for [most-extreme deployment scenario]"
   - **Risk**: May imply broader capability than tested
   - **Mitigation**: Specified "tested down to [extreme threshold]; below this requires verification"
   - **Source**: None (qualitative statement)

### Assumptions / To Verify

1. **Assumption**: [Product unit] lifetime exceeds [N] years under [extreme condition]
   - **Missing Data**: Long-term field test data (>[N] years)
   - **Source Needed**: Customer deployment reports or extended lab testing
   - **Impact**: High (affects total cost of ownership calculation)

2. **Assumption**: Cost comparison with [auxiliary-system-dependent] alternatives
   - **Missing Data**: Pricing for comparable [auxiliary-system-equipped] systems
   - **Source Needed**: Market research or supplier quotes
   - **Impact**: Medium (affects ROI analysis)

### Data Gaps Requiring Follow-up

- [ ] [Condition]-cycling data: Need test results for repeated [extreme threshold] to [baseline] cycles
- [ ] [Secondary-condition] impact: How does [secondary condition] affect performance under [extreme condition]?
- [ ] [Secondary capability]: Maximum safe [rate/load] at [threshold]
- [ ] [Longevity metric]: Degradation when stored under [extreme condition]

---

*Last Updated: [YYYY-MM-DD]*
*Sources: Internal Test Report (PDF), Supplier Data Sheets (Excel), Industry Standards (Web)*
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Adding Unsourced Numbers
**Wrong**: Most [product category] fails below [threshold].
**Correct**: Testing shows 40% [performance metric] loss at [threshold] for standard units (Source: [Industry Reference], [year]).

### ❌ Mistake 2: Marketing Language
**Wrong**: Our revolutionary [product category] is the best solution!
**Correct**: Our [product unit] maintains [X]% [performance metric] at [extreme threshold] (PDF p.12), reducing system complexity compared to [auxiliary-system-dependent] alternatives.

### ❌ Mistake 3: Ignoring Conditions
**Wrong**: Works in all [extreme-condition] environments.
**Correct**: Tested and verified for [range A] to [range B] under [test rate/load] (Sheet:TestData). Beyond [extreme threshold] requires additional validation.

### ❌ Mistake 4: Chart Without Context
**Wrong**: ![Chart](chart_01)  
**Correct**: Include caption, alt text, and explain what the chart shows + limitations.

---

## Integration with Pipeline

```
Tech-Article-Architect (outputs)
├── outline.md
└── section_plan.json
         ↓
Tech-Blog-Writer (inputs)
├── outline.md
├── context_pack (from Orchestrator)
├── charts_manifest (from Visualization)
├── brand_constraints
└── style_constraints
         ↓
Tech-Blog-Writer (outputs)
└── final_article.md ✅
```

---

## Success Criteria

Your article is ready when:

- ✅ Every quantitative claim has traceable source
- ✅ All charts properly integrated (or gaps documented)
- ✅ Follows outline structure (≤20 sections)
- ✅ Includes all required components (SEO, FAQ, CTA, Self-Audit)
- ✅ Engineer-to-engineer tone throughout
- ✅ No marketing fluff or unsupported claims
- ✅ Self-audit completed with honest assessment
- ✅ Data gaps explicitly documented
- ✅ Publication-ready Markdown format

---

## Next Steps

1. **Install**: Extract this skill to `.codebuddy/skills/tech-blog-writer/`
2. **Test**: Use with sample outline + context_pack
3. **Integrate**: Connect to your content pipeline
4. **Customize**: Adjust brand_constraints for your industry

---

## Files in This Skill

```
tech-blog-writer/
├── SKILL.md                    # Complete skill definition
├── README.md                   # This file
├── assets/
│   ├── example_article.md      # Sample output
│   └── style_guide.md          # Detailed style reference
└── scripts/
    └── validate_article.py     # Quality validation script
```

---

## Support

For questions or issues:
- Check example_article.md for reference
- Review style_guide.md for detailed formatting rules
- Run validate_article.py to check output quality

---

**Tech-Blog-Writer: Transform technical outlines into publication-ready content that engineers trust.**

*Version 1.0.0*  
*Industry: Generic - applicable to any technical/B2B domain (replace bracketed placeholders with your own)*  
*Governance: Strict Numerical Validation + Source Attribution*
