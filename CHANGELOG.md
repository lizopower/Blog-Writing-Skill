# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
follows the release-version policy in [`VERSIONING.md`](VERSIONING.md): the
`VERSION` file, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and
`.claude-plugin/marketplace.json` always carry the same number.

For history predating this file, see the git log.

## [3.7.0]

### Added
- Codex lifecycle prelude fallback. Codex has no `PreToolUse` hook, so the
  mechanical phase gate that protects Claude sessions cannot run there. Codex
  installs now write a managed lifecycle prelude block into the project-root
  `AGENTS.md`, mandating that agents run `resume_context.py` first and honor the
  same artifact gates by convention.
  - New pure module `_agentsmd.py` (marker-delimited block, render/upsert/remove
    helpers). The gated artifact list is sourced from
    `phase_gate.ARTIFACT_MIN_PHASE`, so the prose prelude can never drift from
    the mechanical gate.
  - `install_session_hook.py` gained `write_prelude`/`clear_prelude`, invoked on
    install/uninstall for any harness without a mechanical gate (Codex).
  - The managed block is appended non-destructively — user-authored `AGENTS.md`
    content is preserved — and `--uninstall` strips only the managed block,
    removing the file only when the block was its sole content.
- `tests/test_agentsmd.py` (12 tests) covering render, idempotent upsert,
  in-place replace, content preservation, and the install/uninstall round trip.

### Changed
- `README.md` documents the Codex `AGENTS.md` prelude behavior in the
  "One-command project init" section.

## [3.6.0]

### Added
- Mechanical lifecycle gates (Trellis-parity hardening). A `PreToolUse` phase
  gate (`phase_gate.py`, fail-open) denies premature writes to `outline.md`,
  `draft.md`, `fact_check.md`, and `editorial_review.md`. Hooks are installed
  automatically on `article.py create`, and `resume_context.py` loads exactly
  the artifacts each phase needs.

## [3.4.0]

### Added
- Installer-first setup path.
- SERP strategy and on-page SEO finalizer layers.

### Fixed
- Blog workflow gate enforcement and plugin skill resolution clarifications.

## [3.3.0]

### Added
- Unified SessionStart envelope emitted for all harnesses.
- Project-local writing runtime installed by `init.py`.
- Trellis lifecycle and spec store.

### Fixed
- Waiver no longer bypasses phase legality in the state machine.
- UTF-8 stdout forced to prevent GBK console crashes on Windows.

## [3.0.0] – [3.2.0]

See the git log for the detailed history of these releases (governed style and
offering context, AEO/GEO citation signals, anti-AI style rules, and packaging
changes).

[3.7.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.7.0
[3.6.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.6.0
[3.4.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.4.0
[3.3.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.3.0
