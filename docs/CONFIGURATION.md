# ⚙️ AI-CLI 配置指南

## 概述

AI-CLI 使用 YAML 格式的配置文件来管理所有设置。配置自动加载，支持环境变量和命令行参数覆盖。

## 配置文件位置

### 默认位置
```
~/.config/ai-cli/config.yaml
```

### 自定义位置
```bash
# 使用环境变量
export AI_CLI_CONFIG_DIR="~/.my-config/ai-cli"

# 或使用命令行参数
ai --config ~/custom/path/config.yaml
```

## 配置结构

### 完整示例
```yaml
# ~/.config/ai-cli/config.yaml

# AI 模型配置
model:
  # 模型名称
  name: "kimi-k2-turbo-preview"
  
  # 提供商 (moonshot, openai, ollama, local)
  provider: "moonshot"
  
  # API 密钥（建议使用环境变量）
  api_key: "${MOONSHOT_API_KEY}"
  
  # API 基础 URL
  base_url: "https://api.moonshot.cn/v1"
  
  # 温度参数 (0.0-1.0)
  temperature: 0.3
  
  # 最大 token 数
  max_tokens: 1000
  
  # 请求超时（秒）
  timeout: 30

# 功能开关
features:
  # 自动建议
  auto_suggest: true
  
  # 命令解释
  explain_commands: true
  
  # 学习模式
  learn_patterns: true
  
  # 安全检查
  safety_check: true
  
  # 缓存启用
  enable_cache: true
  
  # 调试模式
  debug_mode: false

# 命令别名
aliases:
  # 清理 Python 缓存文件
  cleanup: "find . -name '*.pyc' -delete"
  
  # 统计 Git 提交数
  stats: "git log --oneline | wc -l"
  
  # 查看大文件
  largefiles: "find . -type f -size +10M"
  
  # 快速进入项目目录
  proj: "cd ~/projects"

# 插件配置
plugins:
  # 启用的插件列表
  enabled:
    - example
    - git-enhancer
  
  # 禁用的插件列表
  disabled:
    - experimental
  
  # 插件特定配置
  settings:
    weather:
      api_key: "${WEATHER_API_KEY}"
      units: "metric"
      language: "zh"

# 用户界面配置
ui:
  # 主题颜色
  theme: "default"  # default, dark, light
  
  # 动画效果
  animations: true
  
  # 进度条样式
  progress_style: "bar"  # bar, spinner, none
  
  # 输出格式
  output_format: "rich"  # rich, plain, json

# 性能配置
performance:
  # 缓存 TTL（秒）
  cache_ttl: 300
  
  # 最大缓存大小（MB）
  max_cache_size: 100
  
  # 并发限制
  max_concurrent: 5
  
  # 启用预加载
  preload: true

# 学习配置
learning:
  # 学习模式
  mode: "adaptive"  # adaptive, passive, active
  
  # 历史记录大小
  history_size: 1000
  
  # 个性化程度 (0.0-1.0)
  personalization: 0.7
  
  # 隐私模式
  privacy_mode: false
```

## AI 模型配置

### Moonshot AI (Kimi)
```yaml
model:
  name: "kimi-k2-turbo-preview"
  provider: "moonshot"
  api_key: "${MOONSHOT_API_KEY}"
  base_url: "https://api.moonshot.cn/v1"
  temperature: 0.3
```

### OpenAI
```yaml
model:
  name: "gpt-4o"
  provider: "openai"
  api_key: "${OPENAI_API_KEY}"
  base_url: "https://api.openai.com/v1"
  temperature: 0.7
```

### Ollama (本地)
```yaml
model:
  name: "llama3.2:3b"
  provider: "ollama"
  # Ollama 不需要 API 密钥
  base_url: "http://localhost:11434"
  temperature: 0.5
```

### 本地回退
```yaml
model:
  name: "local"
  provider: "local"
  # 本地模式不使用 API
  temperature: 0.3
```

## 环境变量

### AI 服务
```bash
# Moonshot AI
export MOONSHOT_API_KEY="sk-xxxxxxxxxxxxxxxx"

# OpenAI
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"

# 其他服务
export ANTHROPIC_API_KEY="sk-xxxxxxxxxxxxxxxx"
export GEMINI_API_KEY="xxxxxxxxxxxxxxxx"
```

### AI-CLI 配置
```bash
# 调试模式
export AI_CLI_DEBUG="true"

# 配置目录
export AI_CLI_CONFIG_DIR="~/.my-config/ai-cli"

# 日志级别
export AI_CLI_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR

# 缓存目录
export AI_CLI_CACHE_DIR="~/.cache/ai-cli"
```

