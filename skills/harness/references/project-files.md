# Project Files

Each repository may contain:

```text
.harness/
  config.yaml
  active-project
  index.md
  context/
  projects/
```

## Project Workspace

`project-YYYYMMDD-HHMMSS` is a goal workspace, not a Claude session and not a git branch. It can span multiple Claude sessions.

Files:

- `goal.md`: user goal and scope.
- `mode.md`: research, implementation, debug, review, migration, operation, or mixed.
- `status.md`: current state.
- `next-actions.md`: immediate next steps.
- `handoff.md`: compact resume context.
- `transcript.md`: sparse process log.
- `research/*`: research artifacts.
- `planning/spec.md`: accepted spec.
- `planning/plan.md`: implementation plan.
- `planning/plan.json`: structured task routing when needed.
- `implementation/changes.md`: what changed.
- `implementation/verification.md`: tests/checks and results.
- `reviews/*`: Codex review outputs.

Keep these files concise. Their purpose is resumption and learning, not a full chat transcript.
