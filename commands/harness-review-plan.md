---
description: "对当前 Harness plan 运行 Codex 计划评审关卡"
---

使用 `harness` skill，并检查当前 active project。

评审输入：

- `.harness/projects/<active>/goal.md`
- `.harness/projects/<active>/planning/spec.md`
- `.harness/projects/<active>/planning/plan.md`
- `.harness/projects/<active>/planning/plan.json`
- 相关 `.harness/context/*.md`

当计划是中高风险、跨模块、架构敏感、安全敏感、数据敏感或边界模糊时，请让 Codex 审查计划。结果保存到：

```text
.harness/projects/<active>/reviews/codex-plan-review.md
```

如果 Codex 指出 critical 或 important 问题，先修正计划，再执行。
