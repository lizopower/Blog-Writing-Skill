---
name: article-templates
description: Pre-built article structure templates for common B2B technical content types (English)
version: 1.0.0
---

# Article Templates Library

## Purpose
Provide ready-to-use article structure templates for common B2B technical content scenarios. All templates are designed for **English content creation**.

---

## Template 1: Product Comparison Article

**Use Case:** "Our Product vs. Competitor" or "Solution A vs. Solution B"

**Target Audience:** Engineers, Procurement Managers

**Typical Word Count:** 2000-2500 words

### Structure:

```markdown
# [Core Keyword]: [Value Proposition] - [Technical Focus]

## TL;DR (3-5 bullet points)
- Key finding 1 with metric (source)
- Key finding 2 with metric (source)
- Key finding 3 with metric (source)

## 1. Problem Definition
### 1.1 Industry Pain Points
### 1.2 Failure Modes (MANDATORY)

## 2. Solution Overview
### 2.1 Technical Approach A
### 2.2 Technical Approach B

## 3. Head-to-Head Comparison (MANDATORY)
### 3.1 Performance Metrics
[INSERT: comparison_table]
### 3.2 TCO Analysis
### 3.3 Non-negotiables (MANDATORY)

## 4. Data & Evidence
### 4.1 Laboratory Test Results
[INSERT: chart_01, chart_02]
### 4.2 Field Deployment Data

## 5. Selection Guide
### 5.1 Selection Checklist (MANDATORY)
### 5.2 Application Scenarios
### 5.3 Common Mistakes (MANDATORY)

## 6. FAQ (≥6 questions)

## 7. Conclusion & Next Steps
```

**Required Sections:**
- TL;DR
- Failure Modes
- Comparison Table
- Non-negotiables
- Selection Checklist
- Common Mistakes
- FAQ (≥6)

**Word Budget Allocation (2000 words):**
- TL;DR: 60 words
- Problem Definition: 250 words
- Solution Overview: 200 words
- Comparison: 400 words
- Data & Evidence: 350 words
- Selection Guide: 300 words
- FAQ: 350 words
- Conclusion: 90 words

---

## Template 2: Technical Tutorial Article

**Use Case:** "How to Configure/Deploy/Optimize X"

**Target Audience:** Engineers, Technical Staff

**Typical Word Count:** 1800-2200 words

### Structure:

```markdown
# How to [Action]: [Technical Focus] - Complete Guide

## TL;DR
- What you'll achieve
- Prerequisites
- Estimated time

## 1. Background & Prerequisites
### 1.1 Technical Requirements
### 1.2 Common Misconceptions (MANDATORY)

## 2. Step-by-Step Tutorial
### 2.1 Step 1: [Action]
### 2.2 Step 2: [Action]
### 2.3 Step 3: [Action]

## 3. Verification & Testing
### 3.1 How to Verify Success
### 3.2 Troubleshooting Common Issues (MANDATORY)

## 4. Best Practices
### 4.1 Performance Optimization
### 4.2 Common Mistakes to Avoid (MANDATORY)

## 5. FAQ (≥6 questions)

## 6. Next Steps & Resources
```

**Word Budget (2000 words):**
- TL;DR: 50 words
- Background: 200 words
- Tutorial Steps: 900 words
- Verification: 250 words
- Best Practices: 250 words
- FAQ: 300 words
- Next Steps: 50 words

---

## Template 3: Case Study Article

**Use Case:** "Customer Success Story" or "Real-World Deployment"

**Target Audience:** Project Managers, Procurement Managers, Engineers

**Typical Word Count:** 1500-2000 words

### Structure:

```markdown
# [Customer/Project Name]: [Achievement] with [Solution]

## TL;DR
- Customer background
- Challenge summary
- Key results with metrics

## 1. Customer Background
### 1.1 Industry & Application
### 1.2 Technical Requirements

## 2. Challenge Analysis
### 2.1 Pain Points
### 2.2 Constraints & Non-negotiables (MANDATORY)

## 3. Solution Design
### 3.1 Technical Approach
### 3.2 Implementation Steps

## 4. Results & Data
### 4.1 Performance Metrics
[INSERT: charts with before/after data]
### 4.2 ROI Analysis

## 5. Lessons Learned
### 5.1 What Worked Well
### 5.2 Common Pitfalls Avoided (MANDATORY)

## 6. FAQ (≥6 questions)

## 7. Conclusion & Applicability
```

**Word Budget (1800 words):**
- TL;DR: 60 words
- Background: 200 words
- Challenge: 300 words
- Solution: 350 words
- Results: 400 words
- Lessons: 250 words
- FAQ: 200 words
- Conclusion: 40 words

---

## Usage Instructions

### How to Use Templates

1. **Select Template** based on content type
2. **Customize Structure** if needed (keep mandatory sections)
3. **Adjust Word Budget** based on target_word_count
4. **Pass to tech-article-architect** with template parameter

### Example Usage:

```json
{
  "topic": "[Product/Technology] deployment in [extreme-condition target deployment scenario]",
  "template": "case_study",
  "target_word_count": 1800,
  "context_pack": {...}
}
```

---

*All templates designed for English content creation*
*Templates follow B2B technical writing best practices*
