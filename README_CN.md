# 符灵 (Fú Líng) - 智能命令行助手

<div align="center">

![符灵Logo](docs/images/fuling_logo.png)

**古代符咒之灵 · 现代AI智能**

[English](README.md) | [中文](README_CN.md)

</div>

## 🎯 简介

**符灵** (Fú Líng) 是一个融合古代符咒文化与现代AI技术的智能命令行助手。它将传统的命令行工具与人工智能相结合，为开发者和系统管理员提供更智能、更高效的工作体验。

### ✨ 核心理念

```
符 (Fú) - 古代符咒，代表神秘力量和智慧
灵 (Líng) - 灵魂，智能，代表AI和现代科技

符灵：古代符咒之灵在现代复活，成为智能助手
```

## 🚀 快速开始

### 安装

```bash
# 从源码安装
git clone https://github.com/yourusername/fuling.git
cd fuling
pip install -e .

# 或直接使用（开发中）
python fuling_cli.py --help
```

### 初始化

```bash
# 初始化符灵配置
fl init

# 设置AI提供商API密钥（可选）
export MOONSHOT_API_KEY='your_api_key_here'
```

### 基本使用

```bash
# 解释shell命令
fl explain "ls -la"

# 生成代码
fl generate "python函数计算斐波那契数列" -l python

# 与符灵对话
fl chat

# 查看系统状态
fl power

# 获取今日运势（随机命令建议）
fl fortune
```

## 🔮 核心功能

### 1. 智能命令解释
```bash
fl explain "docker run -d nginx"
# 输出：容器符：从虚空召唤nginx容器灵体并在后台运行
```

### 2. AI代码生成
```bash
fl generate "快速排序算法" -l python -o quicksort.py
fl generate "React按钮组件" -l javascript
fl generate "用户表SQL" -l sql
```

### 3. 交互式聊天
```bash
fl chat
# 进入交互模式，可以：
# - 询问技术问题
# - 请求代码帮助
# - 讨论最佳实践
```

### 4. 系统状态监控
```bash
fl power
# 显示：
# - AI连接状态
# - 系统信息
# - 配置状态
```

### 5. 智慧库
```bash
fl wisdom
# 获取使用建议、最佳实践、命令参考
```

## 🎨 主题系统

符灵支持多种主题，适应不同使用场景：

```bash
# 古风主题（默认）
fl init --theme ancient

# 现代主题
fl init --theme modern

# 暗黑主题
fl init --theme dark

# 明亮主题
fl init --theme light
```

### 主题预览

**古风主题**：
```
    ██▓▓▓▓██
    ▓▓    ▓▓    符灵 v0.1.0
    ▓▓  ██▓▓    智能命令行助手
    ▓▓▓▓██▓▓
    ▓▓  ▓▓▓▓    古代智慧 · 现代AI
    ██▓▓▓▓██
```

**现代主题**：
```
    ╔══════════╗
    ║  符灵    ║
    ║ v0.1.0   ║
    ╚══════════╝
    智能命令行助手
```

## 🔌 AI提供商支持

符灵支持多种AI后端：

### 已支持：
- **Moonshot (Kimi)** - 推荐，中文优化
- **OpenAI** - ChatGPT兼容
- **本地模式** - 离线基础功能

### 配置示例：
```yaml
# ~/.config/fuling/config.yaml
model:
  provider: "moonshot"  # moonshot | openai | local
  name: "kimi-k2-turbo-preview"
  api_key: "${MOONSHOT_API_KEY}"
  temperature: 0.3
  max_tokens: 1000
```

## 📁 项目结构

```
fuling/
├── fuling_cli.py          # 主命令行入口
├── fuling_core.py         # 核心配置管理
├── fuling_ai.py           # AI集成模块
├── fuling_theme.py        # 主题系统
├── config/               # 配置文件
│   └── themes/          # 主题定义
├── docs/                 # 文档
│   ├── README_CN.md     # 中文文档
│   ├── README.md        # 英文文档
│   ├── QUICK_START.md   # 快速开始
│   └── API_REFERENCE.md # API参考
├── examples/             # 使用示例
└── tests/               # 测试文件
```

## 🛠️ 开发指南

### 环境设置
```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/fuling.git
cd fuling

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 开发安装
pip install -e .
```

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_cli.py

# 带覆盖率报告
pytest --cov=fuling tests/
```

### 代码规范
```bash
# 代码格式化
black fuling_cli.py fuling_core.py fuling_ai.py

# 代码检查
flake8 fuling_cli.py fuling_core.py fuling_ai.py

# 类型检查（可选）
mypy fuling_cli.py fuling_core.py fuling_ai.py
```

## 📚 文档目录

### 用户文档
- [快速开始](docs/QUICK_START.md) - 5分钟上手
- [命令参考](docs/COMMAND_REFERENCE.md) - 所有命令详解
- [配置指南](docs/CONFIGURATION.md) - 详细配置说明
- [主题定制](docs/THEMES.md) - 主题系统使用
- [AI提供商](docs/AI_PROVIDERS.md) - AI后端配置

### 开发者文档
- [架构设计](docs/ARCHITECTURE.md) - 系统架构
- [API参考](docs/API_REFERENCE.md) - 模块API
- [插件开发](docs/PLUGIN_DEVELOPMENT.md) - 开发插件
- [贡献指南](docs/CONTRIBUTING.md) - 参与贡献
- [发布流程](docs/RELEASE_PROCESS.md) - 版本发布

### 示例
- [基础使用](examples/basic_usage.py)
- [代码生成](examples/code_generation.py)
- [自动化脚本](examples/automation.py)
- [插件示例](examples/plugin_example.py)

## 🚀 路线图

### v0.1.0 (当前)
- ✅ 基础CLI框架
- ✅ 命令解释功能
- ✅ 本地知识库
- ✅ 主题系统基础
- ✅ 多AI提供商架构

### v0.2.0 (开发中)
- 🔄 真实AI集成
- 🔄 代码生成优化
- 🔄 插件系统框架
- 🔄 性能监控
- 🔄 完整文档

### v0.3.0 (计划中)
- 📅 高级代码重构
- 📅 团队协作功能
- 📅 可视化界面
- 📅 插件市场
- 📅 云同步

### v1.0.0 (目标)
- 🎯 生产就绪
- 🎯 完整测试覆盖
- 🎯 社区生态
- 🎯 企业功能
- 🎯 多语言支持

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 代码风格
- 添加适当的类型注解
- 编写单元测试
- 更新相关文档
- 保持向后兼容性

### 报告问题
请使用 [GitHub Issues](https://github.com/yourusername/fuling/issues) 报告bug或提出功能建议。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下项目和技术的启发：
- [OpenClaw](https://github.com/openclaw/openclaw) - 开源AI助手框架
- [Moonshot AI](https://www.moonshot.cn/) - Kimi智能助手
- [Click](https://click.palletsprojects.com/) - Python CLI框架
- [Rich](https://github.com/Textualize/rich) - 终端美化库

## 📞 联系方式

- **GitHub**: [yourusername/fuling](https://github.com/yourusername/fuling)
- **问题反馈**: [GitHub Issues](https://github.com/yourusername/fuling/issues)
- **讨论区**: [GitHub Discussions](https://github.com/yourusername/fuling/discussions)

---

<div align="center">

**符灵 - 让命令行更智能，让开发更高效**

![符灵](docs/images/fuling_banner.png)

</div>