---
description: "用 Codex/GPT-5.5 high 对 active Harness project 做最终代码评审"
---

使用 `harness` skill，并检查当前 active project。

这个命令用于代码已经实现并完成基本验证之后的最终代码 review。这里应该用 `codex exec review --uncommitted`，不是普通 `codex exec`。

运行：

```bash
active="$(cat .harness/active-project)"
project=".harness/projects/$active"
out="$project/reviews/codex-final-review.md"
mkdir -p "$project/reviews"

codex exec review \
  --uncommitted \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="high"' \
  --ephemeral \
  -o "$out" \
  - <<PROMPT
请用中文对当前未提交代码变更做最终代码 review。

这是 Harness 的 final gate。目标不是重新设计方案，而是检查已经完成的代码是否可以交接。

请结合以下 Harness 上下文审查：

- goal: $project/goal.md
- accepted plan: $project/planning/plan.md
- changes: $project/implementation/changes.md
- verification: $project/implementation/verification.md
- known constraints/pitfalls: .harness/context/

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
```

如果 Codex 给出 `block` 或 Critical 问题，先处理这些问题，再声明工作 ready。
