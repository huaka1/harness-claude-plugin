# 项目文件

每个代码仓库可以有自己的：

```text
~/.harness/projects/<repo-id>/
  config.yaml
  active-project
  index.md
  repo.json
  state.json
  events/
  context/
  projects/
```

Harness 默认使用全局目录，不在当前仓库创建 `.harness/`。

## Project Workspace

`project-YYYYMMDD-HHMMSS` 是一个目标工作区，不是 Claude session，也不是 git branch。它可以跨多个 Claude Code 会话延续。

文件说明：

- `goal.md`: 用户目标和范围。
- `mode.md`: research、implementation、debug、review、migration、operation 或 mixed。
- `status.md`: 当前状态。
- `next-actions.md`: 下一步行动。
- `handoff.md`: 紧凑恢复上下文。
- `transcript.md`: 精简过程日志。
- `research/*`: 调研产物。
- `planning/spec.md`: 已接受的 spec。
- `planning/plan.md`: 实现计划。
- `planning/plan.json`: 需要结构化路由时使用。
- `implementation/changes.md`: 改了什么。
- `implementation/verification.md`: 跑了哪些验证，结果如何。
- `reviews/*`: Codex review 输出。

这些文件要短而有用。它们的目的不是保存完整聊天记录，而是帮助恢复任务和沉淀经验。
