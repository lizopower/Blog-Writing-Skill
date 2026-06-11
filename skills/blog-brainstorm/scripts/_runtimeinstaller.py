#!/usr/bin/env python3
"""Install and manage project-local Blog-Writing-Skill runtime files."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


RUNTIME_ROOT = ".trellis-writing"
RUNTIME_SCRIPTS = PurePosixPath("runtime/scripts")
VERSION_FILE = ".version"
HASHES_FILE = ".template-hashes.json"
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parents[2]


@dataclass(frozen=True)
class TemplateFile:
    destination: PurePosixPath
    source: Path | None = None
    content: str | None = None

    def render(self) -> str:
        if self.content is not None:
            return self.content
        if self.source is None:
            raise ValueError(f"{self.destination}: missing source/content")
        return self.source.read_text(encoding="utf-8")


@dataclass(frozen=True)
class RuntimeUpdateResult:
    written: tuple[str, ...]
    conflicts: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeUninstallResult:
    removed: tuple[str, ...]
    preserved: tuple[str, ...]


def runtime_root(root: Path) -> Path:
    return root / RUNTIME_ROOT


def runtime_scripts_dir(root: Path) -> Path:
    return runtime_root(root) / "runtime" / "scripts"


def version_path(root: Path) -> Path:
    return runtime_root(root) / VERSION_FILE


def hashes_path(root: Path) -> Path:
    return runtime_root(root) / HASHES_FILE


def session_start_path(root: Path) -> Path:
    return runtime_scripts_dir(root) / "session_start.py"


def release_version() -> str:
    manifest = REPO_ROOT / ".codex-plugin" / "plugin.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "0.0.0"
    version = data.get("version")
    return str(version) if version else "0.0.0"


def template_files() -> list[TemplateFile]:
    return [
        TemplateFile(RUNTIME_SCRIPTS / "session_start.py", content=render_session_start()),
        TemplateFile(RUNTIME_SCRIPTS / "resume_context.py", source=SCRIPTS_DIR / "resume_context.py"),
        TemplateFile(
            RUNTIME_SCRIPTS / "inject_workflow_state.py",
            source=SCRIPTS_DIR / "inject_workflow_state.py",
        ),
        TemplateFile(RUNTIME_SCRIPTS / "_statemachine.py", source=SCRIPTS_DIR / "_statemachine.py"),
        TemplateFile(RUNTIME_SCRIPTS / "_specstore.py", source=SCRIPTS_DIR / "_specstore.py"),
        TemplateFile(RUNTIME_SCRIPTS / "phase_gate.py", source=SCRIPTS_DIR / "phase_gate.py"),
        TemplateFile(RUNTIME_SCRIPTS / "article.py", source=SCRIPTS_DIR / "article.py"),
        TemplateFile(
            RUNTIME_SCRIPTS / "create_article_workspace.py",
            source=SCRIPTS_DIR / "create_article_workspace.py",
        ),
    ]


def render_session_start() -> str:
    return '''#!/usr/bin/env python3
"""Project-local SessionStart entry for Blog-Writing-Skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit project-local writing context for SessionStart hooks.")
    parser.add_argument("--harness", choices=["claude", "codex"], default="codex")
    return parser


def session_start_envelope(context: str) -> dict[str, object]:
    # Claude and Codex SessionStart hooks share an identical wire format:
    # hookSpecificOutput.{hookEventName, additionalContext}. A single envelope
    # satisfies both schemas, so output no longer branches on --harness.
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }


