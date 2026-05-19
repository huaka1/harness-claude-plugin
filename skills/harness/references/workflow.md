# Harness 工作流

Harness 默认是 Claude Code 的无感记忆层：

```text
Claude Code hooks
  -> 写 ~/.harness/projects/<repo-id>/events/*.jsonl
  -> 后台 compactor 压缩到 context/*.md
  -> SessionStart 注入 <harness-memory>
  -> Claude Code 少重复读项目、少重复踩坑
```

可选的 `/harness` 是围绕 Superpowers 的工作流增强：

```text
/harness <目标>
  -> 创建或恢复 ~/.harness/projects/<repo-id>/projects/<project-id>
  -> 加载相关项目记忆
  -> Superpowers brainstorming
  -> Superpowers writing-plans
  -> 风险足够高时进入 Harness Codex plan gate
  -> Superpowers execution
  -> 风险足够高时进入 Harness Codex final gate
  -> Harness learn
  -> 用户自己处理 finish
```

用户经常会自己决定 branch finish、merge、PR、cleanup。因此 Harness 必须在 finish 之前写好 learnings 和 handoff，而不是等分支收尾之后再记。

## 恢复任务

恢复任务时优先读取：

```text
~/.harness/projects/<repo-id>/active-project
~/.harness/projects/<repo-id>/projects/<active>/handoff.md
~/.harness/projects/<repo-id>/projects/<active>/status.md
~/.harness/projects/<repo-id>/projects/<active>/next-actions.md
```

如果这些文件已经能回答“当前做到哪里、下一步是什么”，不要从零扫描项目。
