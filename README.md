# Harness Claude Plugin

Harness 是一个 Claude Code 插件，用来包住 Superpowers，并补上项目本地记忆、可恢复工作区和 Codex review gate。

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

- `/harness <goal>`: 创建或恢复 Harness project，并启动包装 Superpowers 的工作流。
- `/harness-status`: 查看 active project 状态。
- `/harness-resume [query]`: 恢复 active 或匹配的 project。
- `/harness-review-plan`: 运行计划评审关卡。
- `/harness-review-final`: 运行最终评审关卡。

## 项目状态

Harness 会在当前代码仓库里写入：

```text
.harness/
  config.yaml
  active-project
  index.md
  context/
  projects/
```

`.harness/projects/project-*` 是目标工作区。它可以跨多个 Claude Code 会话延续。

## MVP 限制

当前版本还没有实现完整的 PostToolUse 解析、自动 Codex 调用、MiniMax executor 或模型 proxy。第一阶段先固定插件形态和项目本地状态协议。
