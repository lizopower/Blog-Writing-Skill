# Versioning Policy

This bundle uses **three independent, clearly scoped version numbers**. Do not
hand-maintain a version string anywhere else — that is what caused drift in
earlier releases.

| Scope | Source of truth | Current | Bump when |
|-------|-----------------|---------|-----------|
| **Release version** | `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/marketplace.json` (must always agree) | `2.2.0` | Any user-visible change to skills, routing, docs, or packaging. |
| **Context Pack data contract** | `schemas/context_pack_schema.json` (`version` field) | `2.2.0` | The Context Pack JSON shape changes (fields added/removed/retyped). Downstream validators key off this. |
| **Standards / templates** | Front-matter `version:` in `standards/*.md` and `templates/*.md` | per file | The individual standard or template changes. These are reusable documents with their own lifecycle. |

## Rules

1. The three **release-version** files must always carry the same number. A CI
   check or reviewer should reject a PR where they diverge.
2. The **data-contract** version is decoupled from the release version on
   purpose: the package can ship many releases without changing the Context Pack
   shape.
3. **Per-skill `SKILL.md` files do NOT carry their own version.** A skill's
   version is the release version. (Footers may keep `Role:` / `Output:` /
   `Industry:` lines for orientation, but never a `Version:` line.)
4. When you cut a release, bump the three release-version files together and tag
   the repo (`git tag v2.2.0`).

## Quick check

```bash
python scripts/check_versions.py     # asserts the 3 release files agree
python scripts/check_router_sync.py  # asserts BOTH routers reference every sub-skill
```
