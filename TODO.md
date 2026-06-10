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

### Risk
The remaining risk is not command availability; it is clean-profile behavior:
whether a first-time user can add this GitHub repository as a marketplace,
install `blog-writing-skills`, update it, and get the expected namespaced skill
routes without manual filesystem repair.

### Acceptance criteria
- [ ] Confirm install and update behavior from a clean Claude Code profile.
- [ ] Confirm namespaced skill routing works after plugin install.
- [ ] Confirm uninstall/reinstall leaves no stale plugin state.
- [ ] If any clean-profile issue appears, demote the plugin path back below the
      standalone installer and document the failure mode.

### Verification path
- Use a disposable Claude Code profile or test machine.
- Run install, update, and uninstall commands end to end.
- Verify the agent can see `blog-writing-skills:<skill>` routes afterward.

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
