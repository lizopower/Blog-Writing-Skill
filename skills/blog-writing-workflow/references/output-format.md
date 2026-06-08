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

## Issues Requiring Attention

<warnings, failures, unsupported claims, source gaps>

## Next Step

<one concrete recommendation>
```

Do not hide warnings. If validation or fact-check status is not `passed`, the output must say so clearly.
