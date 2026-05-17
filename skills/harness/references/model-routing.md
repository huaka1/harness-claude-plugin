# 模型路由

当前默认分工：

```text
claude-main  = Claude Code 里的 DeepSeek Pro
claude-cheap = Claude Code 里的 DeepSeek Flash
codex-gate   = Codex / GPT-5.5 / high reasoning review gate
hermes       = 可选的背景调研或记忆辅助
minimax      = 备用
```

规则：

- `claude-main`: 普通代码、调试、架构、跨文件理解。
- `claude-cheap`: 低风险、机械、输入明确、输出格式明确的小任务。
- `codex-gate`: 只做计划评审和最终代码评审，不作为默认执行器。固定使用 `gpt-5.5` + `model_reasoning_effort="high"`。
- `hermes`: 只有当它的记忆/调研 profile 明确有帮助时才使用。
- `minimax`: 不用于深度代码库分析或模糊规划。先作为 fallback 保留。

MVP 阶段不要引入 proxy 层。DeepSeek Pro/Flash 已经能覆盖主模型和便宜模型的基础分层。
