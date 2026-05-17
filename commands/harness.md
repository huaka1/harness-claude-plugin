---
description: "启动或继续一个 Harness 项目工作流"
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

2. 读取命令输出，把它当成本次会话的权威 Harness project 状态。
3. 如果输出显示恢复了已有 project，就从 `handoff.md`、`status.md`、`next-actions.md` 继续。
4. 如果创建了新 project，先判断任务模式；涉及设计、实现或行为变化时，使用 `superpowers:brainstorming`。
5. brainstorming 后，如果是多步骤实现，使用 `superpowers:writing-plans`。
6. 中高风险计划执行前，运行 `/harness-review-plan`。
7. 执行阶段优先使用 Superpowers 的 `executing-plans` 或 `subagent-driven-development`。
8. 中高风险工作交接前，运行 `/harness-review-final`。
9. 停止前保持 `.harness/projects/<project>/handoff.md`、`status.md`、`next-actions.md` 更新。

不要把 Harness 当成 Superpowers 的替代品。Harness 只负责在 Superpowers 外围提供项目记忆、模型路由、review gate 和 handoff 纪律。
