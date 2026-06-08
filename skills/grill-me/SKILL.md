---
name: grill-me
description: Use when the user wants to be relentlessly questioned about a technical/B2B blog, article, white paper, content strategy, outline, angle, evidence plan, or editorial decision until the plan is pressure-tested and agreed.
---

# Grill-Me Skill

Pressure-test a technical/B2B content plan by walking the user through the decision tree one branch at a time until the article strategy is clear, defensible, and shared.

## When to Use This Skill

Use when the user asks to:
- "grill me", "追问我", "拷问我", "challenge this", "pressure-test this", or "stress-test this".
- Deeply review a blog idea, outline, angle, argument, claim set, evidence plan, visual plan, CTA, or publishing strategy.
- Decide whether a topic is worth writing before drafting.
- Resolve content strategy choices where multiple directions are plausible.

This skill must trigger before drafting when the user explicitly asks to be questioned or pressure-tested.

## Not For / Boundaries

- Do not write the final article directly. Route to `tech-blog-writer` after the plan is settled.
- Do not invent facts, market claims, citations, or audience evidence. If evidence is missing, ask for it or recommend `tech-research`, `audience-pain-point-research`, or `tech-blog-orchestrator`.
- Do not ask questions whose answers can be derived from available files, code, context_pack, outline, or prior conversation. Inspect first, then ask only what remains unresolved.
- Do not ask multiple questions at once.

## Operating Rules

1. Ask exactly one question at a time.
2. For each question, include your recommended answer and why.
3. Do not treat your recommended answer as the user's answer.
4. After asking a question, stop and wait for an explicit user reply before continuing.
5. Do not continue to the next question, outline, draft, or handoff until the user answers, unless the user explicitly requested autopilot/no-interaction mode.
6. Walk the decision tree in dependency order: goal -> audience -> pain -> angle -> evidence -> structure -> claims -> visuals -> CTA -> quality gate.
7. After each user answer, update the working understanding before asking the next question.
8. Continue until every material branch is resolved or the user stops the grilling.
9. When finished, summarize decisions, unresolved risks, and the next sub-skill to invoke.

## Handoff

- If the plan lacks source material, hand off to `tech-research`, `audience-pain-point-research`, or `tech-blog-orchestrator`.
- If the plan has a context_pack but no outline, hand off to `tech-article-architect`.
- If the plan has both outline and context_pack, hand off to `tech-blog-writer`.
- If a draft exists with factual claims, hand off to `fact-checker`.
