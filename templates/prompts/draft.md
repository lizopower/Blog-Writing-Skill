# Draft prompt

Write draft.md from outline + context_pack only.

**Voice calibration (before writing the first section)**: For English articles, ALWAYS read `skills/tech-blog-writer/assets/cadence_card.md` first (one page). Then read the style exemplars — `context_pack.style_exemplars` if provided; otherwise the default corpus in `content/reference/american-voice/` (start with its README) plus 1–2 genre-matched pieces from `content/reference/<topic>/<articleType>/` if present. Record which you read plus one concrete cadence observation in the Self-Audit (required item). Match the *cadence* of the exemplars: sentence-length variance, plain Anglo-Saxon verbs, short punch sentences at irregular intervals, register. Never copy their phrases, claims, or anecdotes (exemplars are style-only; see tech-blog-writer SKILL.md §1a/§1b). Re-read one exemplar before the editing pass to re-calibrate your ear.

After the first full draft, follow `standards/draft_lint_guide.md` and run `check_draft.py` on the workspace. Optional: `normalize_draft.py --check-only` before fact-check.
