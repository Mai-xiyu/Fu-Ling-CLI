# 更新日志

所有项目的显著更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-02-02

### 新增
- **初始发布**: AI-CLI 智能命令行助手
- **核心CLI框架**: 基于 Click + Rich 的专业命令行界面
- **AI集成系统**: 支持 Moonshot AI (Kimi)、OpenAI、Ollama、本地回退
- **插件系统**: 可扩展的插件架构，支持动态加载
- **性能监控**: 启动时间优化，系统资源监控
- **上下文感知**: 自动识别 Git 状态、目录内容、系统信息

### 功能
- `ai init` - 交互式配置向导
- `ai find` - 自然语言文件搜索
- `ai explain` - 命令解释（AI增强）
- `ai suggest` - 智能命令建议
- `ai grep` - 文件内容搜索
- `ai history` - 历史命令搜索
- `ai learn` - 用户模式学习
- `ai config` - 配置管理
- `ai status` - 系统状态检查
- `ai interactive` - 交互式对话模式
- `ai plugin` - 插件管理命令
- `ai perf` - 性能监控命令

### 技术特性
- 完全离线支持（保护隐私）
- 渐进式增强（有AI用AI，没AI用规则）
- 多模型支持（可配置AI提供商）
- 插件热加载
- 性能优化（启动时间 < 50ms）
- 完整的错误处理系统
- 丰富的终端输出格式化

### 文档
- 完整的快速开始指南
- API 参考文档
- 插件开发指南
- 贡献指南
- 使用示例

### 测试
- 核心功能测试套件
- AI集成测试
- 插件系统测试
- 性能基准测试

## 版本规划

### 即将发布 (0.2.0)
- [ ] 更多 AI 模型支持 (Claude, Gemini, 本地 LLM)
- [ ] 前端工程师功能 (CodePen 动画学习)
- [ ] 后端工程师功能 (Go/Java 代码分析)
- [ ] VS Code 扩展
- [ ] 云同步功能

### 计划中 (0.3.0)
- [ ] 团队协作功能
- [ ] 企业级特性
- [ ] 应用商店（插件市场）
- [ ] API 服务

## 版本说明

### 版本号规则
- `MAJOR` - 不兼容的 API 修改
- `MINOR` - 向后兼容的功能性新增
- `PATCH` - 向后兼容的问题修正

### 升级指南
- 补丁版本：直接升级，无破坏性更改
- 次要版本：检查新功能，通常兼容
- 主要版本：仔细阅读迁移指南

### 弃用策略
- 废弃的功能会在两个次要版本中保留
- 废弃警告会显示在相关命令中
- 迁移指南会提供替代方案

## 贡献者

感谢所有为 AI-CLI 项目做出贡献的人！

### 核心团队
- **xiyu-bot-assistant** - 项目创建者和维护者

### 特别感谢
- **Kimi AI (Moonshot AI)** - 提供强大的 AI 能力
- **Click 和 Rich 社区** - 优秀的 Python CLI 工具
- **所有早期用户** - 宝贵的反馈和建议

## 链接
- [GitHub 仓库](https://github.com/xiyu-bot-assistant/ai-cli)
- [问题追踪](https://github.com/xiyu-bot-assistant/ai-cli/issues)
- [讨论区](https://github.com/xiyu-bot-assistant/ai-cli/discussions)
- [文档](https://github.com/xiyu-bot-assistant/ai-cli/tree/main/docs)

---

**提示**: 查看 `ai --version` 获取当前安装的版本信息。