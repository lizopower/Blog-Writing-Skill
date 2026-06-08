# Review Summary

## Problem

Agents could read Blog-Writing-Skill as a writing-style reference, then draft directly instead of executing the required `blog-writing-workflow` pipeline.

## Changes

- Added an execution contract to the root router, Codex plugin router, and workflow skill.
- Explicitly prohibited extracting style/voice guidance from bundle files to bypass the workflow.
- Clarified that disabling CCG, project management, task archival, or similar process frameworks does not waive Blog-Writing-Skill stages.
- Required dependency blockers to stop and report options instead of silently producing simplified drafts.
- Added a structured workflow receipt table to `references/output-format.md`.
- Required partial receipts when the workflow blocks before completion.

## Dual-Model Review

- Gemini review: PASS.
- Claude review: PASS after fixes.
- Initial Claude findings:
  - Receipt format was underspecified.
  - Style-reference scope was too narrow.
  - Process-framework wording was inconsistent.
  - Rationale was missing.
- Fixes applied:
  - Added explicit production-pipeline rationale.
  - Expanded scope to all bundle files, including sub-skills, references, assets, templates, and examples.
  - Normalized process-framework wording.
  - Added a concrete workflow receipt format and partial-receipt rule.

## Local Checks

- `python scripts/check_router_sync.py`
- `python scripts/check_versions.py`
- `git diff --check`

## Result

No blocking issues remain.
