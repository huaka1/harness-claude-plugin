#!/usr/bin/env bash
set -euo pipefail

plugin_root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"

context="$(python3 "$plugin_root/scripts/harness_state.py" stop --cwd "$PWD" 2>/dev/null || true)"

python3 - "$context" <<'PY'
import json
import sys

context = sys.argv[1]
print(json.dumps({
    "decision": "approve",
    "reason": "Harness stop hook completed.",
    "systemMessage": context,
}))
PY
