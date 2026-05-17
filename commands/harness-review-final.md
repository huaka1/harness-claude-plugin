---
description: "对 active Harness project 运行 Codex 最终评审关卡"
---

使用 `harness` skill，并检查当前 active project。

评审输入：

- `.harness/projects/<active>/goal.md`
- `.harness/projects/<active>/planning/plan.md`
- `.harness/projects/<active>/implementation/changes.md`
- `.harness/projects/<active>/implementation/verification.md`
- `git diff`
- 相关 `.harness/context/*.md`

当存在实质代码 diff、公共 API 变化、schema 变化、安全/用户数据风险、核心逻辑变化或验证不足时，请让 Codex 审查最终结果。结果保存到：

```text
.harness/projects/<active>/reviews/codex-final-review.md
```

如果 Codex 指出 critical 或 important 问题，先处理这些问题，再声明工作 ready。
