---
description: "Run a Codex-oriented review gate for the current Harness plan"
---

Use the `harness` skill and inspect the active project.

Review inputs:

- `.harness/projects/<active>/goal.md`
- `.harness/projects/<active>/planning/spec.md`
- `.harness/projects/<active>/planning/plan.md`
- `.harness/projects/<active>/planning/plan.json`
- relevant `.harness/context/*.md`

Ask Codex to review the plan when the plan is medium/high risk, cross-module, architecture-sensitive, security-sensitive, data-sensitive, or ambiguous. Save the result to:

```text
.harness/projects/<active>/reviews/codex-plan-review.md
```

If Codex finds critical or important issues, revise the plan before execution.
