---
description: "Start or continue a Harness project workflow around Superpowers"
argument-hint: "<goal or continue request>"
---

Use the `harness` skill for this request.

User input:

```text
$ARGUMENTS
```

Workflow:

1. Run:

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "Harness state script not found. Reinstall with: claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" start --cwd "$PWD" --goal "$ARGUMENTS"
```

2. Read the command output and treat it as the authoritative Harness project state for this session.
3. If the output says an active project was resumed, continue from `handoff.md`, `status.md`, and `next-actions.md`.
4. If a new project was created, classify the task mode and start with `superpowers:brainstorming` when the request involves design, implementation, or behavior changes.
5. After brainstorming, use `superpowers:writing-plans` for multi-step implementation work.
6. Before execution of medium/high-risk plans, run `/harness-review-plan`.
7. During execution, prefer Superpowers' `executing-plans` or `subagent-driven-development` workflow.
8. Before final handoff of medium/high-risk work, run `/harness-review-final`.
9. Keep `.harness/projects/<project>/handoff.md`, `status.md`, and `next-actions.md` current before stopping.

Do not treat Harness as a replacement for Superpowers. Harness provides project memory, routing, review gates, and handoff discipline around Superpowers.
