# Codex Gates

Codex gates are review checkpoints. They are not default execution.

## Plan Gate

Run after Superpowers writing-plans and before execution when:

- plan is medium/high risk
- work crosses modules
- architecture direction is involved
- database/schema/migration is involved
- security, permission, or user data is involved
- the plan has unclear ownership or boundaries

Save output to:

```text
.harness/projects/<active>/reviews/codex-plan-review.md
```

If critical or important issues are found, revise the plan first.

## Final Gate

Run after implementation and verification, before handoff, when:

- there is meaningful code diff
- public interfaces changed
- data models changed
- core logic changed
- tests are weak or missing
- user requested final review

Save output to:

```text
.harness/projects/<active>/reviews/codex-final-review.md
```

Use the review to decide whether more implementation is required.
