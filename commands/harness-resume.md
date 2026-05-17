---
description: "Resume the active Harness project"
argument-hint: "[optional project id or topic]"
---

Use the `harness` skill, then run:

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "Harness state script not found. Reinstall with: claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" resume --cwd "$PWD" --query "$ARGUMENTS"
```

Continue from the returned `handoff.md`, `status.md`, and `next-actions.md`. If the project is ambiguous, show the candidates from `.harness/index.md` and ask the user which one to resume.
