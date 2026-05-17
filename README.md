# Harness Claude Plugin

Harness is a Claude Code plugin that wraps Superpowers with project-local memory, resumable workspaces, and Codex review gates.

## Install For Local Testing

From this repository:

```bash
claude --plugin-dir /Users/huangaokai/Documents/code/agent-study/harness/claude-plugin
```

Or validate the plugin:

```bash
claude plugin validate /Users/huangaokai/Documents/code/agent-study/harness/claude-plugin
```

## Commands

- `/harness <goal>`: create or resume a Harness project and start the wrapped workflow.
- `/harness-status`: show active project status.
- `/harness-resume [query]`: resume the active or matching project.
- `/harness-review-plan`: run the plan review gate.
- `/harness-review-final`: run the final review gate.

## Project State

Harness writes state into the current repository:

```text
.harness/
  config.yaml
  active-project
  index.md
  context/
  projects/
```

The `.harness/projects/project-*` directory is a goal workspace. It can span multiple Claude sessions.

## MVP Limits

This version does not yet implement full PostToolUse parsing, automatic Codex invocation, a MiniMax executor, or a model proxy. It establishes the plugin shape and the project-local state protocol first.
