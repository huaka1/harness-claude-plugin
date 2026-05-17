---
description: "Show the active Harness project and current handoff"
---

Run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/harness_state.py" status --cwd "$PWD"
```

Summarize the active project, current status, next actions, and any relevant project memory from the output. Do not scan the full repository unless the user asks.
