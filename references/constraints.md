# Harness 约束

- Claude Code 是默认工作台。
- Superpowers 是工程流程骨架。
- Harness 必须是项目本地、可恢复的。
- 项目记忆放在 `.harness/context/`。
- Codex 是 review gate，不是默认 executor。
- MVP 阶段不把 MiniMax 用于深度分析。
- Hooks 用来辅助记录状态，但不能变成隐藏的重型自动化层。
- 不要把 secrets 写入 `.harness/`。
