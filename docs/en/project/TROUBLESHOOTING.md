# 🔧 故障排除指南

## 常见问题

### 1. 安装问题

#### 错误：无法安装依赖
```bash
# 症状
ERROR: Could not find a version that satisfies the requirement...
ERROR: No matching distribution found for...

# 解决方案
# 1. 更新pip
pip install --upgrade pip

# 2. 使用国内镜像（中国用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 安装系统依赖（Ubuntu/Debian）
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# 4. 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### 错误：权限被拒绝
```bash
# 症状
PermissionError: [Errno 13] Permission denied

# 解决方案
# 1. 使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 2. 使用用户安装
pip install --user -e .

# 3. 修复权限
sudo chown -R $USER:$USER ~/.local/
```

### 2. 配置问题

#### 错误：配置文件找不到
```bash
# 症状
ConfigError: Configuration file not found

# 解决方案
# 1. 运行初始化
ai init

# 2. 手动创建配置
mkdir -p ~/.config/ai-cli
cp config.example.yaml ~/.config/ai-cli/config.yaml

# 3. 设置环境变量
export AI_CLI_CONFIG=~/.config/ai-cli/config.yaml
```

#### 错误：API密钥无效
```bash
# 症状
AuthenticationError: Invalid API key

# 解决方案
# 1. 检查环境变量
echo $MOONSHOT_API_KEY

# 2. 更新配置文件
# 编辑 ~/.config/ai-cli/config.yaml
# 设置正确的api_key

# 3. 使用其他AI提供商
# 修改配置文件中的provider为"openai"或"ollama"
```

### 3. 运行问题

#### 错误：命令不存在
```bash
# 症状
Error: No such command 'explain'

# 解决方案
# 1. 检查安装
pip list | grep ai-cli

# 2. 重新安装
pip install -e .

# 3. 检查PATH
which ai

# 4. 使用完整路径
python -m ai_cli.cli explain "ls -la"
```

#### 错误：模块导入失败
```bash
# 症状
ModuleNotFoundError: No module named 'rich'

# 解决方案
# 1. 安装缺失依赖
pip install rich click pyyaml

# 2. 重新安装所有依赖
pip install -r requirements.txt

# 3. 检查Python版本
python --version  # 需要Python 3.8+
```

### 4. AI功能问题

#### 错误：网络连接失败
```bash
# 症状
NetworkError: Failed to connect to API

# 解决方案
# 1. 检查网络连接
curl -I https://api.moonshot.cn

# 2. 使用代理（如果需要）
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# 3. 使用离线模式
# 修改配置文件，设置provider为"local"
```

#### 错误：响应超时
```bash
# 症状
TimeoutError: Request timed out

# 解决方案
# 1. 增加超时时间
# 在配置文件中增加timeout设置

# 2. 使用本地模型
# 安装Ollama并使用本地模型

# 3. 检查API限制
# 确认API密钥有足够配额
```

### 5. 插件问题

#### 错误：插件加载失败
```bash
# 症状
PluginError: Failed to load plugin

# 解决方案
# 1. 检查插件目录
ls ~/.config/ai-cli/plugins/

# 2. 检查插件语法
python -m py_compile plugin.py

# 3. 查看详细错误
ai --debug plugin list
```

#### 错误：插件冲突
```bash
# 症状
PluginError: Plugin conflict detected

# 解决方案
# 1. 禁用冲突插件
# 编辑配置文件，在disabled_plugins中添加插件名

# 2. 更新插件版本
# 检查插件是否有更新

# 3. 报告问题
# 在GitHub Issues报告插件冲突
```

## 性能优化

### 启动速度慢
```bash
# 优化措施
# 1. 启用缓存
# 在配置文件中设置enable_cache: true

# 2. 减少预加载
# 设置preload: false

# 3. 使用轻量模式
ai --no-banner --no-animation

# 4. 编译优化
python -m py_compile ai_cli/**/*.py
```

### 内存使用高
```bash
# 优化措施
# 1. 限制缓存大小
# 在配置文件中设置max_cache_size: 50

# 2. 定期清理
ai perf cleanup

# 3. 监控资源
ai perf resources

# 4. 减少并发
# 设置max_concurrent: 2
```

## 调试技巧

### 启用调试模式
```bash
# 基本调试
ai --debug <command>

# 详细调试
AI_CLI_DEBUG=1 ai <command>

# 日志文件
tail -f ~/.config/ai-cli/logs/ai-cli.log
```

### 检查配置
```bash
# 显示当前配置
ai config

# 验证配置
ai config validate

# 导出配置
ai config export > config_backup.yaml
```

### 测试功能
```bash
# 测试AI连接
ai explain "ls -la" --debug

# 测试插件系统
ai plugin list --verbose

# 测试性能
ai perf report --detailed
```

## 获取帮助

### 官方资源
- **GitHub仓库**: https://github.com/Mai-xiyu/Fu-Ling-CLI
- **文档**: https://github.com/kawinkhae101-pixel/ai-cli/tree/main/docs
- **问题反馈**: https://github.com/kawinkhae101-pixel/ai-cli/issues

### 社区支持
- **Discord**: [链接待添加]
- **Telegram群组**: [链接待添加]
- **Stack Overflow**: 使用标签 `ai-cli`

### 紧急联系
如果遇到安全问题或紧急问题，请通过GitHub Issues报告。

## 更新日志

### 已知问题
1. **v0.1.0**: 首次发布，可能存在未知问题
2. **网络依赖**: 需要互联网连接使用AI功能
3. **平台限制**: 主要测试于Linux/macOS，Windows可能有限制

### 计划修复
- [ ] Windows平台兼容性
- [ ] 离线模式改进
- [ ] 更多AI提供商支持

---

**提示**: 如果问题仍未解决，请运行以下命令收集诊断信息：
```bash
ai status --diagnostic > diagnostic_report.txt
```

然后将报告文件附加到GitHub Issue中。 🔧