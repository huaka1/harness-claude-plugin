---
description: "Resume the active Harness project"
argument-hint: "[optional project id or topic]"
---

Use the `harness` skill, then run:

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
python3 "$plugin_root/scripts/harness_state.py" resume --cwd "$PWD" --query "$ARGUMENTS"
```

Continue from the returned `handoff.md`, `status.md`, and `next-actions.md`. If the project is ambiguous, show the candidates from `.harness/index.md` and ask the user which one to resume.
