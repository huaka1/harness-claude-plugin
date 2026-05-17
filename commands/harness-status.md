---
description: "查看当前 active Harness project 和 handoff"
---

运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
python3 "$state_script" status --cwd "$PWD"
```

根据输出总结当前 active project、状态、下一步行动，以及相关项目记忆。除非用户要求，不要扫描完整代码仓库。
