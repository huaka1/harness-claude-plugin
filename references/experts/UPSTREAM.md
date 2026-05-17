# 上游专家库来源

本目录的专家模板参考并改写自：

- Repository: https://github.com/msitarzewski/agency-agents
- License: MIT License
- Copyright: 2025 AgentLand Contributors

## 使用方式

Harness 没有把 `agency-agents` 整库复制进来，而是选择了和项目工作流最相关的专家角色，改写成中文的计划增强模板。

当前重点吸收的上游角色：

- Software Architect
- Minimal Change Engineer
- Code Reviewer
- AI Engineer
- Backend Architect
- Frontend Developer
- Security Engineer
- DevOps Automator
- Data Engineer
- Product Manager
- Reality Checker
- API Tester

## 维护规则

- 新增专家时，先确认它是否会被 Harness 高频使用。
- 专家模板要服务于计划增强、验收和 review gate，不要写成人设表演。
- 不要直接粘贴长篇上游正文；用中文压缩成可执行检查点。
- 如果某个专家只是一次性需要，放在当前项目 `.harness/context/`，不要进插件。
