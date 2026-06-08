# Blog Writing Workflow Data Flow

```text
User input
  topic + files + options
      |
      v
audience-pain-point-research (optional)
      |
      v
tech-blog-orchestrator
      |
      v
Context Pack v2.1.0
      |
      v
data-validator
      |
      v
grill-me (conditional / mandatory if requested)
      |
      v
tech-article-architect
      |
      v
tech-visualization-generator (conditional)
      |
      v
tech-blog-writer
      |
      v
fact-checker
      |
      v
final article + quality reports
```

## Artifact Handoffs

- Pain points -> Context Pack research focus.
- Context Pack -> validation, strategy pressure test, outline, writing, fact-check.
- Validation report -> pressure-test and quality gate decisions.
- Strategy summary -> outline and article writing.
- Outline -> article writer.
- Charts manifest -> article writer.
- Draft -> fact checker.

Never fabricate or reshape upstream artifacts silently. If an artifact is invalid, fix it at the producing step or ask the user for approval to proceed with risk.
