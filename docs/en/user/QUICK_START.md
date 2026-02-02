# 🚀 AI-CLI 快速开始指南

## 安装

### 方式一：从源码安装（推荐）
```bash
# 克隆仓库
git clone https://github.com/xiyu-bot-assistant/ai-cli.git
cd ai-cli

# 安装依赖
pip install -e .

# 验证安装
ai --version
```

### 方式二：使用pip安装（发布后）
```bash
pip install ai-cli
```

## 配置

### 1. 初始化配置
```bash
# 交互式配置向导
ai init

# 或使用命令行参数
ai init --model moonshot --api-key $MOONSHOT_API_KEY
```

### 2. 环境变量配置
```bash
# 设置API密钥（推荐）
export MOONSHOT_API_KEY="your_api_key_here"

# 或编辑配置文件
vim ~/.config/ai-cli/config.yaml
```

### 3. 配置文件示例
```yaml
# ~/.config/ai-cli/config.yaml
model:
  name: "kimi-k2-turbo-preview"
  provider: "moonshot"
  api_key: "${MOONSHOT_API_KEY}"  # 使用环境变量
  base_url: "https://api.moonshot.cn/v1"
  temperature: 0.3

features:
  auto_suggest: true
  explain_commands: true
  learn_patterns: true
  safety_check: true

aliases:
  cleanup: "find . -name '*.pyc' -delete"
  stats: "git log --oneline | wc -l"
```

## 基本使用

### 查看帮助
```bash
# 查看所有命令
ai --help

# 查看命令详情
ai explain --help
```

### 系统状态检查
```bash
# 检查AI-CLI状态
ai status

# 检查系统资源
ai perf resources

# 性能报告
ai perf report
```

## 核心功能

### 1. 命令解释
```bash
# 解释shell命令
ai explain "find . -name '*.py' -exec grep -l import {} \;"

# 解释复杂管道
ai explain "ps aux | grep python | awk '{print $2}' | xargs kill -9"
```

### 2. 文件搜索
```bash
# 自然语言搜索
ai find "今天修改的Python文件"
ai find "大于1MB的图片文件"
ai find "包含TODO注释的文件"
```

### 3. 命令建议
```bash
# 获取建议
ai suggest

# 基于上下文的建议
ai suggest "我想清理临时文件"
```

### 4. 内容搜索
```bash
# 搜索文件内容
ai grep "数据库连接"
ai grep "TODO|FIXME" --regex
```

### 5. 历史搜索
```bash
# 搜索命令历史
ai history
ai history "git"
```

## 高级功能

### 交互模式
```bash
# 启动交互式会话
ai interactive

# 交互式配置
ai interactive --setup
```

### 插件系统
```bash
# 列出插件
ai plugin list

# 插件信息
ai plugin info example

# 插件命令
ai hello
ai calc "1 + 2 * 3"
```

### 性能监控
```bash
# 性能优化
ai perf optimize

# 系统资源
ai perf resources
```

## 使用示例

### 示例1：开发工作流
```bash
# 开始新功能开发
ai find "需要重构的代码"
ai explain "复杂的重构命令"
ai suggest "代码优化"

# 测试和验证
ai perf optimize
ai status
```

### 示例2：学习新命令
```bash
# 学习awk
ai explain "awk '{print $1}' file.txt"
ai suggest "awk使用场景"

# 练习
ai history "awk"
```

### 示例3：项目管理
```bash
# 项目分析
ai find "大文件"
ai grep "性能瓶颈"
ai perf resources

# 优化建议
ai suggest "项目优化"
```

## 故障排除

### 常见问题

#### Q1: AI功能不工作
```bash
# 检查API配置
ai config

# 测试连接
ai explain "test"  # 应该返回AI解释
```

#### Q2: 命令找不到
```bash
# 重新安装
pip install -e .

# 检查PATH
which ai
```

#### Q3: 性能问题
```bash
# 性能报告
ai perf report

# 优化启动
ai perf optimize
```

### 调试模式
```bash
# 启用调试
ai --debug status

# 查看详细错误
ai --debug explain "test"
```

## 下一步

### 学习更多
- 阅读 [API参考](./API_REFERENCE.md)
- 查看 [插件开发指南](./PLUGIN_GUIDE.md)
- 尝试 [示例代码](../examples/)

### 贡献项目
- 阅读 [贡献指南](./CONTRIBUTING.md)
- 提交Issue和PR
- 开发插件

### 获取帮助
- GitHub Issues
- 文档
- 示例代码

---

**提示**：AI-CLI会学习你的使用习惯，用得越多越智能！ 🚀