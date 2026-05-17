# Superpowers 集成方式

Harness 包住 Superpowers，不复制、不 fork Superpowers skills。

映射关系：

- 设计或行为变化：使用 `superpowers:brainstorming`。
- 实现计划：使用 `superpowers:writing-plans`。
- 执行计划：使用 `superpowers:executing-plans` 或 `superpowers:subagent-driven-development`。
- Debug：使用 `superpowers:systematic-debugging`。
- 最终验证：使用 `superpowers:verification-before-completion`。

Harness 额外补充：

- 项目本地记忆。
- `.harness/projects` 工作区。
- Codex plan/final gate。
- hook 提醒和 handoff。
- 长期 lesson、links、pitfalls、decisions。

如果 Superpowers 已经自然往后推进，不要打断它。Harness 只在自然检查点插入 gate：计划生成后、最终完成前。
