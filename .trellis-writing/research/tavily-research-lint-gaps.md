{
  "content": "# Mechanical lint checks for a B2B technical-blog draft validator (Vale-focused)\n\n## Executive summary\nThis brief specifies concrete, testable mechanical lint checks (beyond word blacklists) for B2B technical blog drafts across five dimensions: document structure, citation quality, rhythm/cadence, em‑dash typography, and cross‑cutting quality. Each check includes rationale, a detection rule or metric (with recommended default thresholds), severity, an example of passing/problematic text, and guidance on implementing the check in Vale or via external tooling. Recommendations prioritize in‑Vale implementation where feasible and identify checks that require external preprocessing (sentence tokenization, link validation, or NLI-based claim/citation analysis). Vale capabilities referenced below inform rule outlines and limitations. [1][2][3]\n\n## 1. Structure checks (required/optional sections, headings, blocks)\nRationale: Consistent structure improves scannability and conversion in B2B technical content and supports predictable automation (CTAs, technical examples, elevator pitches). [10][9]\n\nChecks, metrics, defaults, severity, examples, and implementability:\n- Required sections present (configurable set: elevator pitch, problem, solution, technical details, examples, CTA). Detection: verify presence of headings matching canonical labels (case-insensitive regex list). Default severity: error if required section missing; warning if CTA missing. Implementation: Vale token rule matching heading text (works for Markdown/HTML scope in Vale); for repo‑wide variations, use substitution lists. Example Vale rule outline: scope: header; match: '^(#{1,6}\\s*(Elevator pitch|Problem|Solution|Technical details|Examples|CTA)\\b)'; message: 'Missing required section: %s'; level: error. (Vale supports regex and header scope; see rules syntax.) [3][1][5]\n\n- Heading hierarchy and order. Rationale: predictable TOC and accessibility. Detection: validate that heading levels increment by at most one and that top-level exists or front‑matter title is handled. Default severity: warning. Implementation: Use a preprocessor that produces a heading-level sequence and emits Vale JSON annotations, or rely on markdownlint for strict enforcement (recommended in CI). Example detection: parse Markdown headings, assert next level ∈ {current, current+1, ≤ current}. [9][21]\n\n- Heading style (case/length). Rationale: consistent capitalization improves readability. Detection: sentence‑style capitalization vs Title Case choice enforced by regex; max words per heading default 12. Default severity: suggestion/warning. Implementation: Vale token rule matching first character uppercase and other words lowercase for sentence case; use lookahead/lookbehind per Vale regex guide. [1][3][34]\n\n- Paragraph and section length. Rationale: shorter paragraphs enhance scanability; suggested defaults: paragraphs ≤ 6 sentences and sections ≤ 300–450 words (configurable). Detection: requires sentence tokenization and word counts; default severity: warning. Implementation: external preprocessor (sentence tokenizer + counts) that emits Vale‑compatible annotations or JSON. Vale alone cannot robustly compute sentence counts across Markdown blocks. [12][22]\n\n- Code blocks and examples formatting. Rationale: consistent fenced code blocks with language tag and brief explanatory caption/inline comment increases usability. Detection: ensure fenced code blocks contain a language tag and adjacent explanatory prose within one paragraph. Severity: warning. Implementation: Vale can match fenced code block delimiters via regex but verifying adjacent prose requires parser; implement with preprocessor that reports missing captions as Vale annotations. [3][5]\n\n- Alt text for figures. Rationale: accessibility and SEO; alt text should be concise but descriptive. Detection: image syntax with empty alt or excessively long alt (>25 words) flagged; severity: warning. Implementation: Vale rule matching Markdown image syntax and alt text length via regex; where complex, use a parser. [11]\n\n- Lonely headings / orphaned sections. Rationale: headings without substantive content indicate outline remnants. Detection: heading followed by fewer than N words or sentences (default N=20 words) before next heading → warning. Implementation: requires simple block parsing; feasible as an external script emitting Vale annotations or a scoped Vale rule if content follows predictable Markdown patterns. [9][3]\n\n## 2. Citations and references\nRationale: Technical claims require authoritative support; B2B audiences expect credible sourcing and working links. [17][16][19]\n\nChecks:\n- Claim→citation detection: flag sentences making assertive claims without nearby citation. Detection: use lightweight heuristics (presence of terms like \"demonstrates\", numeric claims, \"studies show\") combined with claim classifier; default severity: warning. Implementation: external NLP model or ALCE/claim detectors (research in automated claim detection exists; ALCE shows promising results for citation tasks) — emit Vale annotations. [18][24]\n\n- Citation density and authoritative-source ratio. Rationale: ensure sufficient support for technical claims. Detection: require at least one authoritative-source citation per X technical claims (default X=3) and a minimum fraction of citations from whitelisted domains (.gov, .edu, known vendors) default 25%. Severity: warning/error depending on shortfall. Implementation: external citation parser that extracts URLs/DOIs and computes ratios; broken-link checking (weekly) for URL health recommended. [17][16][23]\n\n- Missing citation metadata. Rationale: complete citations (author/title/date/DOI/URL) enable verification. Detection: bibliographic entries or link anchor text lacking metadata flagged; severity: warning. Implementation: external script to parse reference blocks and validate via pattern matching (DOI regex) and by attempting URL HEAD requests (link health). [16][17]\n\n- Inline vs endnote style and anchor text quality. Rationale: consistent inline linking improves immediacy; anchor text should describe target. Detection: anchor text shorter than 3 characters or generic \"click here\" flagged; severity: suggestion. Implementation: Vale regex matching link patterns and anchor text content; feasible in Vale for Markdown link tokens. [3]\n\n- Self‑citation bias. Rationale: excessive self‑citation reduces perceived objectivity. Detection: compute self‑citation ratio against baseline β (configurable); flag non‑linear growth above threshold as warning/error. Implementation: external analytics module (research shows algorithms for self‑citation exist); emit Vale annotations. [25][17]\n\n- Dead-link detection. Rationale: broken links harm trust and SEO. Detection: periodic HEAD/GET checks; flag 4xx/5xx or redirects beyond limit. Severity: error for 404 on production content. Implementation: external link-checker run in CI/cron and annotate PRs or generate Vale‑compatible JSON. [16]\n\n## 3. Rhythm / cadence (measurable)\nRationale: Cadence affects comprehension and perceived professionalism in B2B content; measurable metrics enable automated signals to editors. [12][19][13]\n\nChecks and detection rules:\n- Average sentence length and variance. Metric: mean words/sentence and standard deviation; recommended defaults: mean ≤ 25 words; SD ≥ 6 preferred to avoid monotony. Severity: warning when mean >25; error when mean >35. Implementation: external sentence tokenizer → compute metrics → emit Vale annotations. [12][19]\n\n- Short/long sentence ratio and long run detection. Metric: ratio of sentences <10 words to >30 words; flag runs of >4 consecutive sentences within ±10% length (monotonous cadence). Severity: suggestion/warning. Implementation: external tokenizer + simple sliding-window algorithm. [19][31]\n\n- Passive voice percentage. Detection: approximate via regex for \"was|were|is|are|be + past‑participle\" patterns; default warning if >15%. Implementation: Vale can implement simple passive regex rules; existing Vale write‑good style packages provide similar checks. [3][9]\n\n- Nominalization density. Detection: count tokens with nominalizing suffixes (-tion, -ment, -ance, -ity, -ing nominalizations); default flag when density > 3% of words. Severity: suggestion. Implementation: Vale substitution/vocab rules can flag specific nominalizations; heavier statistical checks require preprocessing. [13][2]\n\n- Readability score (Flesch). Metric: Flesch Reading Ease and Flesch‑Kincaid grade level; recommend B2B target grade 10–11 (configurable). Implementation: external readability library computes scores; annotate via Vale JSON. [12][19]\n\n- Diversity of sentence openings. Detection: repeated sentence starts (same first word in >3 consecutive sentences) flagged. Severity: suggestion. Implementation: external tokenizer; can be approximated by Vale if sentence boundaries are clear but better as preprocessor. [31]\n\n## 4. Em‑dash density and typography\nRationale: Inconsistent dash use degrades typography; B2B content should be consistent with chosen style (Chicago vs web preferences). [14][15]\n\nChecks:\n- Em‑dash frequency (per 1,000 words). Default warning threshold: >15 em‑dashes/1,000 words; error >30/1,000 words. Rationale and thresholds are recommendations to tune. Detection: count Unicode em‑dash (—) occurrences normalized by word count. Implementation: feasible via Vale token rule that matches em‑dash characters, but counting per‑file requires an external pass or Vale limit field to cap instances. [1][3][14]\n\n- Clustering (multiple em‑dashes in one sentence). Detection: regex for two or more em‑dashes within sentence → warning. Implementation: Vale regex rule with lookahead/behind. [1][3]\n\n- Consistency of dash type and spacing. Detection: mixed use of hyphen (-), en‑dash (–), and em‑dash (—) in same document or presence of spaces around dashes conflicting with chosen convention (spaced en‑dash vs unspaced em‑dash). Default: pick convention (Chicago: unspaced em‑dash; web/GOV: spaced en‑dash). Severity: warning for mixed usage; error if majority uses non‑selected convention. Implementation: Vale regex rules can detect characters and spacing patterns; use YAML substitution rules to suggest replacements. [14][15][1]\n\n## 5. Cross‑cutting checks and workflow guidance\nRationale: Combine sentence/paragraph boundary checks, run‑on detection, repeated starts, tone flags, presence of value proposition/CTA, and hedging language detection to surface editorial issues. Detection: mix of Vale regex rules (hedging words), substitution rules (tone), and external NLP (run‑on detection, value‑proposition presence). Severity: suggestion→warning depending on editorial policy. Implementation: use Vale for lexical flags and CI pipelines + external scripts for structural/NLP checks; integrate via Vale JSON or PR comments. [3][5][21]\n\n## Prioritized checklist (grouped)\nImplementable directly in Vale (low-effort/high‑value): heading label matches, heading capitalization patterns, anchor text heuristics, simple passive voice regex, dash‑character and spacing rules, substitution vocab (nominalizations), link‑format pattern checks. [1][3][2]\n\nRequires external tooling (pre/post‑processing): paragraph/section sentence counts, sentence tokenization metrics (readability, cadence, sentence diversity), claim→citation detection, authoritative‑source ratio and self‑citation analytics, dead‑link HTTP checking, bibliographic metadata verification. [16][18][17]\n\n## Implementation notes, testing and CI\nVale rule files are YAML with keys like extends, message, level, scope, and limit; regexes should be quoted and can use lookahead/lookbehind. Vale templates can format output; Vale supports styles in .vale/styles and .vale.ini configuration and can run in CI or Git hooks. Use unit tests with small sample corpus and CI integration (GitHub Actions or repo scripts) and allow per‑repo .vale‑overrides for tuning. Watch for false positives where tokenization is ambiguous (code blocks, inline HTML). [1][3][4][6][10][5]\n\n## Risks, false positives, and tuning\n- Regex-based passive detection and nominalization flags produce false positives; tune with vocab lists and whitelist contexts. [3][13]\n- Claim detection/NLI tools (ALCE/CiteEval) have nontrivial false‑positive/negative rates and require human review for relevance. [18][17]\n- Dash conventions vary by style guide (Chicago vs web/GOV); enforce a single chosen convention to avoid churn. [14][15]\n\n## Evidence gaps\n- No single canonical numeric thresholds for em‑dash density or exact sentence-length cutoffs for B2B audiences; defaults above are recommendations to tune to audience. (Thresholds proposed are not derived from an authoritative standard in the provided findings.) [14][19]\n- No fully specified, production‑ready claim‑detection models within Vale; research indicates approaches exist but require external tooling and validation. [18][17]\n\n## Recommended authoritative references to consult when building rules\nPrioritize Vale official docs and examples, markdownlint rules for headings, Google and Microsoft style guidance for headings/capitalization, Flesch formulas for readability, typographic guidance for dashes, ALCE/CiteEval literature for citation detection, and standard link‑checking/SEO practices for dead links. [1][3][9][10][11][12][14][18][17][16]\n\n## Works Cited\n[1] https://vale.sh/docs/guides/regex  \n[2] https://vale.sh/docs/styles  \n[3] https://vale.sh/docs/templates  \n[4] https://spectrocloud.com/blog/how-we-use-vale-to-enforce-better-writing-in-docs-and-beyond  \n[5] https://buildwithfern.com/post/docs-linting-guide  \n[6] https://github.com/elastic/vale-rules  \n[7] https://wiki.qt.io/Setting_Up_Vale  \n[8] https://learn.microsoft.com/en-us/style-guide/scannable-content/headings  \n[9] https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md  \n[10] https://developers.google.com/style  \n[11] https://developers.google.com/tech-writing/accessibility/self-study/write-alt-text  \n[12] https://clickhelp.com/clickhelp-technical-writing-blog/improve-the-readability-of-your-technical-documentation-with-flesch  \n[13] https://readabilityformulas.com/the-hidden-pitfalls-of-nominalizations  \n[14] https://smashingmagazine.com/2011/08/mind-your-en-and-em-dashes-typographic-etiquette  \n[15] https://stylemanual.gov.au/grammar-punctuation-and-conventions/punctuation/dashes  \n[16] https://semonto.com/blog/how-to-monitor-broken-links-12-seo-best-practices-2026  \n[17] https://arxiv.org/html/2506.01829v1  \n[18] https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.398.pdf  \n[19] https://radix-communications.com/how-can-i-make-complex-b2b-content-readable-and-compelling-b2b-content-tuesday  \n[20] https://mbrenndoerfer.com/writing/attribution-and-citation",
  "sources": [
    {
      "url": "https://vale.sh/docs/guides/regex",
      "title": "Regex - Vale CLI",
      "favicon": "https://vale.sh/favicon.ico"
    },
    {
      "url": "https://vale.sh/docs/styles",
      "title": "Styles - Vale CLI",
      "favicon": "https://vale.sh/favicon.ico"
    },
    {
      "url": "https://vale.sh/docs/templates",
      "title": "Templates - Vale CLI",
      "favicon": "https://vale.sh/favicon.ico"
    },
    {
      "url": "https://www.spectrocloud.com/blog/how-we-use-vale-to-enforce-better-writing-in-docs-and-beyond",
      "title": "How we use Vale to enforce better writing in docs and beyond",
      "favicon": "https://cdn.prod.website-files.com/64105dfa8da6a9f617932c6c/67af0dfd3fbdeb8edbbcb829_ForWebclip_256x256%20(1).png"
    },
    {
      "url": "https://wiki.qt.io/Setting_Up_Vale",
      "title": "Setting Up Vale - Qt Wiki",
      "favicon": "https://wiki.qt.io/favicon.ico?t=2016041300"
    },
    {
      "url": "https://github.com/elastic/vale-rules",
      "title": "GitHub - elastic/vale-rules: Elastic Docs' style guide rules for the Vale linter · GitHub",
      "favicon": "https://github.githubassets.com/favicons/favicon.svg"
    },
    {
      "url": "https://developers.google.com/style",
      "title": "About this guide | Google developer documentation style guide",
      "favicon": "https://www.gstatic.com/devrel-devsite/prod/v8b2f8e7f8a7704cc38c0519ef05e8f889c427cc26f7c8f743e84df2a01b1dee7/developers/images/touchicon-180-new.png"
    },
    {
      "url": "https://learn.microsoft.com/en-us/style-guide/scannable-content/headings",
      "title": "Headings - Microsoft Style Guide",
      "favicon": "https://learn.microsoft.com/favicon.ico"
    },
    {
      "url": "https://developers.google.com/tech-writing/accessibility/self-study/write-alt-text",
      "title": "Write helpful alt text  |  Technical Writing  |  Google for Developers",
      "favicon": "https://www.gstatic.com/devrel-devsite/prod/v8b2f8e7f8a7704cc38c0519ef05e8f889c427cc26f7c8f743e84df2a01b1dee7/developers/images/touchicon-180-new.png"
    },
    {
      "url": "https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md",
      "title": "markdownlint/doc/Rules.md at main · DavidAnson/markdownlint · GitHub",
      "favicon": "https://github.githubassets.com/favicons/favicon.svg"
    },
    {
      "url": "https://arxiv.org/html/2506.01829v1",
      "title": "CiteEval: Principle-Driven Citation Evaluation for Source Attribution",
      "favicon": "https://arxiv.org/static/browse/0.3.4/images/icons/apple-touch-icon.png"
    },
    {
      "url": "https://semonto.com/blog/how-to-monitor-broken-links-12-seo-best-practices-2026",
      "title": "How to Monitor Broken Links: 12 SEO Best Practices (2026) | Semonto",
      "favicon": "https://semonto.com/favicon.ico"
    },
    {
      "url": "https://readabilityformulas.com/the-hidden-pitfalls-of-nominalizations",
      "title": "Unlocking Readability: The Hidden Pitfalls of Nominalizations – ReadabilityFormulas.com",
      "favicon": "https://readabilityformulas.com/favicon.ico"
    },
    {
      "url": "https://www.smashingmagazine.com/2011/08/mind-your-en-and-em-dashes-typographic-etiquette",
      "title": "Mind Your En And Em Dashes: Typographic Etiquette — Smashing Magazine",
      "favicon": "https://www.smashingmagazine.com/images/favicon/apple-touch-icon.png"
    },
    {
      "url": "https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/punctuation/dashes",
      "title": "Dashes | Style Manual",
      "favicon": "https://www.stylemanual.gov.au/themes/custom/sm/favicon.ico"
    },
    {
      "url": "https://radix-communications.com/how-can-i-make-complex-b2b-content-readable-and-compelling-b2b-content-tuesday",
      "title": "How can I make complex B2B content readable and compelling? | B2B Content Tuesday - Radix Communications",
      "favicon": "https://radix-communications.com/wp-content/uploads/2024/12/favicon-1-150x150.png"
    },
    {
      "url": "https://clickhelp.com/clickhelp-technical-writing-blog/improve-the-readability-of-your-technical-documentation-with-flesch",
      "title": "Flesch-Kincaid Grade Level: Enhancing Document Clarity",
      "favicon": "https://clickhelp.com/wp-content/themes/clickhelp/inc/img/favicon.svg"
    },
    {
      "url": "https://buildwithfern.com/post/docs-linting-guide",
      "title": "Docs Linting Guide - January 2026 | Fern",
      "favicon": "https://buildwithfern.com/icon4.png?icon4.0ft48whryf2.b.png?dpl=dpl_BtwacSWoHSzqyGmh6ySapXtFT38R"
    },
    {
      "url": "https://mbrenndoerfer.com/writing/attribution-and-citation",
      "title": "Attribution and Citation: Sourcing LLM Outputs - Interactive | Michael Brenndoerfer | Michael Brenndoerfer",
      "favicon": "http://mbrenndoerfer.com/apple-icon.png"
    },
    {
      "url": "https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.398.pdf",
      "title": "[PDF] Enabling Large Language Models to Generate Text with Citations",
      "favicon": "https://aclanthology.org/aclicon.ico"
    }
  ],
  "status": "completed",
  "created_at": "2026-06-24T08:54:04.067760+00:00",
  "response_time": 195.85,
  "request_id": "944008b1-4126-493b-8dbb-b983f53aad91"
}
