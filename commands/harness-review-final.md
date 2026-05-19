---
description: "用 Codex/GPT-5.5 high 对 active Harness project 做最终代码评审"
---

使用 `harness` skill，并检查当前 active project。

这个命令用于代码已经实现并完成基本验证之后的最终代码 review。

注意：Superpowers 可能已经在执行过程中产生 commit，所以不能固定只审 `--uncommitted`。Final Review 应该优先和主分支/base branch 做整体 diff review。

如果用户没有明确说 base branch，先尝试自动识别；识别不到时，必须问用户主分支是什么。

运行：

```bash
state_script="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces" -path "*/scripts/harness_state.py" -print 2>/dev/null | sort | tail -n 1)"
if [ -z "$state_script" ] || [ ! -f "$state_script" ]; then
  echo "找不到 Harness state script。请重装：claude plugin uninstall harness --scope user -y && claude plugin install harness@harness --scope user"
  exit 1
fi
root="$(python3 "$state_script" root --cwd "$PWD")"
active="$(cat "$root/active-project" 2>/dev/null || true)"
if [ -z "$active" ]; then
  echo "当前仓库没有 active Harness workflow project。final review 仍可做，但缺少 Harness plan/change 上下文；请先运行 /harness <目标> 或明确要求只按 git diff review。"
  exit 1
fi
project="$root/projects/$active"
out="$project/reviews/codex-final-review.md"
mkdir -p "$project/reviews"

base_branch="${HARNESS_BASE_BRANCH:-}"
if [ -z "$base_branch" ]; then
  for candidate in origin/main origin/master main master; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then
      base_branch="$candidate"
      break
    fi
  done
fi
if [ -z "$base_branch" ]; then
  echo "无法自动识别 base branch。请先问用户主分支是什么，然后设置：HARNESS_BASE_BRANCH=<branch> /harness-review-final"
  exit 1
fi

codex exec review \
  --base "$base_branch" \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="high"' \
  --ephemeral \
  -o "$out" \
  - <<PROMPT
请用中文对当前分支相对 base branch 的全部变更做最终代码 review。

这是 Harness 的 final gate。目标不是重新设计方案，而是检查已经完成的代码是否可以交接。

Base branch: $base_branch

请结合以下 Harness 上下文审查：

- goal: $project/goal.md
- accepted plan: $project/planning/plan.md
- changes: $project/implementation/changes.md
- verification: $project/implementation/verification.md
- known constraints/pitfalls: $root/context/

重点检查：
1. 是否偏离 goal 或 accepted plan
2. 是否引入明显 bug、回归或边界条件问题
3. 是否有安全、权限、数据损坏、迁移或兼容性风险
4. 验证是否足够，是否缺少关键测试
5. 是否有必须在 handoff 前处理的问题

输出格式：
1. 结论：approve / revise / block
2. Critical 问题
3. Important 问题
4. 建议补充的验证
5. 可以写入 handoff 的剩余风险
PROMPT

echo "Codex final code review saved to $out"
echo "Base branch: $base_branch"
```

如果 Codex 给出 `block` 或 Critical 问题，先处理这些问题，再声明工作 ready。
