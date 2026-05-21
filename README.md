# Harness Claude Plugin

Harness 是一个 Claude Code 插件，用来给每个代码仓库增加一层轻量级项目记忆。

它通过 Claude Code hooks 记录有价值的开发事件，把这些事件压缩成长期 Markdown 记忆，并在后续新会话启动时重新注入给 Claude Code，减少重复读项目、重复踩坑和重复解释背景。

<p align="center">
  <img src="docs/diagrams/harness-overview.svg" alt="Harness 工作原理图" width="860">
</p>

## 为什么需要 Harness？

Claude Code 很擅长阅读代码，但在真实项目里，经常会反复做同样的上下文发现工作：

- 这个项目应该跑哪些命令？
- 哪些架构决策已经讨论过？
- 哪些部署、测试、依赖问题之前踩过坑？
- 用户之前补充过哪些链接、约束和业务背景？

Harness 会把这些重复发现沉淀到 `~/.harness/projects/<repo-id>/context/`，再通过 `SessionStart` hook 在新会话启动时注入给 Claude Code。

## 核心能力

- **全局项目记忆**：默认写入 `~/.harness/projects/<repo-id>/`，不污染当前代码仓库。
- **无感事件记录**：通过 hooks 记录用户提示词、工具调用、工具失败、文件修改和会话事件。
- **启动时注入记忆**：在 Claude Code 启动、清空或 compact 会话时，将 `context/*.md` 注入为 `<harness-memory>`。
- **后台定时压缩**：可选安装 macOS LaunchAgent，把原始事件定期压缩成长期记忆。
- **MiniMax 低成本压缩**：支持通过 `mmx-cli` 调用便宜模型，也支持本地规则降级。
- **Codex 评审关卡**：可选在高风险计划和最终 diff 前后插入 Codex review gate。
- **兼容 Superpowers**：Harness 的定位是包装和增强 Superpowers 这类流程插件，不是替代它们。

## 安装

### 通过 Claude Code Marketplace 安装

在 Claude Code 中打开 `/plugins`，选择 **Add Marketplace**，输入：

```text
huaka1/harness-claude-plugin
```

然后从这个 marketplace 中安装 `harness` 插件。

等价 CLI 命令：

```bash
claude plugin marketplace add huaka1/harness-claude-plugin
claude plugin install harness@harness --scope user
claude plugin enable harness@harness --scope user
```

安装或更新后，重启 Claude Code。

### 更新已有安装

```bash
claude plugin marketplace update harness
claude plugin update harness@harness
claude plugin enable harness@harness --scope user
```

如果 Claude Code 一直使用旧缓存，可以重装：

```bash
claude plugin uninstall harness@harness --scope user -y
claude plugin install harness@harness --scope user
claude plugin enable harness@harness --scope user
```

### 从本地 clone 加载

```bash
git clone https://github.com/huaka1/harness-claude-plugin.git ~/.claude/plugins/harness-claude-plugin
claude --plugin-dir ~/.claude/plugins/harness-claude-plugin
```

`--plugin-dir` 适合本地开发或临时测试。日常使用建议通过 marketplace 安装并启用，这样重启 Claude Code 后仍会自动加载插件。

## 快速开始

1. 安装并启用插件。
2. 在一个 git 仓库目录里打开 Claude Code。
3. 正常提问，或者运行：

```text
/harness-status
```

你应该能看到当前仓库对应的记忆目录：

```text
Harness memory root: ~/.harness/projects/<repo-id>
Repo: /path/to/your/repo
```

验证启动注入是否生效，可以在仓库目录里新开一个 Claude Code 会话，然后问：

```text
不要调用任何工具。你能看到 <harness-memory> 吗？只回答 Memory root 和 Repo root。
```

如果注入成功，Claude 应该能在不读文件的情况下回答出同一个 memory root。

## 工作原理

Harness 有两条链路。

会话内的快速链路：

1. `SessionStart` 读取 `context/*.md`。
2. hook 返回包含 `additionalContext` 的 JSON。
3. Claude Code 收到压缩后的 `<harness-memory>`。
4. 其他 hooks 继续把原始事件追加到 `events/*.jsonl`。

后台的慢速链路：

1. `/harness-compact` 或 `/harness-daemon` 扫描待压缩的原始事件。
2. compactor 提取长期有效的事实、命令、约束、决策、链接和踩坑。
3. 结果写回 `context/*.md`。
4. 下一次新会话会获得更新后的项目记忆。

Harness 默认不会在你的代码仓库里创建 `.harness/`。项目记忆放在全局目录，Claude Code 只接收压缩后的上下文。

## 记忆目录结构

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
  projects/
```

`events/` 保存短期原始观察。`context/` 保存适合注入到未来会话里的长期项目记忆。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `/harness-status` | 查看当前仓库的 memory root 和状态。 |
| `/harness <goal>` | 启动或查看可选的 Harness workflow project。 |
| `/harness-resume [query]` | 恢复匹配的 workflow project。 |
| `/harness-compact [auto|mmx|rules|dry-run]` | 把原始事件压缩进长期记忆。 |
| `/harness-daemon [install|uninstall|status|run-once]` | 管理后台压缩任务。 |
| `/harness-review-plan` | 运行 Codex 计划评审关卡。 |
| `/harness-review-final` | 运行 Codex 最终代码评审关卡。 |

## 后台定时压缩

安装 macOS LaunchAgent：

```text
/harness-daemon install
```

它会创建：

```text
~/Library/LaunchAgents/com.huaka1.harness.compactor.plist
~/.harness/logs/compactor.out.log
~/.harness/logs/compactor.err.log
```

后台任务会定期扫描 `~/.harness/projects/*/state.json`，只处理标记为需要压缩的仓库。

常用操作：

```text
/harness-daemon status
/harness-daemon run-once
/harness-daemon uninstall
```

## 可选 MiniMax 压缩

Harness 可以通过 `mmx-cli` 使用低成本模型做记忆压缩：

```bash
mmx auth status
/harness-compact mmx
```

默认模式是：

```text
/harness-compact auto
```

`auto` 会优先使用 MiniMax；不可用时降级为本地规则。

## Codex Review Gates

Harness 提供两个可选评审关卡：

- `/harness-review-plan`：在高风险实现前，让 Codex 审计划。
- `/harness-review-final`：在完成后，让 Codex 审最终 diff，推荐和 base branch 对比。

这些关卡是显式触发的。Harness 不会在你没有要求时自动消耗昂贵的评审模型调用。

## 安全说明

Harness 用来保存长期项目上下文，不是 secrets 存储。

不要主动把 API key、密码、token、私有凭据或客户数据写入 `context/*.md`。原始事件记录也应该尽量避免保留完整文件内容；能记录路径和摘要时，不要记录全文。

共享 `~/.harness` 日志或记忆文件之前，请先检查敏感信息。

## 本地开发

校验插件：

```bash
claude plugin validate /path/to/harness-claude-plugin
```

用本地 checkout 启动 Claude Code：

```bash
claude --plugin-dir /path/to/harness-claude-plugin
```

查看安装状态：

```bash
claude plugin list
claude plugin details harness@harness
```

## License

MIT
