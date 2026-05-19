---
description: "恢复当前仓库的 active Harness workflow project"
argument-hint: "[可选 project id 或主题]"
---

使用 `harness` skill，然后运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" resume --cwd "$PWD" --query "$ARGUMENTS"
```

从返回的 memory root 和 workflow project 继续。如果 project 不明确，展示 `~/.harness/projects/<repo-id>/index.md` 里的候选项，让用户选择恢复哪一个。