### 插件配置
```bash
# 天气插件
export WEATHER_API_KEY="xxxxxxxxxxxxxxxx"

# GitHub 插件
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxx"

# 其他插件
export PLUGIN_API_KEY="xxxxxxxxxxxxxxxx"
```

## 命令行配置

### 初始化配置
```bash
# 交互式配置
ai init

# 快速配置
ai init --model moonshot --api-key $MOONSHOT_API_KEY

# 指定配置文件
ai init --config ~/custom/config.yaml
```

### 查看配置
```bash
# 显示当前配置
ai config

# 显示配置路径
ai config --show-paths

# 导出配置
ai config --export > config-backup.yaml
```

### 更新配置
```bash
# 更新模型温度
ai config --set model.temperature=0.5

# 启用功能
ai config --set features.auto_suggest=true

# 添加别名
ai config --set aliases.clean="rm -rf node_modules"
```

## 配置验证

### 验证配置
```bash
# 检查配置有效性
ai config --validate

# 测试 AI 连接
ai status

# 测试所有功能
ai test --all
```

### 配置错误处理
如果配置错误，AI-CLI 会：
1. 显示错误信息
2. 使用默认值
3. 创建备份文件
4. 提供修复建议

## 配置备份和恢复

### 备份配置
```bash
# 备份到文件
ai config --export > ai-cli-backup-$(date +%Y%m%d).yaml

# 备份包括插件
ai config --export --include-plugins > full-backup.yaml
```

### 恢复配置
```bash
# 从文件恢复
ai config --import < backup.yaml

# 从环境恢复
ai init --env
```

### 迁移配置
```bash
# 从旧版本迁移
ai config --migrate

# 验证迁移
ai config --validate
```

## 高级配置

### 多环境配置
```yaml
# 开发环境
development:
  model:
    provider: "local"
  features:
    debug_mode: true

# 生产环境  
production:
  model:
    provider: "moonshot"
    api_key: "${PROD_MOONSHOT_API_KEY}"
  features:
    debug_mode: false

# 测试环境
test:
  model:
    provider: "openai"
    api_key: "${TEST_OPENAI_API_KEY}"
```

### 条件配置
```yaml
# 根据系统配置
system_specific:
  linux:
    aliases:
      open: "xdg-open"
  macos:
    aliases:
      open: "open"
  windows:
    aliases:
      open: "start"
```

### 配置模板
```yaml
# 使用模板变量
user: "${USER}"
home: "${HOME}"
timezone: "${TZ}"

model:
  api_key: "${${ENV}_API_KEY}"  # 动态环境变量
```

## 故障排除

### 常见问题

#### Q1: 配置不生效
```bash
# 检查配置文件位置
ai config --show-paths

# 重新加载配置
ai config --reload

# 检查环境变量
printenv | grep AI_CLI
```

#### Q2: AI 连接失败
```bash
# 测试连接
ai status

# 检查 API 密钥
echo $MOONSHOT_API_KEY

# 验证配置
ai config --validate
```

#### Q3: 插件不加载
```bash
# 检查插件目录
ls ~/.config/ai-cli/plugins/

# 查看插件列表
ai plugin list

# 检查插件配置
cat ~/.config/ai-cli/config.yaml | grep plugins
```

### 调试模式
```bash
# 启用调试
ai --debug status

# 详细日志
AI_CLI_LOG_LEVEL=DEBUG ai status

# 跟踪配置加载
strace -e open ai status 2>&1 | grep config
```

## 最佳实践

### 安全实践
1. **使用环境变量**存储敏感信息
2. **定期轮换** API 密钥
3. **限制配置文件**权限
4. **备份重要配置**

### 性能优化
1. **启用缓存**减少 API 调用
2. **调整温度**参数平衡创造性和准确性
3. **合理设置**超时和重试
4. **监控资源**使用情况

### 维护建议
1. **版本控制**配置文件
2. **文档化**自定义配置
3. **定期审查**配置项
4. **测试变更**在生产环境前

## 配置参考

### 完整配置项
查看 [API 参考](../docs/API_REFERENCE.md#配置参考) 获取完整的配置项说明。

### 默认值
查看源代码中的 `ai_cli/core/config.py` 获取所有配置项的默认值。

### 示例配置
查看 `config.example.yaml` 文件获取完整的配置示例。

---

**提示**: 使用 `ai config --help` 获取更多配置命令信息。