# Harness Constraints

- Claude Code is the primary workbench.
- Superpowers remains the engineering workflow backbone.
- Harness must be project-local and resumable.
- Project memory lives in `.harness/context/`.
- Codex is a review gate, not the default executor.
- MiniMax is not used for deep analysis in MVP.
- Hooks should help record state, but must not become a hidden heavy automation layer.
- Do not store secrets in `.harness/`.
