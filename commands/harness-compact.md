---
description: "压缩当前仓库的 Harness 原始事件到长期项目记忆"
argument-hint: "[auto|mmx|rules|dry-run]"
---

使用 `harness` skill，然后运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi

mode="${ARGUMENTS:-auto}"
case "$mode" in
  mmx)
    python3 "$state_script" compact --cwd "$PWD" --engine mmx
    ;;
  rules)
    python3 "$state_script" compact --cwd "$PWD" --engine rules
    ;;
  dry-run)
    python3 "$state_script" compact --cwd "$PWD" --engine auto --dry-run
    ;;
  *)
    python3 "$state_script" compact --cwd "$PWD" --engine auto
    ;;
esac
```

`auto` 会优先使用 `mmx-cli` 的 `mmx text chat`，失败时降级到规则压缩。压缩结果写入当前仓库对应的 `~/.harness/projects/<repo-id>/context/*.md`。
