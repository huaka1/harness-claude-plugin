# Harness Workflow

Harness runs a small state machine around Superpowers:

```text
/harness <goal>
  -> create/resume .harness project
  -> load relevant project memory
  -> Superpowers brainstorming
  -> Superpowers writing-plans
  -> Harness Codex plan gate when risk warrants it
  -> Superpowers execution
  -> Harness Codex final gate when risk warrants it
  -> Harness learn + handoff
  -> user-managed finish
```

The user often handles branch finish, merge, PR, or cleanup personally. Therefore Harness must write learnings and handoff before finishing, not after branch completion.

## Resume

Resume from:

```text
.harness/active-project
.harness/projects/<active>/handoff.md
.harness/projects/<active>/status.md
.harness/projects/<active>/next-actions.md
```

Do not rebuild context from scratch when these files already answer the question.
