---
version: 1.0.0
title: Article Type Profiles
description: Genre-specific structure and check_draft expectations keyed by article.json articleType.
---

# Article Type Profiles

`article.json.articleType` selects a profile for mechanical draft checks (`check_draft.py`).
Profiles do not change lifecycle phases; they tune structure and data-density warnings.

## Valid values

| `articleType` | Label | Min H2 | Max H2 | Min data points |
|---------------|-------|--------|--------|-----------------|
| `blog` | Technical blog (default) | 3 | 20 | 2 |
| `how-to` | How-to guide | 4 | 18 | 1 |
| `case-study` | Case study | 4 | 15 | 3 |
| `comparison` | Comparison article | 4 | 16 | 3 |
| `white-paper` | White paper | 5 | 25 | 5 |

Set at workspace creation:

```bash
python skills/blog-brainstorm/scripts/article.py create "Title" --slug slug --type case-study
```

## Per-type expectations

### blog (default)

- **required_sections**: flexible; at least one decision or takeaway section
- **cta_style**: consultative next steps
- **check_draft**: marketing/AI cliché scan; min 2 sourced or table-backed data points

### how-to

- **section_keywords** (warn if none match): step, how, guide, procedure, checklist
- **cta_style**: actionable start (try, template, download)
- **check_draft**: procedural H2 flow; numbered steps encouraged

### case-study

- **section_keywords**: challenge, problem, solution, result, outcome, lesson
- **cta_style**: consultative contact / discuss similar project
- **check_draft**: min 3 quantitative or outcome claims with attribution

### comparison

- **section_keywords**: comparison, versus, criteria, recommendation, trade
- **cta_style**: decision framework
- **check_draft**: expects comparison table or matrix language

### white-paper

- **section_keywords**: executive, summary, methodology, finding, conclusion
- **cta_style**: download / request full report
- **check_draft**: higher data-point floor; longer-form section balance

## Integration

- `validate_article_workspace.py` rejects unknown `articleType` values.
- `check_draft.py` reads `articleType` from `article.json` when checking a workspace draft.
- Override with `--article-type <type>` when checking a standalone `draft.md` path.

Machine-readable source of truth for validators: `skills/tech-blog-writer/scripts/_article_type_profiles.py`.
