#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${BLOG_WRITING_SKILL_REPO:-https://github.com/lizopower/Blog-Writing-Skill.git}"
SKILL_NAME="${BLOG_WRITING_SKILL_NAME:-blog-writing-skills}"
MARKETPLACE_SOURCE="${BLOG_WRITING_SKILL_MARKETPLACE_SOURCE:-}"
MARKETPLACE_NAME="${BLOG_WRITING_SKILL_MARKETPLACE_NAME:-blog-writing-marketplace}"
TARGET="${1:-all}"
BIN_DIR="${BLOG_WRITING_SKILL_BIN:-$HOME/.local/bin}"
LAST_STANDALONE_DEST=""

usage() {
  cat <<'USAGE'
Usage:
  scripts/install.sh [codex|claude|claude-plugin|claude-standalone|cli|all]

Environment:
  BLOG_WRITING_SKILL_REPO   Override git repository URL.
  BLOG_WRITING_SKILL_NAME   Override installed skill folder name.
  BLOG_WRITING_SKILL_MARKETPLACE_SOURCE
                            Override Claude marketplace source (default: derived from repo URL).
  BLOG_WRITING_SKILL_MARKETPLACE_NAME
                            Override Claude marketplace name (default: blog-writing-marketplace).
  BLOG_WRITING_SKILL_BIN    Override CLI shim directory (default: ~/.local/bin).

Examples:
  curl -fsSL https://raw.githubusercontent.com/lizopower/Blog-Writing-Skill/main/scripts/install.sh | bash -s -- codex
  curl -fsSL https://raw.githubusercontent.com/lizopower/Blog-Writing-Skill/main/scripts/install.sh | bash -s -- claude
  curl -fsSL https://raw.githubusercontent.com/lizopower/Blog-Writing-Skill/main/scripts/install.sh | bash -s -- claude-standalone
  ./scripts/install.sh cli
USAGE
}

timestamp() {
  date +%Y%m%d%H%M%S
}

claude_marketplace_source() {
  if [ -n "$MARKETPLACE_SOURCE" ]; then
    printf '%s\n' "$MARKETPLACE_SOURCE"
    return
  fi

  case "$REPO_URL" in
    https://github.com/*/*.git|https://github.com/*/*)
      local slug="${REPO_URL#https://github.com/}"
      printf '%s\n' "${slug%.git}"
      ;;
    git@github.com:*/*.git|git@github.com:*/*)
      local slug="${REPO_URL#git@github.com:}"
      printf '%s\n' "${slug%.git}"
      ;;
    *)
      printf '%s\n' "$REPO_URL"
      ;;
  esac
}

is_already_configured_message() {
  printf '%s' "$1" | grep -Eiq 'already[[:space:]-]*(exists|configured|added)|marketplace.*already|source.*already'
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
  LAST_STANDALONE_DEST="$dest"
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

install_cli_shim() {
  local skill_dir="$1"
  local entry="$skill_dir/scripts/blog-writing.py"
  if [ ! -f "$entry" ]; then
    echo "WARNING: CLI entry not found at $entry; skipping blog-writing shim." >&2
    return
  fi

  mkdir -p "$BIN_DIR"
  cat > "$BIN_DIR/blog-writing" <<EOF
#!/usr/bin/env sh
exec python3 "$entry" "\$@"
EOF
  chmod +x "$BIN_DIR/blog-writing"
  ln -sf "$BIN_DIR/blog-writing" "$BIN_DIR/bws"

  echo "Installed CLI shim: $BIN_DIR/blog-writing"
  echo "Alias installed: $BIN_DIR/bws"
  case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) echo "NOTE: add $BIN_DIR to PATH to run 'blog-writing init' from any directory." ;;
  esac
}

install_claude_plugin() {
  if ! command -v claude >/dev/null 2>&1; then
    echo "ERROR: claude CLI not found. Use target 'claude-standalone' for a filesystem skill install." >&2
    exit 1
  fi

  local source
  local qualified_plugin
  local output
  local status
  source="$(claude_marketplace_source)"
  qualified_plugin="${SKILL_NAME}@${MARKETPLACE_NAME}"

  echo "Adding/updating Claude Code marketplace source"
  set +e
  output="$(claude plugin marketplace add "$source" 2>&1)"
  status=$?
  set -e
  if [ -n "$output" ]; then
    printf '%s\n' "$output"
  fi
  if [ "$status" -ne 0 ]; then
    if is_already_configured_message "$output"; then
      echo "Marketplace source already configured; continuing."
    else
      echo "ERROR: Claude marketplace add failed for source: $source" >&2
      exit "$status"
    fi
  fi

  echo "Installing/updating Claude Code plugin: $qualified_plugin"
  claude plugin install "$qualified_plugin" || claude plugin update "$qualified_plugin"
}

case "$TARGET" in
  codex)
    install_one codex
    install_cli_shim "$LAST_STANDALONE_DEST"
    ;;
  claude|claude-plugin) install_claude_plugin ;;
  cli) install_cli_shim "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" ;;
  claude-standalone)
    install_one claude
    install_cli_shim "$LAST_STANDALONE_DEST"
    ;;
  all)
    install_one codex
    install_cli_shim "$LAST_STANDALONE_DEST"
    install_claude_plugin
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
