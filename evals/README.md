# Native-Voice Eval Harness

Fixed benchmark to measure whether skill changes actually improve native-English
output quality. Run it before and after any change to the style guide, lint
rules, exemplars, or prompts — no more faith-based tuning.

## Layout

```text
evals/
├── README.md          (this file)
├── rubric.md          (blind qualitative rubric, 1–5 scales)
├── tasks/
│   ├── task-01-comparison.md
│   ├── task-02-howto.md
│   └── task-03-casestudy.md
└── score_draft.py     (quantitative scorer; reuses check_draft)
```

## Workflow

1. **Generate**: for each task in `tasks/`, run the normal workflow
   (brainstorm → outline → draft via `tech-blog-writer`) with the current
   version of the skill. Save each draft as
   `evals/runs/<date>-<label>/task-NN.md` (e.g. `runs/2026-07-02-baseline/`).
2. **Score quantitatively**:
   ```bash
   python evals/score_draft.py evals/runs/<date>-<label>/task-01.md --article-type comparison
   python evals/score_draft.py evals/runs/<date>-<label> --all   # scores the whole run dir
   ```
   Outputs one JSON per draft plus a `summary.json`: warn counts by category
   (translationese / spelling / AI-cliche / AI-pattern / hedge / marketing /
   rhythm / punctuation), rhythm stats (mean, SD, punch count), issues, and a
   composite `native_score` (100 minus weighted warns).
3. **Score qualitatively (blind)**: shuffle drafts from two runs, remove run
   labels, rate each against `rubric.md`. Ideally have a native speaker do it;
   otherwise a fresh LLM session with ONLY the rubric (no skill context).
4. **Compare**: a change ships only if `native_score` does not regress AND
   blind rubric medians improve or hold.

## Rules

- Never edit `tasks/*.md` — a moving benchmark measures nothing. Add new tasks
  as task-04+, don't change old ones.
- Keep every `runs/` directory; history is the point.
- `native_score` is a tripwire, not a target. Optimizing the number directly
  (e.g. padding punch sentences to dodge `[rhythm]`) is Goodhart's law — the
  blind rubric exists to catch that.
