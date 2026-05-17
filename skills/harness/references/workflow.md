# Harness 工作流

Harness 是一个围绕 Superpowers 的小状态机：

```text
/harness <目标>
  -> 创建或恢复 .harness project
  -> 加载相关项目记忆
  -> Superpowers brainstorming
  -> Superpowers writing-plans
  -> 风险足够高时进入 Harness Codex plan gate
  -> Superpowers execution
  -> 风险足够高时进入 Harness Codex final gate
  -> Harness learn + handoff
  -> 用户自己处理 finish
```

用户经常会自己决定 branch finish、merge、PR、cleanup。因此 Harness 必须在 finish 之前写好 learnings 和 handoff，而不是等分支收尾之后再记。

## 恢复任务

恢复任务时优先读取：

```text
.harness/active-project
.harness/projects/<active>/handoff.md
.harness/projects/<active>/status.md
.harness/projects/<active>/next-actions.md
```

如果这些文件已经能回答“当前做到哪里、下一步是什么”，不要从零扫描项目。
