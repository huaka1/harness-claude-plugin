---
description: "Resume the active Harness project"
argument-hint: "[optional project id or topic]"
---

Use the `harness` skill, then run:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/harness_state.py" resume --cwd "$PWD" --query "$ARGUMENTS"
```

Continue from the returned `handoff.md`, `status.md`, and `next-actions.md`. If the project is ambiguous, show the candidates from `.harness/index.md` and ask the user which one to resume.
