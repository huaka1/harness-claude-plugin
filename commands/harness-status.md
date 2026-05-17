---
description: "Show the active Harness project and current handoff"
---

Run:

```bash
plugin_root="${CLAUDE_PLUGIN_ROOT:-}"
if [ -z "$plugin_root" ]; then
  state_script="$(find "$HOME/.claude/plugins/cache" -path "*/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
  plugin_root="${state_script%/scripts/harness_state.py}"
fi
if [ -z "$plugin_root" ] || [ ! -f "$plugin_root/scripts/harness_state.py" ]; then
  echo "Harness plugin root not found. Run: claude plugin marketplace update harness && claude plugin update harness"
  exit 1
fi
python3 "$plugin_root/scripts/harness_state.py" status --cwd "$PWD"
```

Summarize the active project, current status, next actions, and any relevant project memory from the output. Do not scan the full repository unless the user asks.
