# Writing Style Guide: Engineering Consultant Voice

**Based on**: Reference article analysis (a worked example comparing technical product options for an infrastructure deployment scenario — examples below use bracketed placeholders so you can swap in your own product category and comparison axes)

---

## Voice Identity

Write as a **senior engineer sharing project selection advice with peers**.

**Core Characteristics**:
- Authoritative but not arrogant
- Precise but not academic
- Practical but not oversimplified
- Honest but not negative
- Professional but not cold

---

## Opening Templates

### Template 1: Counter-Intuitive Hook

**Structure**:
```markdown
[Surprising fact with data that challenges common belief]

Yet [opposite conclusion]. Why? Because [key insight that resolves the paradox].

This guide [promise of what reader will learn].
```

**Example**:
```markdown
[Variant A] actually outperforms [Variant B] under [extreme condition]. At [threshold], [Variant A] retains 70-80% of its rated [performance metric], while standard [Variant B] drops to just 50-60%.

Yet [Variant B] remains the better choice for most [target deployment] projects. Why? Because [condition] performance is only one parameter. Lifecycle cost, safety, and total cost of ownership matter more for a [N]-year infrastructure investment.

This guide walks you through the [N] parameters that determine whether your [product category] will survive [extreme condition] or leave your [deployment scenario] underperforming.
```

---

## Section Writing Patterns

### Pattern 1: Direct Answer First

**Structure**:
```markdown
## [Question as H2 Title]?

[Direct answer in first sentence].

[Supporting data/explanation in following paragraphs].
```

**Example**:
```markdown
## Which [Core Material/Variant] Works Best Under [Extreme Condition]?

[Variant B] wins for most [target deployment] applications, despite not having the best [condition]-performance numbers.

Here's the [performance metric] retention comparison across [condition values]:
[Table with data]

The numbers seem to favor [Variant A]. But [target deployment] projects are infrastructure investments with [N]-year lifecycles. Consider the full picture:
[Detailed analysis]
```

---

## Data Presentation Templates

### Template 1: Comparison Table with Context

**Structure**:
```markdown
Here's the [metric] comparison across [dimension]:

| [Dimension] | Option A | Option B | Option C |
|-------------|----------|----------|----------|
| Condition 1 | Value    | Value    | Value    |
| Condition 2 | Value    | Value    | Value    |

The numbers seem to favor [X]. But [context that changes the conclusion]:

**[Factor 1]:** [Explanation with data]
**[Factor 2]:** [Explanation with data]

The key insight: [Nuanced conclusion]
```

---

## Decision Framework Templates

### Template 1: When X vs When Y

**Structure**:
```markdown
**When [Option X] makes sense:**
- [Specific condition 1]
- [Specific condition 2]
- [Specific condition 3]
- [Specific condition 4]

**When [Option Y] is sufficient:**
- [Specific condition 1]
- [Specific condition 2]
- [Specific condition 3]
- [Specific condition 4]

[Concluding guidance with specific recommendation]
```

**Example**:
```markdown
**When [active mitigation method] makes sense:**
- [Extreme condition] beyond [threshold A]
- Deployments with irregular [resource/charging] windows
- Projects where guaranteeing [capability] justifies additional cost
- Environments where [secondary condition] rarely returns to baseline

**When [passive mitigation method] is sufficient:**
- Moderate [condition] ([threshold B] to [threshold A])
- Consistent [resource/charging] cycles with periodic recovery
- Enclosures/designs that retain [resource] from the previous cycle
- Projects prioritizing simplicity and lower maintenance

For [target deployment] in moderate-[condition] environments, proper [passive mitigation method] often beats [active mitigation method].
```

---

## Formula Presentation Template

**Structure**:
```markdown
Use this formula:

**[Formula Name] = ([Component A] x [Component B] x [Component C]) / ([Component D] x [Component E] x [Component F])**

[Define each variable]:
- [Variable 1]: [Definition with units]
- [Variable 2]: [Definition with units]

**Example calculation:** [Specific scenario]

- [Input 1]: [Value with units]
- [Input 2]: [Value with units]
- Using [assumptions]: [Calculation steps]

Round up and add a [X]% buffer. For this project, specify at least [Result].
```

---

## Warning/Pitfall Templates

### Template 1: Common Mistake Pattern

