# Blog Writing Workflow Output Format

Use this final report shape after workflow completion.

```markdown
# Blog Writing Workflow Complete

## Article

**Topic**: <topic>
**Word Count**: <actual> words (target: <target>)
**Language**: <language>
**Steps Executed**: <steps>

## Quality Reports

### Data Validation

- Status: <passed | passed_with_warnings | failed>
- Quality Score: <0-100 if available>
- Issues: <count and summary>

### Fact Check

- Status: <passed | passed_with_warnings | failed>
- Claims checked: <count if available>
- Issues: <count and summary>

## Final Output

Saved to: `<path>` or attached below.

## Workflow Receipt

Use execution statuses (`completed`, `skipped`, `blocked`) for work stages. Use validation statuses (`passed`, `warnings`, `failed`, `skipped`, `blocked`) for validation and fact-check stages. Choose exactly one status per row.

| Stage | Status | Artifact / Evidence | Notes |
|---|---|---|---|
| Audience research | <completed | skipped | blocked> | `<path>` / source list / N/A | <reason if skipped or blocked> |
| Research / orchestration | <completed | skipped | blocked> | `<context_pack path>` / research notes | <reason if skipped or blocked> |
| Context validation | <passed | warnings | failed | skipped | blocked> | `<validation report path>` | <key issue or waiver> |
| Strategy pressure test (`grill-me`) | <completed | skipped | blocked> | `<strategy notes>` / user answers | <explicit waiver or inapplicability> |
| Outline | <completed | skipped | blocked> | `<outline path>` | <reason if skipped or blocked> |
| Visualization | <completed | skipped | blocked> | `<charts manifest path>` / N/A | <data insufficiency or waiver> |
| Draft | <completed | skipped | blocked> | `<draft path>` | <word count / target> |
| Fact-check | <passed | warnings | failed | skipped | blocked> | `<fact_check path>` | <claim count / issue summary> |

## Issues Requiring Attention

<warnings, failures, unsupported claims, source gaps>

## Next Step

<one concrete recommendation>
```

Do not hide warnings. If validation or fact-check status is not `passed`, the output must say so clearly.
