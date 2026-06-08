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

**Rule 2**: Every paragraph must contain at least one sentence shorter than five words.

Examples of qualifying short sentences:
- "Here's why."
- "It failed."
- "Check the data."
- "Not anymore."
- "That matters."

**Rule 3**: Every fourth paragraph should contain only one sentence.

This creates breathing room. A single-sentence paragraph forces the reader to pause, absorb, and reset before the next block of information.

**Self-Check Method**:
1. After writing each section, count sentence lengths
2. Flag any run of three+ sentences within ±5 words of each other
3. Verify each paragraph has its sub-five-word sentence
4. Count paragraphs — every fourth one should stand alone

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

**Rule 5**: Maximum one adjective per sentence.

Not "the robust, reliable, high-performance [product unit]." Pick one. "The [N]-cycle [product unit]." Let the noun carry weight.

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

**Rule 14**: Prefer active voice; commit, don't hedge. Convert passive to active when a real actor exists ("the BMS cuts current", not "current is cut"). Contractions are fine in moderation (it's, don't). But do **not** manufacture a casual/"coffee-chat" voice, personal anecdotes, slang, or hedging ("honestly", "in my experience", "perhaps in most cases") — those belong to lifestyle blogging, not source-backed B2B technical writing.

### Chinese (中文) AI tells

When the article is in Chinese, cut the machine-typical phrasing the same way:

- 套话开场/收尾：值得注意的是 / 综上所述 / 总而言之 / 总的来说 / 不难看出 → 直接说要点。
- 时代套话：在当今……的时代 / 随着……的快速发展 / 在数字化浪潮下 → 删。
- 列表腔：首先……其次……最后 / 一方面……另一方面（机械套用时）→ 自然过渡或直接陈述。
- 空对仗：不仅……而且 / 不但……还（堆砌时）→ 拆成短句。
- 万能黑话：赋能 / 抓手 / 闭环 / 打法 / 一站式 / 无缝 / 强大 → 换成具体动作或数字。
- 虚词冗余：众所周知 / 毋庸置疑 / 不言而喻 → 删，并给出证据。

### What "human" does NOT mean

This is engineer-to-engineer B2B writing. "Removing AI flavor" means **more specificity, not artificial messiness**. Some popular "humanize to beat AI detectors" advice is wrong for this skill — explicitly reject it:

- ✅ Do: concrete numbers, named mechanisms, real test conditions, one clear idea per sentence, a stated point of view backed by the context_pack.
- ❌ Do NOT: insert fake typos, deliberate grammar errors, run-ons, filler interjections, slang, or hedging to dodge AI detectors. Do NOT add invented anecdotes or a chatty "over coffee" tone. That destroys B2B credibility, can fabricate unsourced claims, and is not the goal. Authenticity comes from real data and real reasoning, not from sounding sloppy or casual.

### Rhythm Examples

**❌ AI-typical (monotone rhythm)**:
> The [product unit] maintains 90% [performance metric] at [extreme threshold]. The [control system] provides six layers of protection. The [core components] passed all safety tests. The [product unit] weighs approximately [weight value].

**✅ Human rhythm (varied)**:
> At [extreme threshold], this [product unit] holds 90% [performance metric]. That's the headline. The [control system] backs it up with six protection layers, and every [core component] cleared safety testing — [test 1], [test 2], [test 3], the full gauntlet. Weight sits at [weight value].

**❌ AI-typical (abstract + banned words)**:
> This solution is very reliable and essentially provides really good performance in basically all extreme weather conditions.

**✅ Human (concrete + no banned words)**:
> This [product unit] delivers [N]+ usable [output unit] at [extreme threshold] and survives [N] [operating cycles] before hitting 80% [performance metric].

---

### ✅ Correct Tone Examples

1. **Authoritative without arrogance**:
   > "[Variant B] wins for most [target deployment] applications."

2. **Precise without being academic**:
   > "At [threshold], [Variant A] retains 70-80% vs [Variant B]'s 50-60%."

3. **Honest about limitations**:
   > "Below [extreme threshold], or for applications with short expected lifespans, [Variant A] becomes a valid consideration."

4. **Practical with real consequences**:
   > "Get this wrong, and even the best [core components] and [control system] won't deliver expected performance."

### ❌ Wrong Tone Examples

1. **Too academic**:
   > "Research indicates that [Variant B] may potentially offer advantages in certain scenarios."

2. **Too marketing**:
   > "Our revolutionary [product category] delivers unmatched performance!"

3. **Too vague**:
   > "Performance varies depending on conditions."

4. **Too passive**:
   > "It should be noted that consideration should be given to..."

---

*Use this guide when writing technical blog content to maintain consistent voice and style.*
