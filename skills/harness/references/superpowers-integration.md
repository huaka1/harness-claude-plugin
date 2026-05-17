# Superpowers Integration

Harness wraps Superpowers. It should not copy or fork Superpowers skills.

Mapping:

- design or behavior change: use `superpowers:brainstorming`
- implementation plan: use `superpowers:writing-plans`
- plan execution: use `superpowers:executing-plans` or `superpowers:subagent-driven-development`
- debugging: use `superpowers:systematic-debugging`
- final verification: use `superpowers:verification-before-completion`

Harness adds:

- project-local memory
- `.harness/projects` workspace
- Codex plan/final gates
- hook-based handoff reminders
- durable lessons, links, pitfalls, and decisions

If Superpowers wants to proceed automatically, allow it. Insert Harness gates only at natural checkpoints: after plan creation and before final completion.
