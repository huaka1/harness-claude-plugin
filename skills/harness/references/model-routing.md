# Model Routing

Current default routing:

```text
claude-main  = DeepSeek Pro through Claude Code
claude-cheap = DeepSeek Flash through Claude Code
codex-gate   = Codex / GPT-5.5 review gate
hermes       = optional background research or memory helper
minimax      = backup only
```

Rules:

- Use `claude-main` for normal coding, debugging, architecture, and cross-file understanding.
- Use `claude-cheap` for low-risk, mechanical, explicit tasks when Claude Code can route them cheaply.
- Use `codex-gate` for plan/final review, not for default execution.
- Use `hermes` only when its memory/research profile adds clear value.
- Do not use MiniMax for deep codebase analysis or ambiguous planning. Keep it as fallback until there is a reliable executor path.

Do not add a proxy layer until a concrete routing failure requires it. DeepSeek Pro/Flash already covers the main/cheap split for MVP.
