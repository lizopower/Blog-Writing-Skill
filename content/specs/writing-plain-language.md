# Writing Plain Language — Authoritative Spec

This is the **authoritative English prose spec** for the blog-writing skill bundle and any article workspace that uses it.

Rules body source: the eight rules and two gate tests below are the same doctrine as `skills/tech-blog-writer/assets/speak-plainly.md`. When they disagree with older scaffolding, **this file wins**.

---

## Scope

**In scope (must comply):**
- Reader-facing article body: H1–H3 sections, TL;DR, FAQ answers, CTA section prose, captions that appear in the published article
- Draft and final article files (`draft.md`, `final_article.md`, and equivalents)

**Out of scope (exempt):**
- Internal QA / Self-Audit Report blocks
- Lint reports, fact-check tables, research notes, `context_pack` JSON
- Code fences, raw tables of numbers, citation lines that are not prose
- Chinese-language articles (use the Chinese anti-AI section of `writing_style_guide.md` instead)

---

## Precedence

1. This spec (`content/specs/writing-plain-language.md`)
2. `skills/tech-blog-writer/assets/speak-plainly.md` (same doctrine; entry alias)
3. `skills/tech-blog-writer/assets/writing_style_guide.md` and Anti-AI Rules 1–22 — **only where they do not conflict**
4. Older examples in `SKILL.md`, `example_article.md`, `style_guide.md`, README samples — **examples are not requirements** when they contradict this spec

On conflict, follow the **Override table** below. Do not "balance" conflicting rules.

---

## Override table (scaffolding repealed)

| Former scaffold requirement | New ruling |
|---|---|
| Signal-word label lines (`**Key Insight:**`, `**Non-negotiable:**`, `**Common Mistake:**`, `**Trade-off:**`, `**Key takeaway:**`, `**Bottom line:**`, and similar one-to-three-word labels + colon) | **Repealed.** Fold the meaning into a complete sentence. Bold a short clause inside the sentence if needed; do not open with a label line. |
| Em dash "about 1 per 200 words" density allowance | **Repealed.** Body prose: **zero** em dashes (`—`). Rewrite asides as a period, comma, or full sentence. |
| "Not X but Y" / "not just X, but Y" as counter-intuitive hook or rhetorical pattern | **Repealed** as a default move. State Y directly. Keep "not X" only when X is a real, identifiable reader misconception you can name. |
| Rhetorical / sales CTA headings and openers (`Ready to…?`, `Ready to Solve Your … Challenge?`) | **Repealed.** Use a declarative H2 (e.g. `Next steps`) and a plain request (specs, sample test, consultation). No fake question. |

**Still in force (no conflict):**
- Numerical governance and source attribution
- Claim red lines (no fabrication; style exemplars are not sources)
- Outline structure, FAQ count, Self-Audit presence
- Non-conflicting anti-AI word bans (delve, leverage, seamless, …)
- Cadence calibration via `cadence_card.md` + reference exemplars (rhythm only; they do not override this spec)
- Evidence qualifiers (`under [condition]`, `in [sample]`) — these are precision, not hedging

---

## Two gate tests

Every sentence in scope must pass both:

1. **Deletion test** — If you delete it, does the meaning suffer?
2. **Specificity test** — If a reader asks "what does this specifically mean?", can you answer with facts or logic?

Fail either → rewrite or delete. The eight rules expand these tests.

---

## The eight rules

### 1. Do not emphasize what needs no emphasis

If a normal reader would never misunderstand you in that direction, do not draw that line for them. Whenever you want to write a clarification like "not X" or "this is not X," ask whether anyone would actually misread it as X. If not, delete the whole sentence.

### 2. Modifiers must carry information

If deleting an adjective or a clause leaves the actual meaning unchanged, it should never have been there. Do not keep modifiers for style if they fail the deletion test.

### 3. Metaphors and jargon must survive follow-up questions

Before you write any metaphor or sweeping phrase, you must be able to answer two things: first, that you can unpack it with concrete facts or logic; second, that it genuinely helps understanding more than a plain statement would. If you cannot answer either, switch to the plain statement. Cited metaphors from a source author may stay.

### 4. Delete the unnecessary; do not "fix" it

When a passage only stands up after extra explanation, first ask whether it should exist at all. If not, delete it, and delete the patches written to prop it up.

### 5. Do not invent false contrasts

Unless X is a real, identifiable misconception the reader actually holds, do not use "not X but Y" or "not just X, but Y." Just say Y.

### 6. Do not replace argument with hype

Why something matters, and how large the impact is, must be spelled out concretely. Purely emotional words (insane, brutal, disruptive, "the whole internet", …) add volume, not information. Every strong claim must land on concrete facts and consequences.

### 7. Avoid AI stock phrases and industry jargon

Do not use empty openers/closers ("It's important to note," "In today's landscape," "Furthermore," "Moreover," "That said"). Prefer ordinary verbs and nouns. Do not use marketing jargon in place of actions and results. Do not prop up thin paragraphs with label lines ("Key takeaway:", "Bottom line:") or empty First/Second/Finally marches.

### 8. Keep wording and punctuation ordinary

Use common words. Stick to ordinary contemporary punctuation: periods, commas, question marks, quotation marks, and colons. **Do not use em dashes**; rewrite parenthetical asides into normal sentences. Do not write tiny label-style lines of one or two words followed by a colon. Put the meaning into complete sentences.

---

## Em-dash self-check (PowerShell)

Run from the article workspace (or pass a file path). Exit code `1` means em dashes remain in reader-facing prose.

```powershell
param(
  [Parameter(Mandatory = $true)]
  [string] $Path
)
$ErrorActionPreference = 'Stop'
$text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
# Strip fenced code so examples inside fences do not fail the body check
$prose = [regex]::Replace($text, '(?s)```.*?```', '')
# Exempt Self-Audit / lint report tails if present
$prose = [regex]::Replace($prose, '(?ms)^## Self-Audit Report\s*\r?\n.*', '')
$count = ([regex]::Matches($prose, [char]0x2014)).Count
if ($count -gt 0) {
  Write-Host "FAIL: $count em dash(es) in $Path (plain-language spec: body must have zero)"
  exit 1
}
Write-Host "PASS: no em dashes in reader-facing prose of $Path"
exit 0
```

Skill lint: `skills/tech-blog-writer/scripts/check_draft.py` also flags any em dash in English prose (warn; density >15/1000 words → P0 issue).

---

## Agent checklist (English drafts)

- [ ] Read this spec before the first section
- [ ] No signal-word label lines in body
- [ ] Zero em dashes in body
- [ ] No false "not X but Y" unless X is a named reader misconception
- [ ] CTA / closing H2 is declarative (not "Ready to…?")
- [ ] Self-Audit records one plain-language fix applied (deleted label, unpacked metaphor, removed false contrast, or similar)
