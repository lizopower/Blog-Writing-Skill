#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${BLOG_WRITING_SKILL_REPO:-https://github.com/lizopower/Blog-Writing-Skill.git}"
SKILL_NAME="${BLOG_WRITING_SKILL_NAME:-blog-writing-skills}"
TARGET="${1:-all}"

usage() {
  cat <<'USAGE'
Usage:
  scripts/install.sh [codex|claude|all]

Environment:
  BLOG_WRITING_SKILL_REPO   Override git repository URL.
  BLOG_WRITING_SKILL_NAME   Override installed skill folder name.

Examples:
  curl -fsSL https://raw.githubusercontent.com/lizopower/Blog-Writing-Skill/main/scripts/install.sh | bash -s -- codex
  curl -fsSL https://raw.githubusercontent.com/lizopower/Blog-Writing-Skill/main/scripts/install.sh | bash -s -- claude
USAGE
}

timestamp() {
  date +%Y%m%d%H%M%S
}

install_one() {
  local host="$1"
  local base
  case "$host" in
    codex) base="$HOME/.codex/skills" ;;
    claude) base="$HOME/.claude/skills" ;;
    *) echo "ERROR: unknown host: $host" >&2; exit 2 ;;
  esac

  local dest="$base/$SKILL_NAME"
  mkdir -p "$base"

  if [ -d "$dest/.git" ]; then
    local origin=""
    origin="$(git -C "$dest" remote get-url origin 2>/dev/null || true)"
    if [ "$origin" = "$REPO_URL" ] || [[ "$origin" == *"lizopower/Blog-Writing-Skill"* ]]; then
      echo "Updating $host install at $dest"
      git -C "$dest" pull --ff-only
      return
    fi

    local backup="${dest}.backup-$(timestamp)"
    echo "Existing git checkout has different origin ($origin); moving to $backup"
    mv "$dest" "$backup"
  elif [ -e "$dest" ]; then
    local backup="${dest}.backup-$(timestamp)"
    echo "Existing copy install found; moving to $backup"
    mv "$dest" "$backup"
  fi

  echo "Installing $host skill to $dest"
  git clone --depth 1 "$REPO_URL" "$dest"
}

case "$TARGET" in
  codex|claude) install_one "$TARGET" ;;
  all)
    install_one codex
    install_one claude
    ;;
  -h|--help|help) usage ;;
  *)
    usage >&2
    exit 2
    ;;
esac

cat <<'DONE'

Done. Restart the agent or start a new session so the skill index is re-scanned.
For research workflows, also verify Tavily with: tvly --status
DONE