**Structure**:
```markdown
One common [action] mistake costs projects [consequence]: [specific error].

[Explanation of why this is wrong].

[Correct approach with example].
```

**Example**:
```markdown
One common sizing mistake costs projects thousands: confusing [unit-A]-[unit-B] relationships. A [config 1] [product unit] stores [value 1] [combined-unit]. A single [config 2] [product unit] stores only [value 2] [combined-unit]. Always calculate in [combined-unit], then convert to [unit-B] at your system [reference parameter].
```

### Template 2: Never/Non-negotiable Pattern

**Structure**:
```markdown
Never [action] to [save/achieve X]. [Consequence explanation].

[Real-world failure example starting with "I've seen..."]
```

**Example**:
```markdown
Never compromise on [control system] quality to save cost. The [core component] represents 30-40% of your [target deployment] investment. A cheap [control system] that allows out-of-spec operation will destroy components that cost far more than the [control system] savings.

I've seen projects specify excellent [core components] paired with bargain [control systems]. The components failed within two [operating cycles] because the [control system] allowed operation at conditions that caused [degradation mechanism].
```

---

## Sentence Patterns

### Assertive Recommendations

**Use**:
- "[Variant B] wins for most applications"
- "I recommend [specific option]"
- "I consider [X] non-negotiable"
- "For [scenario], [option] becomes essential"

**Avoid**:
- "You might want to consider..."
- "It is generally recommended that..."
- "One could argue that..."

### Experience-Based Authority

**Use**:
- "I've seen projects [fail/succeed] because..."
- "In my experience, [pattern]..."
- "Real-world performance validates..."

**Boundary**: Use first-person experience only when the user supplied it in `author_experience_notes`, an interview, or source-backed case material from `context_pack.key_claims` or `context_pack.extracted_tables` (never from `style_exemplars`). If no real experience is available, convert the point into a sourced pattern or decision rule. Never invent a story to make the article feel more human.

### Conditional Precision

**Use**:
- "At [threshold], [test rate], [soak duration] soak"
- "Below [extreme threshold], or for applications with [condition]"
- "In regions with [specific condition]"

**Avoid**:
- "In [extreme condition] weather"
- "Under normal conditions"
- "Generally speaking"

---

## Paragraph Structure

### Opening Paragraph Pattern

```markdown
[Direct statement of conclusion/recommendation].

[Supporting data or comparison].

[Nuanced explanation of why, despite data, conclusion holds].
```

### Middle Paragraph Pattern

```markdown
[Topic sentence with specific claim].

[Data/evidence with source and conditions].

[Implication for reader's decision].
```

### Closing Paragraph Pattern

```markdown
[Restate key insight].

[Specific condition where exception applies].

[Final recommendation with action].
```

---

## Anti-AI Writing Constraints (Mandatory)

These constraints eliminate robotic patterns. Every rule is non-negotiable.

### Rhythm Constraints

**Rule 1**: No more than two consecutive sentences of similar length.

Break the pattern. Mix a three-word punch with a twenty-word explanation. Then drop a medium sentence between them. Monotone rhythm numbs readers — they forget what they read, why they started, and what year it is.

**Rule 2**: Use short sentences (under ~6 words) as regular punctuation — a few per section, where the content earns them.

Examples: "Here's why." / "It failed." / "Check the data." / "Not anymore."

Do **not** apply this mechanically (one per paragraph, every paragraph). A fixed cadence of punchy fragments reads as gimmicky aphorism-speak — itself a tell. Native writers vary the interval.

**Rule 3**: Use occasional single-sentence paragraphs for emphasis.

This creates breathing room. A single-sentence paragraph forces the reader to pause, absorb, and reset. A few per article is right; never on a fixed schedule (e.g. "every fourth paragraph") — predictable rhythm is machine rhythm.

**Self-Check Method**:
1. After writing each section, count sentence lengths
2. Flag any run of three+ sentences within ±5 words of each other
3. Check each section has at least one short punch sentence — and that they don't land on a predictable beat
4. Check the article has a few single-sentence paragraphs at natural emphasis points

### Vocabulary Constraints

**Banned words** (never use, no exceptions):
- very
- really
- just
- actually
- basically
- essentially

**Rule 4**: Replace all abstract nouns with concrete nouns.

