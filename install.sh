#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -eq 0 ]; then
  exec "$SCRIPT_DIR/scripts/install.sh" cli
fi

exec "$SCRIPT_DIR/scripts/install.sh" "$@"
