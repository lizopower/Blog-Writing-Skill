# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
follows the release-version policy in [`VERSIONING.md`](VERSIONING.md): the
`VERSION` file, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and
`.claude-plugin/marketplace.json` always carry the same number.

For history predating this file, see the git log.

## [4.1.0]

### Added
- Mechanical draft linter `check_draft.py` with article-type profiles (`standards/article_type_profiles.md`).
- Reference corpus contract (`standards/reference_corpus_contract.md`) and `content/reference/` scaffold on `bws init`.
- Genre convention extractor `extract_genre_conventions.py` + `schemas/genre_conventions_schema.json`.
- Near-duplicate audit `audit_near_duplicate.py` for draft vs sources/reference.
- Stage runner `bws run` / `run_stage.py` with prompt templates under `templates/prompts/`.
- Draft normalizer `normalize_draft.py` (optional workflow step 7b).
- Append-only `logs/pipeline.log` receipts on `article.py advance`; `resume_context.py` shows recent entries.

### Changed
- `content-taste-advisor` now owns `editorial_review` lifecycle: writes `editorial_review.md` and advances to `completed`.
- `blog-writing-workflow` adds required step 10 (editorial review) and optional normalize step 7b.
- `completed` gate requires `Publishability: PASS` in `editorial_review.md`.
- `validate_article_workspace.py` validates `articleType` against known profiles.
- CI runs tech-blog-writer, tech-article-architect, and fact-checker script tests.

### Fixed
- Unified `articleType` enum across create, validate, and CLI (`guide` no longer accepted).
- Runtime installer now copies `templates/prompts/` so `bws run` works in installed projects.
- Pipeline log write failures surface as stderr warnings instead of silent drops.
- Clarified `finish.md` vs `completed` lifecycle gate in workflow docs.

## [3.8.0]

### Added
- Scaffold-first install path. Root `install.ps1` / `install.sh` now install the
  lightweight `blog-writing` and `bws` CLI shims by default, so users can clone
  the repo and initialize writing projects without global skill/plugin setup.
- Claude scaffold-only project instructions. Claude `init` now writes a managed
  `CLAUDE.md` block pointing at the scaffold checkout and the relevant workflow
  files, so Claude Code can follow Blog-Writing-Skill even when plugin/skill
  discovery is unavailable.
- `bws check` / doctor validation for the managed Claude project instruction
  block.

### Changed
- README first-screen install flow now emphasizes the recommended
  scaffold + CLI setup, followed by per-project `bws init` / `bws check`.
- Full-article routing rules now explicitly state that rich user input is raw
  workflow material, not permission to bypass Context Pack validation, outline,
  drafting, and fact-check stages.
- Tavily usage on Windows now defaults to `-o` file output for JSON/raw content
  to avoid GBK console crashes with Chinese or other non-ASCII text.
- Documented the controlled fan-out boundary: main session owns canonical
  artifacts and phase advancement; workers may only produce scratch outputs.

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

[4.1.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v4.1.0
[3.8.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.8.0
[3.7.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.7.0
[3.6.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.6.0
[3.4.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.4.0
[3.3.0]: https://github.com/lizopower/Blog-Writing-Skill/releases/tag/v3.3.0
