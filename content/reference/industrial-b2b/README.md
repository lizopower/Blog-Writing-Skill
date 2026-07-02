# Native American English Exemplars — Industrial/Hardware B2B

Three benchmark articles by American native writers/editors, chosen as voice and
rhythm references for `style_exemplars` (voice/structure ONLY — never factual
sources; see writing_style_guide.md Rules 19–22).

**Copyright**: These files contain structural skeletons + partial excerpts for
style analysis, with links to the originals. Do not reuse any sentence verbatim
in drafts — run `audit_near_duplicate.py` if unsure. Do not ship these files in
the bundle.

## The three exemplars

| File | Source | Genre | Why chosen |
|---|---|---|---|
| `blog/protolabs-injection-molding-tolerances.md` | Protolabs blog, Feb 7, 2023 | blog / design tips | Punchy native rhythm, direct address, short-sentence punctuation |
| `how-to/fictiv-injection-molding-tolerances.md` | Fictiv, Steve Melito, Dec 19, 2022 | how-to / definitive guide | Definition-first opening (Rule 15), data tables, FAQ section (strict-final structure) |
| `how-to/batterypowertips-lfp-bms-design.md` | Battery Power Tips (WTWH), JD DiGiacomandrea, May 15, 2023 | how-to / deep dive | Practitioner first-person authority, precise conditions, engineer-to-engineer register |

## Native-voice traits to imitate (cross-cutting)

1. **Short declaratives carry the argument.** "Thick parts tend to sink."
   "Resin selection is crucial." "That's great, but all three holes still need
   to align." The punch sentence lands *after* setup, at irregular intervals.
2. **Direct address with contractions.** "you'll want to design the mold…",
   "it's essential to…", "Let's get into some key design considerations…" —
   conversational precision, not formality.
3. **Concrete numbers inline, conditions attached.** "+/- 0.003 in. (0.076mm)",
   "3.1 V and 3.3 V from 90% to 10% SOC", "2% to 10% capacity per month".
   Claims are bounded, not hedged.
4. **Definition-first openings.** Fictiv: "Injection molding tolerances are
   acceptable variations in size for part features and overall dimensions." —
   textbook Rule 15 bridge-verb definition.
5. **Consequence-driven warnings.** "Out-of-tolerance molds result in
   out-of-tolerance parts." "If pressure isn't placed on the cells, the cell's
   capacity will rapidly degrade." Cause → effect, no abstract "importance".
6. **Sentence-initial But/So/Yet, plain connectives.** No furthermore/moreover;
   transitions are "Practically speaking,", "In turn,", "As a rule,",
   "That's why…".
7. **Phrasal/Anglo-Saxon verbs.** "dial in the parameters", "dump excess
   energy", "throw showers of flame", "take you a long way", "right off the bat".
8. **American conventions throughout.** US spelling, serial comma, imperial
   units first with metric in parentheses (Protolabs), sentence-case or Title
   Case headings kept consistent per publication.

## Usage

- Reference in `context_pack.style_exemplars` with `type: "voice"`.
- Genre extraction: `python skills/tech-article-architect/scripts/extract_genre_conventions.py --root <project-root> --topic industrial-b2b --type how-to --slug <slug>`
- First-person experience in exemplars (e.g., DiGiacomandrea's design advice)
  is HIS experience — never transplant it into your drafts (Rule boundary in
  writing_style_guide.md).
