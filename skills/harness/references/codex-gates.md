# Codex Gate

Codex gate 是评审检查点，不是默认执行路径。

## Plan Gate

在 Superpowers `writing-plans` 之后、执行之前触发。

Plan Gate 是设计/计划 review，不是代码 review。必须用 `codex exec`，固定使用 `gpt-5.5` 和 high reasoning：

```bash
codex exec \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="high"' \
  -s read-only \
  --skip-git-repo-check \
  --ephemeral \
  -o .harness/projects/<active>/reviews/codex-plan-review.md \
  -
```

触发条件：

- 计划是中高风险。
- 跨模块改动。
- 涉及架构方向。
- 涉及数据库、schema、迁移。
- 涉及安全、权限、用户数据。
- 计划的任务边界或 ownership 不清楚。

输出保存到：

```text
.harness/projects/<active>/reviews/codex-plan-review.md
```

如果发现 critical 或 important 问题，先修计划，再执行。

## Final Gate

在实现和验证之后、交接之前触发。

Final Gate 是最终代码 review。代码已经实现并完成基本验证后，必须用 `codex exec review --uncommitted`，固定使用 `gpt-5.5` 和 high reasoning：

```bash
codex exec review \
  --uncommitted \
  -m gpt-5.5 \
  -c 'model_reasoning_effort="high"' \
  --ephemeral \
  -o .harness/projects/<active>/reviews/codex-final-review.md \
  -
```

触发条件：

- 有实质代码 diff。
- 公共接口变化。
- 数据模型变化。
- 核心逻辑变化。
- 测试弱或缺失。
- 用户要求最终 review。

输出保存到：

```text
.harness/projects/<active>/reviews/codex-final-review.md
```

根据 review 结果判断是否需要继续修。

## 命令选择规则

- 审设计、审计划、审任务粒度：用 `codex exec`。
- 审最终代码 diff：用 `codex exec review --uncommitted`。
- 不要用普通 `codex review`，因为它不方便指定 model、reasoning 和输出文件。
- 不要让 Claude 自己冒充 Codex 审核；必须实际执行 Codex CLI。
