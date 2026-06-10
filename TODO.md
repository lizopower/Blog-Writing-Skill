# TODO / Deferred Work

Tracked items that are intentionally deferred. Each entry should carry enough
context, acceptance criteria, and a verification path to be picked up cold.

---

## 1. End-to-end validate Claude Code native plugin marketplace install/update path

**Status:** open · **Opened:** 2026-06-10 · **Area:** `.claude-plugin`, `README.md`

### Context
The repository already ships `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json`. Local CLI help confirms that Claude Code
supports `plugin marketplace add`, `plugin install`, and `plugin update`; the
README now presents this as the preferred Claude Code path.

Follow-up testing found the practical failure mode this is meant to avoid:
standalone filesystem installs can expose the root router, but they do not
guarantee that nested sub-skills resolve through
`blog-writing-skills:<sub-skill>`. When namespace resolution fails, an agent can
receive only a generic "invoke the skill" hint instead of the actual sub-skill
`SKILL.md` instructions, then accidentally write outside the pipeline.

### Risk
The remaining risk is not command availability; it is clean-profile behavior:
whether a first-time user can add this GitHub repository as a marketplace,
install `blog-writing-skills`, update it, and get the expected namespaced skill
routes without manual filesystem repair.

### Acceptance criteria
- [ ] Confirm install and update behavior from a clean Claude Code profile.
- [ ] Confirm namespaced skill routing works after plugin install.
- [ ] Confirm calling `blog-writing-skills:tech-blog-orchestrator` injects the
      actual sub-skill instructions, not just a generic reminder.
- [ ] Confirm a topic-only article request routes to `blog-writing-workflow`
      and does not fall through to manual search/drafting.
- [ ] Confirm uninstall/reinstall leaves no stale plugin state.
- [ ] If any clean-profile issue appears, demote the plugin path back below the
      standalone installer and document the failure mode.

### Verification path
- Use a disposable Claude Code profile or test machine.
- Run install, update, and uninstall commands end to end.
- Verify the agent can see `blog-writing-skills:<skill>` routes afterward.

### Execution plan (handoff)

**Critical split — this item cannot be done entirely by Codex.** Half the
acceptance criteria are Claude Code *runtime* behaviors that an external shell
(Codex) cannot observe. Assign the two halves to the right executor.

**Part A — mechanical (Codex / any shell can do this):**
1. On a disposable Claude Code profile, add this repo as a marketplace:
   `claude plugin marketplace add <repo-url-or-path>`.
2. `claude plugin install blog-writing-skills`; capture the installed location
   and the resolved plugin manifest (`.claude-plugin/plugin.json`,
   `marketplace.json`) version (expect `3.7.0`).
3. `claude plugin update blog-writing-skills`; confirm it moves to the latest
   tag without manual filesystem repair.
4. Inspect the installed plugin to confirm all 15 sub-skills are registered
   (cross-check against `check_router_sync.py`).
5. `claude plugin uninstall blog-writing-skills`, then reinstall; confirm **no
   stale state** is left behind (no orphaned skill dirs, settings, or cache).

**Part B — runtime routing (must run inside a real Claude Code session):**
6. After plugin install, confirm `blog-writing-skills:<sub-skill>` namespace
   routes are actually visible/usable in the session.
7. Invoke `blog-writing-skills:tech-blog-orchestrator` and confirm it injects
   the **actual sub-skill SKILL.md content**, not a generic "invoke the skill"
   reminder. This is the failure mode this item exists to catch.
8. Make a topic-only article request and confirm it auto-routes to
   `blog-writing-workflow` rather than falling through to manual search/drafting.

**Outcome branches:**
- PASS (both parts): record evidence (profile state, Claude Code version, date)
  against the checkboxes above and close this item. README's plugin-first
  ordering stands.
- FAIL (any Part B check, esp. step 7): demote the plugin path back **below**
  the standalone installer in `README.md`, document the exact failure mode
  (which sub-skill, generic-hint vs real-content), keep the standalone install
  as the recommended Claude path, then bump the release version and commit.

**Caution:** Parts A and B need different access — A is shell/CLI, B needs a
live Claude Code session to introspect what actually got injected. Codex should
execute Part A and report state; Part B is run in Claude Code (by the Claude
agent or the user).

---

## 2. Real-host validation of the Codex SessionStart envelope

