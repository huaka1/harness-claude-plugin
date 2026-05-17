---
description: "Run a Codex-oriented final review gate for the active Harness project"
---

Use the `harness` skill and inspect the active project.

Review inputs:

- `.harness/projects/<active>/goal.md`
- `.harness/projects/<active>/planning/plan.md`
- `.harness/projects/<active>/implementation/changes.md`
- `.harness/projects/<active>/implementation/verification.md`
- `git diff`
- relevant `.harness/context/*.md`

Ask Codex to review the final work when there is meaningful code diff, public API change, schema change, security/user-data risk, core logic change, or weak verification. Save the result to:

```text
.harness/projects/<active>/reviews/codex-final-review.md
```

If Codex finds critical or important issues, address them before declaring the work ready.
