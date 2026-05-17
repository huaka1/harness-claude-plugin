---
name: harness
description: 当用户调用 /harness、想启动项目级链式工作流、想让 Claude Code 包住 Superpowers 并加入项目记忆/review gate、或希望工作能通过 .harness 文件恢复时使用。
---

# Harness

Harness 是一层项目本地工作流。它包在 Superpowers 外面，用来处理项目记忆、恢复上下文、评审关卡和交接记录。

它的用途：

- 在 `.harness/projects/` 中创建或恢复一个项目工作区。
- 从 `.harness/context/` 注入项目记忆。
- 持续维护 `handoff.md`、`status.md`、`next-actions.md`。
- 在中高风险计划和最终 diff 前后插入 Codex review gate。
- 记录链接、踩坑、约束和决策，避免后续重复犯错。

不要把 Harness 当成 Superpowers 的替代品。Harness 的职责是包装 Superpowers，不是复制 Superpowers。

## 必走流程

1. 先用 `harness_state.py` 创建或恢复 active Harness project。
2. 做任何重活之前，先读 active project 的关键文件。
3. 工程流程继续使用 Superpowers：
   - 有创意、设计、功能、行为变化时，先用 `superpowers:brainstorming`。
   - 多步骤实现前，用 `superpowers:writing-plans`。
   - 执行计划时，按情况使用 `superpowers:executing-plans` 或 `superpowers:subagent-driven-development`。
4. 插入 Harness gate：
   - 中高风险计划执行前，走 plan gate。
   - 中高风险工作完成前，走 final gate。
5. 停止工作前，更新：
   - `.harness/projects/<active>/status.md`
   - `.harness/projects/<active>/next-actions.md`
   - `.harness/projects/<active>/handoff.md`
6. 出现新的长期有效信息时，更新项目记忆：
   - `.harness/context/links.md`
   - `.harness/context/pitfalls.md`
   - `.harness/context/decisions.md`
   - `.harness/context/constraints.md`
   - `.harness/context/commands.md`

## 任务模式

尽早判断当前任务属于哪类：

- `research`: 调研、证据整理、方案比较、输出建议。
- `implementation`: 修改代码或配置。
- `debug`: 排查失败、定位根因、修复问题。
- `review`: 审查已有变更、计划或方案。
- `migration`: schema、存储、平台迁移。
- `operation`: 部署、cron、生产环境、凭据、环境问题。
- `mixed`: 多种模式混合。

不确定时使用 `mixed`。

## 记忆规则

优先保存稳定、紧凑、可复用的项目记忆，不要保存大段聊天记录。

应该保存：

- 代码库或业务的长期事实。
- 已接受和已拒绝的决策。
- 已验证可用的命令。
- 导致失败的踩坑模式。
- 用户补充的权威链接。

不要保存：

- 大段日志，除非很短且有诊断价值。
- secrets、token、密码等敏感信息。
- 从网页复制的大段文档。
- 没有验证过的猜测。

对于链接，保存 URL、为什么重要、什么时候该看、哪些关键词会触发重新检查。不要把容易过期的外部文档全文冻结到记忆里；需要时重新打开链接看最新内容。

## Review Gate

Codex 是 reviewer，不是默认 executor。Harness gate 必须实际调用 Codex CLI，不能让 Claude 自己冒充 Codex 审核。

Plan gate 是设计/计划 review，使用：

```bash
codex exec -m gpt-5.5 -c 'model_reasoning_effort="high"'
```

适用于：

- 架构方向。
- 跨模块改动。
- 数据库、schema、迁移。
- 安全、权限、用户数据。
- 任务边界不清。
- 中高风险执行计划。

Final gate 是最终代码 review。优先和主分支/base branch 比较，因为 Superpowers 可能已经在执行过程中 commit：

```bash
codex exec review --base <base-branch> -m gpt-5.5 -c 'model_reasoning_effort="high"'
```

如果 base branch 不明确，先问用户主分支是什么。只有确认没有 commit、只需要审未提交工作区时，才使用 `--uncommitted`。

适用于：

- 有实质代码 diff。
- 公共 API 或数据模型变化。
- 核心逻辑变化。
- 验证不足。
- 用户明确要求 review。

## 参考文件

只读取当前任务真正需要的 reference：

- `references/workflow.md`: 整体链式流程。
- `references/project-memory.md`: `.harness/context` 的记忆规则。
- `references/model-routing.md`: DeepSeek、Codex、MiniMax 的角色分工。
- `references/codex-gates.md`: plan/final review gate。
- `references/superpowers-integration.md`: Harness 如何包住 Superpowers。
- `references/project-files.md`: 文件结构和语义。
- `../../references/experts/registry.md`: 专家模板路由和计划增强材料。