| ❌ Abstract | ✅ Concrete |
|------------|------------|
| "importance" | name the specific consequence |
| "effectiveness" | cite the measured outcome |
| "reliability" | state the failure rate |
| "performance" | give the capacity retention percentage |
| "quality" | describe the test result |
| "solution" | name the specific product or method |

**Rule 5**: Default to few adjectives — let nouns and numbers carry weight.

Not "the robust, reliable, high-performance [product unit]." Pick one: "The [N]-cycle [product unit]." Two adjectives are fine when both carry real information ("a sealed 280 Ah prismatic cell"). Never stack three, and never pad with evaluative adjectives (great, powerful, impressive).

### Structure Constraints

**Rule 6**: Opening paragraph — three sentences maximum.

No throat-clearing. No "In today's rapidly evolving energy landscape..." Start with the point.

**Rule 7**: Never open a section with background.

Wrong: "[Product category] technology has evolved over decades..."
Right: "[Variant B] retains 90% [performance metric] at [extreme threshold]." Lead with the finding, the claim, the data. Context follows.

**Rule 8**: End sections by advancing the argument, not summarizing.

No "In summary..." or "To conclude..." or "As we've seen..."

The last sentence of every section should push the reader forward — pose a question, introduce a tension, or state what comes next. Summaries are for obituaries.

### Buzzword Constraints

**Rule 9**: Curb the corporate-AI vocabulary. These words are the strongest "written by AI" signal in English. Replace them with plain or specific language. Keep a word only when it is a genuine technical term of art in context (e.g. "robust regression", "harness" as a physical part).

| ❌ AI buzzword | ✅ Replace with |
|---|---|
| leverage (verb) | use |
| utilize | use |
| robust | reliable / well-tested / proven (or state the number) |
| seamless / seamlessly | works without extra steps (say how) |
| delve into | examine / look at |
| harness (figurative) | use / apply |
| navigate (figurative) | handle / work through |
| unlock / elevate / supercharge | improve (say by how much) |
| transformative / game-changing / revolutionary | name the concrete change |
| cutting-edge / state-of-the-art | the current standard / name the spec |
| pivotal / crucial / vital | important — or cut it and show why |
| realm / landscape / ecosystem / space | market / field / area (or name it) |
| tapestry / symphony / multifaceted | cut |
| testament to | shows / proves |
| foster / bolster / underscore | build / strengthen / show |
| meticulous / nuanced / intricate | precise / specific (or describe it) |

**Rule 10**: Ban filler and signpost phrases. Delete them or replace with the point itself.

- "It's worth noting that…", "It's important to note…", "Needless to say…" → just state it.
- "In today's fast-paced / ever-evolving / rapidly changing world…" → cut entirely.
- "When it comes to X…" → "For X,".
- "In the realm of…", "In the world of…" → cut.
- "At the end of the day…", "In essence…", "Simply put…" → cut.
- "It's not just X, it's Y" / "X isn't only about Y" → state X and Y plainly, no antithesis.
- "Not only… but also…" → split into two sentences or use "and".
- "Let's dive in", "Let's explore", "Buckle up" → start with the content.
- Academic/AI connectives — furthermore, moreover, consequently, thus, hence, "in terms of", "it is evident that", "one may argue", "that being said", "additionally" (when overused) → use plain links (and, but, so, then) or start a new sentence.

### Punctuation & Pattern Constraints

**Rule 11**: Em-dash discipline. The em-dash flood is a top AI tell. At most one em-dash per ~200 words; never two em-dash asides in the same paragraph. Default to a comma, a period, or parentheses. Ask: would a period work here? Then use a period.

**Rule 12**: Break the rule of three. AI defaults to three-item lists and tricolons ("fast, cheap, and reliable") even when the content has two items or five. Vary list length deliberately — use 2, 4, 5, 7. Group three things only when there are genuinely three.

**Rule 13**: Vary openers and connectives. Don't start consecutive sentences with the same word or with "This/These/It". Avoid the stacked-hedge ("can help to potentially improve") — commit to the claim and cite it, or drop it.

**Rule 14**: Prefer active voice; cut empty hedges, keep evidence qualifiers. Convert passive to active when a real actor exists ("the BMS cuts current", not "current is cut"). Contractions are fine in moderation (it's, don't). Do **not** manufacture a casual/"coffee-chat" voice, anecdotes, or slang.

