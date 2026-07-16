# Draft prompt

Write draft.md from outline + context_pack only.

**Voice calibration (before writing the first section)**: For English articles, ALWAYS read in this order: (1) `skills/tech-blog-writer/assets/cadence_card.md` (one page), (2) `content/specs/writing-plain-language.md` (authoritative plain-language spec: scope, override table, two gate tests, eight rules; see tech-blog-writer SKILL.md §1c). Then read the style exemplars — `context_pack.style_exemplars` if provided; otherwise the default corpus in `content/reference/american-voice/` (start with its README) plus 1–2 genre-matched pieces from `content/reference/<topic>/<articleType>/` if present. Do not use repealed scaffolding: no `**Key Insight:**` label lines, no em dashes, no default "not X but Y" hooks, no "Ready to…?" CTA. Record which files you read, one cadence observation, and one plain-language fix in the Self-Audit (required). Match the *cadence* of the exemplars; never copy their phrases or claims (§1a/§1b). On the editing pass: re-read the plain-language spec and one exemplar.

After the first full draft, follow `standards/draft_lint_guide.md` and run `check_draft.py` on the workspace. Optional: `normalize_draft.py --check-only` before fact-check.
