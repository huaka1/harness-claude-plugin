---
name: harness
description: Use when the user invokes /harness, asks to run a project-local chained workflow, wants Claude Code to wrap Superpowers with memory/review gates, or wants work to be resumable through .harness files.
---

# Harness

Harness is a project-local workflow layer around Superpowers.

Use it to:

- start or resume a project workspace in `.harness/projects/`
- inject project memory from `.harness/context/`
- keep handoff/status/next-actions current
- place Codex review gates around medium/high-risk plans and final diffs
- record links, pitfalls, constraints, and decisions that should prevent repeated mistakes

Do not use Harness as a replacement for Superpowers. Harness wraps Superpowers.

## Required Flow

1. Establish or resume the active Harness project with `harness_state.py`.
2. Read the active project files before substantial work.
3. Use Superpowers for the engineering workflow:
   - `superpowers:brainstorming` before creative/design/behavior changes.
   - `superpowers:writing-plans` before multi-step implementation.
   - `superpowers:executing-plans` or `superpowers:subagent-driven-development` for execution when appropriate.
4. Insert Harness gates:
   - plan gate before executing medium/high-risk plans.
   - final gate before saying medium/high-risk work is ready.
5. Before stopping, update:
   - `.harness/projects/<active>/status.md`
   - `.harness/projects/<active>/next-actions.md`
   - `.harness/projects/<active>/handoff.md`
6. When new durable knowledge appears, update project memory:
   - `.harness/context/links.md`
   - `.harness/context/pitfalls.md`
   - `.harness/context/decisions.md`
   - `.harness/context/constraints.md`
   - `.harness/context/commands.md`

## Mode Classification

Classify the active task early:

- `research`: gather evidence, compare options, produce recommendation.
- `implementation`: modify code or configuration.
- `debug`: investigate a failure and fix root cause.
- `review`: inspect existing changes or plans.
- `migration`: schema/storage/platform transition.
- `operation`: deployment, cron, production, credentials, or environment work.
- `mixed`: multiple modes.

Use `mixed` when unsure.

## Memory Rules

Prefer stable, compact project memory over large transcripts.

Save:

- durable facts about the codebase or business
- accepted and rejected decisions
- commands that are known to work
- pitfalls that caused failed attempts
- links the user provided as authoritative sources

Do not save:

- full logs unless they are short and diagnostic
- sensitive secrets
- large docs copied from the web
- speculative facts that were not verified

For links, save the URL, why it matters, when to use it, and keywords that should trigger re-checking it. Do not freeze long external content into memory when the link should be checked for current docs.

## Review Gates

Use Codex as a reviewer, not as the default executor.

Plan gate applies to:

- architecture direction
- cross-module changes
- database/schema/migration work
- security, permission, or user data handling
- unclear task boundaries
- medium/high-risk execution plans

Final gate applies to:

- meaningful code diff
- public API or data model changes
- core logic changes
- weak verification
- user-requested review

## References

Read only the relevant reference file:

- `references/workflow.md` for the chained workflow.
- `references/project-memory.md` for `.harness/context` rules.
- `references/model-routing.md` for DeepSeek/Codex/MiniMax roles.
- `references/codex-gates.md` for plan/final review gates.
- `references/superpowers-integration.md` for how Harness wraps Superpowers.
- `references/project-files.md` for file layout and semantics.
