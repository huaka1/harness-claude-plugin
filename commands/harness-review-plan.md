---
description: "用 Codex/GPT-5.5 high 对当前 Harness plan 做设计/计划评审"
---

使用 `harness` skill，并检查当前 active project。

这个命令不是代码 review。它用于在执行前，让 Codex/GPT-5.5 以高推理强度审查设计、计划、边界、风险和验收标准。

运行：

```bash
active="$(cat .harness/active-project)"
project=".harness/projects/$active"
out="$project/reviews/codex-plan-review.md"
mkdir -p "$project/reviews"

{
  echo "# Harness Codex Plan Review Request"
  echo
  echo "你是独立的 GPT-5.5 架构/计划 reviewer。请用中文审查这个计划。"
  echo
  echo "重点检查："
  echo "- 目标是否清楚"
  echo "- 方案是否过度设计或遗漏关键步骤"
  echo "- 任务粒度是否适合执行"
  echo "- 文件/模块边界是否清楚"
  echo "- 验收标准和验证命令是否足够"
  echo "- 是否有安全、数据、迁移、权限或回滚风险"
  echo "- 是否应该先向用户确认某些决策"
  echo
  echo "输出格式："
  echo "1. 结论：approve / revise / block"
  echo "2. Critical 问题"
  echo "3. Important 问题"
  echo "4. 建议修改后的计划要点"
  echo "5. 需要用户确认的问题"
  echo
  for f in \
    "$project/goal.md" \
    "$project/mode.md" \
    "$project/planning/spec.md" \
    "$project/planning/plan.md" \
    "$project/planning/plan.json" \
    ".harness/context/constraints.md" \
    ".harness/context/decisions.md" \
    ".harness/context/pitfalls.md" \
    ".harness/context/links.md"
  do
    echo
    echo "## $f"
    if [ -f "$f" ]; then
      sed -n '1,260p' "$f"
    else
      echo "(missing)"
    fi
  done
} | codex exec \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="high"' \
  -s read-only \
  --skip-git-repo-check \
  --ephemeral \
  -o "$out" \
  -

echo "Codex plan review saved to $out"
```

如果 Codex 给出 `block` 或 Critical 问题，先修正计划，不要进入执行。
