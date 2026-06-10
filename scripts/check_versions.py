#!/usr/bin/env python3
"""Assert all release-version files agree.

See VERSIONING.md. The release version lives in VERSION plus the release
manifests; they must always carry the same value. Run in CI or before tagging a
release.

Exit 0 if consistent, 1 otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RELEASE_FILES = {
    "VERSION": (),
    ".claude-plugin/plugin.json": ("version",),
    ".codex-plugin/plugin.json": ("version",),
    ".claude-plugin/marketplace.json": ("plugins", 0, "version"),
}


def dig(data, path):
    for key in path:
        data = data[key]
    return data


def main() -> int:
    versions: dict[str, str] = {}
    for rel, path in RELEASE_FILES.items():
        f = ROOT / rel
        try:
            if path:
                versions[rel] = dig(json.loads(f.read_text(encoding="utf-8")), path)
            else:
                versions[rel] = f.read_text(encoding="utf-8").strip()
        except (OSError, KeyError, IndexError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read version from {rel}: {exc}")
            return 1

    unique = set(versions.values())
    for rel, v in versions.items():
        print(f"  {v}  {rel}")
    if len(unique) != 1:
        print(f"FAIL: release versions diverge: {sorted(unique)}")
        return 1
    print(f"OK: all release files agree on {unique.pop()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
