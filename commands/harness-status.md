---
description: "Show the active Harness project and current handoff"
---

Run:

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "Harness state script not found. Reinstall with: claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" status --cwd "$PWD"
```

Summarize the active project, current status, next actions, and any relevant project memory from the output. Do not scan the full repository unless the user asks.
