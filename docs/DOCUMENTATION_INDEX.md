# 📚 符灵 (Fuling) 文档索引

## 🌐 语言版本

### 英文文档 (English)
- **User Documentation** (`docs/en/user/`)
  - [Getting Started](en/user/GETTING_STARTED.md) - 5分钟上手
  - [Quick Start](en/user/QUICK_START.md) - 快速开始指南
  - [Configuration](en/user/CONFIGURATION.md) - 配置说明
  - [Plugin Guide](en/user/PLUGIN_GUIDE.md) - 插件使用指南

- **Developer Documentation** (`docs/en/developer/`)
  - [Extending Fuling](en/developer/EXTENDING_FULING.md) - 扩展开发指南
  - [API Reference](en/developer/API_REFERENCE.md) - API参考
  - [Improvement Plan](en/developer/IMPROVEMENT_PLAN.md) - 改进计划
  - [Browser Capabilities](en/developer/BROWSER_CAPABILITIES.md) - 浏览器能力

- **Project Documentation** (`docs/en/project/`)
  - [Changelog](en/project/CHANGELOG.md) - 更新日志
  - [Contributing](en/project/CONTRIBUTING.md) - 贡献指南
  - [Code of Conduct](en/project/CODE_OF_CONDUCT.md) - 行为准则
  - [Security](en/project/SECURITY.md) - 安全策略
  - [Troubleshooting](en/project/TROUBLESHOOTING.md) - 故障排除

### 中文文档 (中文)
- **用户文档** (`docs/zh/user/`)
  - [快速开始](zh/user/快速开始.md) - 5分钟上手
  - [配置指南](zh/user/CONFIGURATION.md) - 配置说明
  - [插件指南](zh/user/PLUGIN_GUIDE.md) - 插件使用指南

- **开发者文档** (`docs/zh/developer/`)
  - [扩展指南](zh/developer/扩展指南.md) - 扩展开发指南
  - [实施计划](zh/developer/符灵_实施计划.md) - 开发计划
  - [API参考](zh/developer/API_REFERENCE.md) - API参考

- **项目文档** (`docs/zh/project/`)
  - [更新日志](zh/project/CHANGELOG.md) - 版本历史
  - [贡献指南](zh/project/CONTRIBUTING.md) - 参与贡献
  - [行为准则](zh/project/CODE_OF_CONDUCT.md) - 社区准则
  - [安全策略](zh/project/SECURITY.md) - 安全指南

## 🎯 快速导航

### 新用户
1. **5分钟上手** → [Getting Started](en/user/GETTING_STARTED.md) / [快速开始](zh/user/快速开始.md)
2. **安装配置** → [Quick Start](en/user/QUICK_START.md) / [配置指南](zh/user/CONFIGURATION.md)
3. **核心命令** → 运行 `fl wisdom` 获取帮助

### 开发者
1. **扩展开发** → [Extending Fuling](en/developer/EXTENDING_FULING.md) / [扩展指南](zh/developer/扩展指南.md)
2. **API参考** → [API Reference](en/developer/API_REFERENCE.md) / [API参考](zh/developer/API_REFERENCE.md)
3. **贡献指南** → [Contributing](en/project/CONTRIBUTING.md) / [贡献指南](zh/project/CONTRIBUTING.md)

### 团队协作
1. **团队功能** → 运行 `fl team` 使用团队协作
2. **配置共享** → 使用 `fl config` 导出/导入配置
3. **命令分享** → 使用 `fl team` 分享命令

## 📁 文档结构

```
docs/
├── en/                    # 英文文档
│   ├── user/             # 用户文档
│   │   ├── GETTING_STARTED.md
│   │   ├── QUICK_START.md
│   │   ├── CONFIGURATION.md
│   │   └── PLUGIN_GUIDE.md
│   ├── developer/        # 开发者文档
│   │   ├── EXTENDING_FULING.md
│   │   ├── API_REFERENCE.md
│   │   ├── IMPROVEMENT_PLAN.md
│   │   └── BROWSER_CAPABILITIES.md
│   └── project/          # 项目文档
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       ├── CODE_OF_CONDUCT.md
│       ├── SECURITY.md
│       └── TROUBLESHOOTING.md
├── zh/                    # 中文文档
│   ├── user/             # 用户文档
│   │   ├── 快速开始.md
│   │   ├── CONFIGURATION.md
│   │   └── PLUGIN_GUIDE.md
│   ├── developer/        # 开发者文档
│   │   ├── 扩展指南.md
│   │   ├── 符灵_实施计划.md
│   │   └── API_REFERENCE.md
│   └── project/          # 项目文档
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       ├── CODE_OF_CONDUCT.md
│       └── SECURITY.md
└── DOCUMENTATION_INDEX.md # 本文档
```

## 🚀 功能特性

### 核心功能
- **智能命令解释** - 解释shell命令（本地/AI增强）
- **AI代码生成** - 生成多语言代码
- **交互式聊天** - 与AI对话获取帮助
- **团队协作** - 配置共享、命令分享
- **主题系统** - 4种主题风格
- **多AI支持** - Moonshot、OpenAI、本地回退

### 扩展功能
- **插件系统** - 支持自定义命令和提供商
- **配置管理** - 环境变量、配置文件支持
- **错误处理** - 优雅降级、友好提示
- **使用统计** - API使用情况记录

## 🔧 开发资源

### 代码仓库
- **GitHub**: https://github.com/mai-xiyu/Fu-Ling-CLI
- **问题跟踪**: https://github.com/mai-xiyu/Fu-Ling-CLI/issues
- **讨论区**: https://github.com/mai-xiyu/Fu-Ling-CLI/discussions

### 开发工具
- **Python**: 3.8+
- **Click**: CLI框架
- **PyYAML**: 配置管理
- **Pytest**: 测试框架
- **Black**: 代码格式化

### 构建发布
- **安装**: `pip install -e .`
- **测试**: `pytest tests/`
- **打包**: `python -m build`
- **发布**: `twine upload dist/*`

## 🔄 文档维护

### 更新流程
1. **修改文档** → 更新对应语言版本
2. **同步翻译** → 确保中英文内容一致
3. **更新索引** → 更新本文档的链接
4. **测试验证** → 确保链接有效
5. **提交更改** → 推送到GitHub

### 翻译指南
- **技术术语** → 保持一致性
- **代码示例** → 保持原样
- **文化差异** → 适当本地化
- **定期同步** → 确保内容更新

### 贡献文档
1. Fork 仓库
2. 创建分支
3. 修改文档
4. 提交PR
5. 等待审核

## 📞 支持与反馈

### 获取帮助
- **命令行**: 运行 `fl wisdom` 获取提示
- **文档**: 查看本文档索引
- **社区**: 访问GitHub讨论区
- **问题**: 提交GitHub Issue

### 报告问题
- **文档错误**: 提交Issue或PR
- **功能建议**: 在讨论区提出
- **翻译改进**: 提交翻译PR
- **内容更新**: 直接修改并提交

### 联系方式
- **维护者**: deepseek-chat-v3
- **邮箱**: kawinkhae.101@gmail.com
- **仓库**: https://github.com/mai-xiyu/Fu-Ling-CLI
- **问题反馈**: 通过GitHub Issues或邮箱联系

---

**文档系统已优化，支持多语言、结构清晰、易于维护！** 📚🌐

**开始使用符灵：运行 `fl init` 然后 `fl wisdom` 获取每日提示！** 🚀