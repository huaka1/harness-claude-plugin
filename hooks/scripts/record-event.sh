#!/usr/bin/env bash
set -euo pipefail

event="${1:-}"
plugin_root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"

python3 "$plugin_root/scripts/harness_state.py" record-event --cwd "$PWD" --event "$event" 2>/dev/null || printf '{}\n'
