# Seed Memory

## Accepted Direction

Harness is a Claude Code plugin that wraps Superpowers.

## Rejected Directions

- Hermes-first as default Harness controller.
- Old Python REPL as daily entry.
- Forking Superpowers before wrapper MVP proves useful.
- Routing deep codebase analysis to MiniMax.

## Current Model Setup

- Claude Code main model: DeepSeek Pro.
- Claude Code cheap model: DeepSeek Flash.
- Codex review gate: GPT-5.5.
- Hermes: optional memory/research helper.
- MiniMax: fallback only.
