# 项目记忆

`~/.harness/projects/<repo-id>/context/` 是长期项目记忆。对工程工作来说，项目维度记忆通常比跨项目个人记忆更重要。

它用来避免反复调研、反复踩同一个坑。

Harness 默认不在当前仓库创建 `.harness/`。项目内 `.harness/` 只应该作为显式导出/共享能力出现。

## 文件说明

- `facts.md`: 已验证的长期事实。
- `architecture.md`: 当前架构和重要耦合点。
- `commands.md`: 已知可用命令，必要时写清 cwd/env。
- `constraints.md`: 项目约束和用户偏好。
- `decisions.md`: 已接受/已拒绝的决策和理由。
- `pitfalls.md`: 失败模式和修正方式。
- `links.md`: 权威链接，以及什么时候必须重新打开。
- `glossary.md`: 项目术语。
- `lessons/`: 当一个坑太长，无法放进 `pitfalls.md` 时写成独立 lesson。

## 原始事件

hooks 会先把原始事件写入：

```text
~/.harness/projects/<repo-id>/events/
  user-prompts.jsonl
  tool-uses.jsonl
  tool-failures.jsonl
  file-changes.jsonl
  session-events.jsonl
```

这些不是最终记忆。后续 compactor 会从事件中提炼稳定事实、命令、坑、决策、约束和链接。

## 链接记录模板

```text
## <主题>

- URL: <url>
- Why: <为什么这个来源重要>
- Applies to: <关键词>
- Last checked: YYYY-MM-DD
- Rule: <未来遇到什么情况必须重新打开这个链接>
```

当信息会变化时，优先保存链接和适用场景，不要复制一大段外部内容。
