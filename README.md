# Harness Claude Plugin

Harness 是一个 Claude Code 插件，用 hooks 做无感项目记忆增强，并保留可选的 Superpowers / Codex review gate 工作流。

## 通过 Claude Code Marketplace UI 安装

在 Claude Code 里打开 `/plugins`，选择 **Add Marketplace**，输入：

```text
huaka1/harness-claude-plugin
```

或者：

```text
https://github.com/huaka1/harness-claude-plugin
```

然后从这个 marketplace 里安装 `harness` 插件。

对应 CLI 命令：

```bash
claude plugin marketplace add huaka1/harness-claude-plugin
claude plugin install harness@harness
```

如果之前已经安装过旧版本，而 Claude Code 一直使用缓存里的旧插件，请重装：

```bash
claude plugin marketplace update harness
claude plugin uninstall harness --scope user -y
claude plugin install harness@harness --scope user
```

## 通过 Git Clone 本地加载

Claude Code 也可以直接从本地插件目录加载：

```bash
git clone https://github.com/huaka1/harness-claude-plugin.git ~/.claude/plugins/harness-claude-plugin
claude --plugin-dir ~/.claude/plugins/harness-claude-plugin
```

## 本地开发测试

在当前仓库里运行：

```bash
claude --plugin-dir /Users/huangaokai/Documents/code/agent-study/harness/claude-plugin
```

校验插件：

```bash
claude plugin validate /Users/huangaokai/Documents/code/agent-study/harness/claude-plugin
```

## 命令

- `/harness <goal>`: 查看或创建当前仓库的 Harness 全局记忆/可选 workflow project。
- `/harness-status`: 查看当前仓库的 Harness memory root 和状态。
- `/harness-resume [query]`: 恢复 active 或匹配的 project。
- `/harness-review-plan`: 运行计划评审关卡。
- `/harness-review-final`: 运行最终评审关卡。

## 全局记忆

Harness 默认不会在当前代码仓库里创建 `.harness/`。它写入全局目录：

```text
~/.harness/projects/<repo-id>/
  config.yaml
  repo.json
  state.json
  events/
    user-prompts.jsonl
    tool-uses.jsonl
    tool-failures.jsonl
    file-changes.jsonl
    session-events.jsonl
  context/
    facts.md
    architecture.md
    commands.md
    constraints.md
    decisions.md
    pitfalls.md
    links.md
    glossary.md
  active-project
  index.md
  projects/
```

Claude Code 启动时，`SessionStart` hook 会读取 `context/` 并注入 `<harness-memory>`。事件先进入 `events/*.jsonl`，后续由后台 compactor 压缩成长期记忆。

## 专家模板

`references/experts/` 提供中文专家模板，用来在计划阶段补充产品、架构、后端、前端、AI、数据、安全、测试、DevOps、API 和现实验收视角。

专家模板参考并改写自 [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)，不是整库复制。使用时先看 `references/experts/registry.md`，只选择当前任务最相关的 2-4 个专家。

## MVP 限制

当前版本已经实现全局事件记录和 SessionStart 记忆注入，但还没有实现后台 MiniMax/便宜模型 compactor、自动 Codex 调用或模型 proxy。
