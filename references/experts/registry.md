# 专家模板注册表

这些专家模板是 Harness 的计划增强材料，不是默认要启动的独立 agent。

使用方式：

1. 先判断任务模式和风险。
2. 只选 2-4 个最相关专家，不要把整个专家库塞进上下文。
3. 把专家提出的约束、问题、验收点写进计划。
4. 中高风险计划进入 Codex plan gate 前，先完成专家增强。
5. 如果专家意见互相冲突，由主控 Claude Code 做取舍，并写清楚原因。

## 上游来源

本目录的专家模板参考并改写自 `msitarzewski/agency-agents`。详情见 `UPSTREAM.md`。

## 默认专家

- `software-architect.md`: 系统设计、边界、架构取舍、ADR。
- `minimal-change-engineer.md`: 最小变更、范围控制、避免顺手重构。
- `product-manager.md`: 用户目标、成功标准、非目标、分阶段交付。
- `backend.md`: API、存储、worker、数据流、事务。
- `frontend.md`: UI、UX、浏览器验证、状态和响应式。
- `ai-engineer.md`: LLM、agent、memory、tooling、评估和模型路由。
- `data-engineer.md`: schema、pipeline、迁移、回填、索引。
- `devops.md`: 部署、CI、运行时、可观测性、回滚。
- `security.md`: 认证、权限、secrets、用户数据、供应链。
- `testing.md`: 验证策略、测试风险、证据要求。
- `api-tester.md`: API 契约、权限、错误语义、性能和兼容性。
- `code-reviewer.md`: 最终代码评审视角，补充 Codex final gate。
- `reality-checker.md`: 防止虚假完成，要求证据和真实验收。

## 任务到专家的路由

| 任务类型 | 首选专家 | 可选专家 |
| --- | --- | --- |
| 新功能 | `product-manager.md`, `minimal-change-engineer.md` | `frontend.md`, `backend.md`, `testing.md` |
| 架构/云化/多租户 | `software-architect.md`, `backend.md`, `security.md` | `data-engineer.md`, `devops.md` |
| LLM/Agent/记忆 | `ai-engineer.md`, `software-architect.md` | `security.md`, `testing.md` |
| 数据迁移 | `data-engineer.md`, `backend.md` | `devops.md`, `reality-checker.md` |
| 前端体验 | `frontend.md`, `product-manager.md` | `testing.md`, `reality-checker.md` |
| API/平台集成 | `api-tester.md`, `backend.md`, `security.md` | `devops.md` |
| 生产发布 | `devops.md`, `reality-checker.md` | `security.md`, `testing.md` |
| 最终收尾 | `code-reviewer.md`, `reality-checker.md` | `minimal-change-engineer.md` |

## 模型使用建议

- 专家增强由主控 Claude Code 完成，通常不需要额外模型。
- 只有机械化整理、清单改写、格式转换这类低风险任务才交给便宜模型。
- 深度源码理解、模糊架构拆解、跨模块计划不要交给 MiniMax/Flash。
- Codex 只负责 plan gate 和 final gate，不替代专家增强。