def main(argv: list[str] | None = None) -> int:
    # Parse for validation/forward-compat only; the installed hook command still
    # passes --harness, but output format is now uniform across harnesses.
    _ = build_parser().parse_args(argv)

    from resume_context import render_context

    context = render_context(project_root())
    print(json.dumps(session_start_envelope(context), ensure_ascii=False), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def destination_path(root: Path, template: TemplateFile) -> Path:
    return runtime_root(root) / Path(template.destination.as_posix())


def registry_entry(template: TemplateFile, text: str) -> dict[str, str]:
    source = str(template.source.relative_to(REPO_ROOT)).replace("\\", "/") if template.source else "<generated>"
    return {"sha256": sha256_text(text), "source": source}


def load_hashes(root: Path) -> dict[str, Any]:
    path = hashes_path(root)
    if not path.exists():
        return {"version": release_version(), "files": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": release_version(), "files": {}}
    if not isinstance(data, dict):
        return {"version": release_version(), "files": {}}
    files = data.get("files")
    if not isinstance(files, dict):
        data["files"] = {}
    return data


def save_hashes(root: Path, registry: dict[str, Any]) -> None:
    path = hashes_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def install_runtime(root: Path) -> list[str]:
    root = root.resolve()
    messages: list[str] = []
    registry = load_hashes(root)
    registry["version"] = release_version()
    files = registry.setdefault("files", {})
    if not isinstance(files, dict):
        files = {}
        registry["files"] = files

    runtime_root(root).mkdir(parents=True, exist_ok=True)
    for template in template_files():
        text = template.render()
        path = destination_path(root, template)
        rel = template.destination.as_posix()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        files[rel] = registry_entry(template, text)
        messages.append(f"installed {RUNTIME_ROOT}/{rel}")

    version_path(root).write_text(release_version() + "\n", encoding="utf-8")
    save_hashes(root, registry)
    return messages


def ensure_runtime(root: Path) -> RuntimeUpdateResult:
    root = root.resolve()
    if hashes_path(root).exists():
        return update_runtime(root)
    written = tuple(message.removeprefix("installed " + RUNTIME_ROOT + "/") for message in install_runtime(root))
    return RuntimeUpdateResult(written, ())


def update_runtime(root: Path) -> RuntimeUpdateResult:
    root = root.resolve()
    registry = load_hashes(root)
    registry["version"] = release_version()
    files = registry.setdefault("files", {})
    if not isinstance(files, dict):
        files = {}
        registry["files"] = files

    written: list[str] = []
    conflicts: list[str] = []
    runtime_root(root).mkdir(parents=True, exist_ok=True)

    for template in template_files():
        text = template.render()
        path = destination_path(root, template)
        rel = template.destination.as_posix()
        stored = files.get(rel)
        stored_hash = stored.get("sha256") if isinstance(stored, dict) else None
        current_hash = sha256_text(path.read_text(encoding="utf-8")) if path.exists() else None

        if current_hash is not None and stored_hash is not None and current_hash != stored_hash:
            new_path = path.with_name(path.name + ".new")
            new_path.write_text(text, encoding="utf-8")
            conflicts.append(rel)
            continue

        if current_hash is not None and stored_hash is None:
            new_path = path.with_name(path.name + ".new")
            new_path.write_text(text, encoding="utf-8")
            conflicts.append(rel)
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        files[rel] = registry_entry(template, text)
        written.append(rel)

    version_path(root).write_text(release_version() + "\n", encoding="utf-8")
    save_hashes(root, registry)
    return RuntimeUpdateResult(tuple(written), tuple(conflicts))


def uninstall_runtime(root: Path) -> RuntimeUninstallResult:
    root = root.resolve()
    registry = load_hashes(root)
    files = registry.get("files")
    if not isinstance(files, dict):
        files = {}

    removed: list[str] = []
    preserved: list[str] = []
    for rel, entry in files.items():
        if not isinstance(rel, str) or not isinstance(entry, dict):
            continue
        path = runtime_root(root) / Path(rel)
        if not path.exists():
            removed.append(rel)
            continue
        stored_hash = entry.get("sha256")
        current_hash = sha256_text(path.read_text(encoding="utf-8"))
        if current_hash == stored_hash:
            path.unlink()
            removed.append(rel)
        else:
            preserved.append(rel)

    if not preserved:
        for metadata in (hashes_path(root), version_path(root)):
            if metadata.exists():
                metadata.unlink()

    _remove_empty_dirs(runtime_root(root))
    return RuntimeUninstallResult(tuple(removed), tuple(preserved))


def _remove_empty_dirs(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        return
    for child in sorted((item for item in path.rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
        try:
            child.rmdir()
        except OSError:
            pass
    try:
        path.rmdir()
    except OSError:
        pass