Distinguish two kinds of qualifier — this is critical for B2B credibility:
- ❌ Cut **empty hedges** that dodge responsibility: arguably, perhaps, it could be said, many believe, it is often thought, in my experience.
- ✅ Keep **evidence qualifiers** that state real scope: "under [test condition]", "in [sample of N]", "according to [source]", "validated only to [range]", "at [temperature]". These are precision, not hedging. Never strip a condition that bounds a claim's validity.

### Citation-Earning Constraints (AEO/GEO)

Rules 15–18 come from AEO/GEO research on what makes content quotable by AI assistants (ChatGPT, Perplexity, Google AI). That research is **correlational, not causal**, and time-sensitive — treat it as writing-quality guidance, not a ranking hack. **Never let citation optimization induce fabrication or keyword stuffing.** Full context: `standards/aeo_geo_signals.md`.

**Rule 15** — Definition sentences go straight to the bridge verb. Open a definition with `[Term] is / are / means / refers to [definition] under [scope]` (中文：`[术语] 是指……`). Do not open a definition with "can be considered", "may be regarded as", or "is a kind of … that emerged from …" unless the context_pack marks the claim low-confidence. A direct "X is Y" is the strongest semantic path to a citable answer.

**Rule 16** — Entity echo. When an H2/H3 is phrased as a question, the first sentence of the answer repeats the question's subject entity as its own subject. Never open with "It", "This", "该技术". (H2 "What is programmatic SEO?" → "Programmatic SEO is…", not "It is…".)

**Rule 17** — Named-entity governance. Use specific products, standards, competitors, studies, dates, and institutions — they ground a claim and reduce model uncertainty. But every named entity must come from the context_pack or a traceable source. Do **not** invent brands/competitors, and do **not** stuff entities to hit a density target; unnatural entity density is itself an AI tell. If an entity is needed but unsourced, write `[Entity TBD]` and list it under To-Verify.

**Rule 18** — Primary-source attribution. State a statistic as: source name + year + sample size + subject ("Semrush's 2026 analysis of 337,785 URLs", not "recent research"). Prefer the primary study over a blog that cites it. If name, year, or sample size is missing, mark the claim medium/low confidence and hand it to `fact-checker`.

### Native American English — Positive Signals (Rules 19–22)

Rules 1–18 are subtractive: they remove AI flavor. Removing AI tells does not by itself produce native-sounding English — prose can be rule-clean and still read like a careful non-native writer. Rules 19–22 add the positive signals of American native fluency. They apply only to English-language articles.

**Rule 19 — Prefer phrasal and Anglo-Saxon verbs over Latinate verbs** when precision is equal. Native technical writing leans on short verbs; ESL and AI writing lean Latinate.

| ❌ Latinate default | ✅ Native default |
|---|---|
| ascertain / determine whether | figure out / check whether |
| commence / initiate | start / kick off |
| terminate | end / stop / kill (a process) |
| demonstrate | show |
| sufficient / insufficient | enough / not enough |
| purchase | buy |
| approximately | about / roughly |
| attempt to | try to |
| in order to | to |
| prior to | before |
| subsequently | then / later |

Keep Latinate words that ARE the technical term (configure, provision, deploy, calibrate, terminate a contract). This is about defaults, not bans.

**Rule 20 — American conventions, consistently.** American spelling (color, optimize, analyze, center, catalog); the serial comma; dates as "July 2, 2026"; sentence case for headings; periods and commas inside closing quotes. For US-facing deployment content, give imperial alongside metric on first use: "−40°C (−40°F)", "30 m (about 100 ft)".

**Rule 21 — Natural connective tissue.** Sentence-initial "And", "But", "So" are correct and native — use them instead of "However," / "Additionally," / "Therefore," most of the time. Contractions (it's, don't, you'll, that's) are the native default in blog prose; write them out only for emphasis ("do not skip this test"). Good transitions: "That said," "Even so," "In practice," "Here's the catch:", "The short version:". Native register is conversational precision — plain syntax carrying exact numbers — not formality.

**Rule 21a — American B2B idiom bank (verified, optional).** Real idioms from native industrial/B2B writing. Each is an *option* when the register fits — never a quota.

*Operations & buyer-pain vocabulary* (fits fleet managers, plant/warehouse ops, procurement):

