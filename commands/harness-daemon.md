---
description: "安装、查看或运行 Harness 后台定时压缩任务"
argument-hint: "[install|uninstall|status|run-once]"
---

使用 `harness` skill，然后运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi

action="${ARGUMENTS:-status}"
case "$action" in
  install)
    python3 "$state_script" daemon install --interval 300 --engine auto
    ;;
  uninstall)
    python3 "$state_script" daemon uninstall
    ;;
  run-once)
    python3 "$state_script" daemon run-once --engine auto --if-needed
    ;;
  status|*)
    python3 "$state_script" daemon status
    ;;
esac
```

`install` 会创建用户级 macOS LaunchAgent：`~/Library/LaunchAgents/com.huaka1.harness.compactor.plist`。它每 5 分钟运行一次，只压缩 `needs_compaction=true` 的项目。