**Status:** open · **Opened:** 2026-06-09 · **Area:** `skills/blog-brainstorm/scripts`

### Context
Commit `28312e6` unified the SessionStart hook output so that **both** `--harness
claude` and `--harness codex` emit the same JSON envelope:

```json
{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}
```

The Codex path was changed on the basis of a **schema match** against the OpenAI
Codex generated output schema
(`codex-rs/hooks/schema/generated/session-start.command.output.schema.json`),
whose `hookSpecificOutput` wire format is field-for-field identical to Claude's.

This is a sound inference, but it has **not been validated against a live Codex
host**. The original implementation deliberately kept Codex on naked stdout
pending real-host confirmation; that guard was removed when the envelope was
unified.

### Risk
If a real Codex host does not consume `hookSpecificOutput.additionalContext` the
way the schema implies, the injected writing context would be silently dropped on
SessionStart for Codex users — no error, just missing context.

### Acceptance criteria
- [ ] Install the hook into a real Codex project: `python install_session_hook.py --harness codex --root <project>`
- [ ] Start a Codex session in a project that has an active article workspace
- [ ] Confirm the article context (e.g. `Current Target: <slug>`, `Phase: ...`)
      actually appears in the Codex session context — not just in stdout
- [ ] If it does NOT surface, restore a harness-specific output branch (the
      pre-`28312e6` naked-stdout behavior) for Codex and add a regression test
      asserting the host-correct format

### Verification path
- Unit/CLI coverage already exists:
  `tests/test_init.py::test_project_local_session_start_prints_codex_json_envelope`
  proves the script emits the envelope. The remaining gap is purely the
  **host-consumption** behavior, which cannot be asserted from this repo's tests.

### Execution plan (Codex handoff)

This is a read-only investigation plus a *conditional* code change: code only
changes if the host-consumption check fails.

**Known facts (do not re-investigate):**
- Codex hook config: `<project>/.codex/hooks.json`, event `SessionStart`, three
  matchers (`startup` / `clear` / `compact`), command
  `python .trellis-writing/runtime/scripts/session_start.py --harness codex`
  (timeout 10).
- Emitted envelope (`session_start.py` → stdout):
  `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<resume_context output>"}}`.
- `additionalContext` is the output of `resume_context.py`: `Current Target`,
  `Phase`, `Track`, per-phase required files, next phases, blocked gates, specs.
- Install: `python skills/blog-brainstorm/scripts/init.py --root <project> --harness codex`.
- Envelope source: `_runtimeinstaller.py::render_session_start` and
  `session_start_envelope`; output no longer branches on `--harness` since
  `28312e6` (which removed the pre-existing naked-stdout branch for Codex on a
  schema match alone, never validated on a live host).

**Steps:**
1. Build a throwaway project: `init.py --root <project> --harness codex`, then
   create an in-progress workspace `content/articles/<slug>/article.json` with
   `currentPhase` set to e.g. `drafting` (not `completed`).
2. Baseline (emit side, always works): run
   `python .trellis-writing/runtime/scripts/session_start.py --harness codex`
   in the project root; confirm stdout is a valid envelope whose
   `additionalContext` contains `Current Target: <slug>`.
3. Consume side (the actual question): open a **fresh Codex thread** in that
   project (triggers the `startup` matcher). Without reading any files, ask:
   "Which article is currently in progress and what phase is it in?"
   - Answers with `Current Target` / `Phase` → injection works.
   - No idea / needs to read files → injection was dropped.
4. Repeat for the `clear` and `compact` matchers. Capture any Codex hook debug
   logs as evidence that the hook fired and stdout was consumed.

**Outcome branches:**
- PASS: record host version + date + observation against the acceptance
  checkboxes above and close this item. No code change.
- FAIL: (a) restore harness-branched output — Codex back to naked stdout
  (pre-`28312e6`), Claude keeps the envelope; (b) add a regression test
  asserting `--harness codex` emits naked stdout and `--harness claude` emits
  the envelope; (c) note in `CHANGELOG.md` that the v3.7.0 `AGENTS.md` prelude
  is now Codex's primary context path, not a fallback; (d) run the full suite,
  bump the release version, commit.

**Cautions:** do not use `--harness all` (keep the test isolated to Codex). The
consume-side check is self-observational — the executing Codex must open a new
thread *inside the target project* to trigger injection, then reason about
whether it already knows the workspace state without reading files.