| Idiom | Meaning / use |
|---|---|
| downtime spikes | 停机时间激增 — "Capacity drops and downtime spikes." |
| headcount | 人头/编制 — "without adding a single headcount" |
| out the door | 发货/出库 — "orders out the door in under 24 hours" |
| the math doesn't work / gets brutal | 这笔账算不过来 — cost-pressure framing |
| floor staff / shop-floor | 一线员工/车间现场 — "shop-floor realities" |
| your investment (for capital equipment) | 大宗设备称资产而非产品 |
| burn out (people) / wear out (equipment) | 人是 burn out,设备是 wear out |

*Engineer verbs & discourse moves* (fits engineer-to-engineer content):

| Idiom | Meaning / use |
|---|---|
| dial in (parameters, a process) | 精调到位 — "dial in the parameters" |
| know the drill | 你懂的/老流程了 — shared-experience opener |
| right off the bat | 一上来/立刻 — "flags design issues right off the bat" |
| workaround | 绕行方案 — more concrete than "solution" |
| bottleneck | 瓶颈 — name WHICH step is the bottleneck |
| blast radius (IT/security) | 故障波及面 |
| signal vs. noise | 有效信息 vs 噪音 |
| fighting a losing battle | 打注定输的仗 — for a doomed approach |
| flip the script | 彻底反转 — sparingly; marketing-adjacent |
| take you a long way | 能帮你走很远 — "These tips will take you a long way." |
| bring X to a grinding halt | 让项目/产线嘎然而止 — for a blocking failure |
| treat X as an afterthought | 把关键事项当事后补救 — critiques late-stage planning |
| can't [verb] your way out of | 靠 X 补救不了先天缺陷 — "you can't tune your way out of a bad sensor choice" |
| de-risk | 降风险 — compliance/procurement register (medical, finance, aero) |
| rack up (costs, penalties) | 费用迅速累积 — "racking up daily storage penalties" |
| line item / flag | 账单明细 / 标记提醒 — "a line item nobody flagged" |

*Guardrails* (violating these recreates the AI tell in the opposite direction):
1. **Max 1–2 idioms per article.** Stacked idioms read as an AI imitating a human.
2. **Match the reader.** Ops idioms for ops audiences, engineer idioms for engineers. A CTO whitepaper gets fewer than a fleet-manager blog post.
3. **Never in definition sentences or FAQ answers** — those must stay literal for citability (Rules 15–16).
4. **Never force one in during editing.** If it wasn't natural in drafting, it won't be natural in revision.
5. Idioms are seasoning on top of specificity, not a substitute for it. "Downtime spikes" still needs the number: "downtime spikes — 11 hours lost per line per month."

**Rule 22 — Kill translationese.** These phrasings are grammatical but mark the writer as non-native (Chinese-transfer patterns; `check_draft` warns on them as `[translationese]`):

| ❌ Translationese | ✅ Native fix |
|---|---|
| In recent years, … | Name the years: "Since 2023, …" |
| more and more X | "increasingly" — or state the number |
| X plays an important role in Y | Say what X does: "X cuts Y by 30%" |
| pay attention to X | watch for / check / mind X |
| with the development of X | Cut, or name the specific change |
| as we all know / as is known to all | Cut |
| it is worth mentioning that | Cut — state it |
| last but not least | finally — or nothing |
| a double-edged sword | State the actual trade-off |
| under the background of | given / amid — or cut |
| to some extent | Quantify it, or cut |
| the above-mentioned X | this X / that X |
| give full play to | use / get the most out of |

Also self-check the two grammar zones where Chinese-transfer errors cluster: articles (a/an/the — "the accuracy improves" → "accuracy improves" for general claims; "install BMS" → "install a BMS" for countables) and mass/count nouns (equipment, feedback, research take no plural).

### Chinese (中文) AI tells

When the article is in Chinese, cut the machine-typical phrasing the same way:

- 套话开场/收尾：值得注意的是 / 综上所述 / 总而言之 / 总的来说 / 不难看出 → 直接说要点。
- 时代套话：在当今……的时代 / 随着……的快速发展 / 在数字化浪潮下 → 删。
- 列表腔：首先……其次……最后 / 一方面……另一方面（机械套用时）→ 自然过渡或直接陈述。
- 空对仗：不仅……而且 / 不但……还（堆砌时）→ 拆成短句。
- 万能黑话：赋能 / 抓手 / 闭环 / 打法 / 一站式 / 无缝 / 强大 → 换成具体动作或数字。
- 虚词