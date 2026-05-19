---
description: "查看或启动当前仓库的 Harness 全局记忆/增强工作流"
argument-hint: "<目标或继续请求>"
---

使用 `harness` skill 处理这个请求。

用户输入：

```text
$ARGUMENTS
```

流程：

1. 先运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" start --cwd "$PWD" --goal "$ARGUMENTS"
```

2. 读取命令输出，把它当成本次会话的权威 Harness memory root。
3. 默认不要在当前仓库创建 `.harness/`；Harness 记忆存放在 `~/.harness/projects/<repo-id>/`。
4. 如果只是普通工作，继续按 Claude Code / Superpowers 正常流程执行。
5. 中高风险计划执行前，可以运行 `/harness-review-plan`。
6. 中高风险代码完成后，可以运行 `/harness-review-final`。

不要把 Harness 当成 Superpowers 的替代品。Harness 的默认职责是无感记录事件、注入项目记忆和提供 review gate。
