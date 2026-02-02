# 📚 AI-CLI API 参考

## 核心模块

### `ai_cli.cli`
主CLI入口点。

```python
from ai_cli.cli import cli

# 直接调用CLI
if __name__ == "__main__":
    cli()
```

**装饰器**：
- `@cli.command()` - 注册新命令
- `@click.option()` - 命令选项
- `@click.argument()` - 命令参数

### `ai_cli.core.config`
配置管理模块。

```python
from ai_cli.core.config import get_config, update_config, CONFIG_FILE

# 获取配置
config = get_config()
print(config["model"]["provider"])

# 更新配置
update_config({"model": {"temperature": 0.5}})

# 配置文件路径
print(CONFIG_FILE)  # ~/.config/ai-cli/config.yaml
```

**函数**：
- `get_config()` → Dict - 获取当前配置
- `update_config(updates: Dict)` - 更新配置
- `add_alias(alias: str, command: str)` - 添加别名
- `remove_alias(alias: str)` - 删除别名

### `ai_cli.core.ai`
AI模型集成模块。

```python
from ai_cli.core.ai import get_model, generate_command, test_model_connection

# 获取模型实例
model = get_model()

# 生成AI响应
response = model.generate("解释ls命令")

# 测试连接
if test_model_connection():
    print("AI连接正常")
```

**类**：
- `AIModel` - AI模型基类
- `OpenAIModel` - OpenAI兼容模型
- `LocalModel` - 本地回退模型

**函数**：
- `get_model() → AIModel` - 获取配置的模型
- `generate_command(context: Dict, query: str) → str` - 生成命令
- `test_model_connection() → bool` - 测试AI连接

### `ai_cli.core.context`
上下文感知模块。

```python
from ai_cli.core.context import get_context

# 获取当前上下文
context = get_context()
print(context["directory"])  # 当前目录
print(context["git"]["is_repo"])  # 是否Git仓库
```

**函数**：
- `get_context() → Dict` - 获取当前上下文
- `get_git_info() → Dict` - 获取Git信息
- `get_directory_contents() → List[str]` - 获取目录内容

### `ai_cli.core.plugins`
插件系统模块。

```python
from ai_cli.core.plugins import Plugin, plugin_manager

# 创建插件
class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("myplugin", "1.0.0")
        self.register_command("hello", self.hello)
    
    def hello(self):
        return "Hello from plugin!"

# 获取插件管理器
manager = plugin_manager
plugins = manager.get_all_plugins()
```

**类**：
- `Plugin` - 插件基类
- `PluginManager` - 插件管理器

**函数**：
- `load_plugins()` - 加载插件
- `get_plugin_manager() → PluginManager` - 获取插件管理器

### `ai_cli.core.performance`
性能监控模块。

```python
from ai_cli.core.performance import (
    measure_performance, 
    PerformanceMonitor,
    cache_result
)

# 性能测量装饰器
@measure_performance("my_function")
def my_function():
    pass

# 缓存装饰器（5分钟）
@cache_result(ttl=300)
def expensive_operation():
    pass

# 性能监控器
monitor = PerformanceMonitor()
monitor.start_timer("operation")
# ... 操作 ...
elapsed = monitor.stop_timer("operation")
```

## 命令模块

### `ai_cli.commands.find`
文件搜索命令。

```python
from ai_cli.commands.find import find_files, parse_natural_language_query

# 自然语言搜索
results = find_files("今天修改的Python文件")

# 解析查询
query_info = parse_natural_language_query("大于1MB的图片")
```

### `ai_cli.commands.explain`
命令解释命令。

```python
from ai_cli.commands.explain import explain_command

# 解释命令
explanation = explain_command("find . -name '*.py'")
```

### `ai_cli.commands.suggest`
命令建议命令。

```python
from ai_cli.commands.suggest import suggest_commands

# 获取建议
suggestions = suggest_commands("清理临时文件")
```

### `ai_cli.commands.grep`
内容搜索命令。

```python
from ai_cli.commands.grep import search_contents

# 搜索内容
results = search_contents("数据库连接")
```

### `ai_cli.commands.history`
历史搜索命令。

```python
from ai_cli.commands.history import search_history

# 搜索历史
history = search_history("git")
```

## 工具模块

### `ai_cli.utils.errors`
错误处理工具。

```python
from ai_cli.utils.errors import (
    handle_error,
    safe_execute,
    format_error,
    format_success
)

# 安全执行
result = safe_execute(risky_function)

# 格式化输出
print(format_success("操作成功"))
print(format_error("操作失败", Exception("错误详情")))
```

**异常类**：
- `AICLIError` - 基类异常
- `ConfigError` - 配置错误
- `AIError` - AI相关错误
- `PluginError` - 插件错误

## 配置参考

### 配置文件结构
```yaml
# ~/.config/ai-cli/config.yaml
model:
  # 必填：模型名称
  name: "kimi-k2-turbo-preview"
  
  # 必填：提供商 (moonshot, openai, ollama, local)
  provider: "moonshot"
  
  # 可选：API密钥（建议使用环境变量）
  api_key: "${MOONSHOT_API_KEY}"
  
  # 可选：API基础URL
  base_url: "https://api.moonshot.cn/v1"
  
  # 可选：温度参数 (0.0-1.0)
  temperature: 0.3
  
  # 可选：最大token数
  max_tokens: 1000

features:
  # 自动建议
  auto_suggest: true
  
  # 命令解释
  explain_commands: true
  
  # 学习模式
  learn_patterns: true
  
  # 安全检查
  safety_check: true

aliases:
  # 自定义别名
  cleanup: "find . -name '*.pyc' -delete"
  stats: "git log --oneline | wc -l"

plugins:
  # 插件配置
  enabled:
    - example
    - git
  disabled:
    - experimental
```

### 环境变量
```bash
# AI配置
export MOONSHOT_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"

# AI-CLI配置
export AI_CLI_DEBUG="true"  # 调试模式
export AI_CLI_CONFIG_DIR="~/.my-config/ai-cli"  # 自定义配置目录
```

## 插件开发API

### 插件基类
```python
from ai_cli.core.plugins import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="myplugin",
            version="1.0.0",
            description="我的插件",
            author="开发者"
        )
        
        # 注册命令
        self.register_command(
            name="mycommand",
            func=self.my_command,
            help_text="我的命令帮助"
        )
        
        # 注册钩子
        self.register_hook("before_command", self.before_hook)
        self.register_hook("after_command", self.after_hook)
    
    def my_command(self, *args):
        """命令实现"""
        return "命令执行结果"
    
    def before_hook(self, command_name, args):
        """命令执行前钩子"""
        pass
    
    def after_hook(self, command_name, args, result):
        """命令执行后钩子"""
        pass
```

### 钩子系统
可用钩子：
- `before_command` - 命令执行前
- `after_command` - 命令执行后
- `config_loaded` - 配置加载后
- `plugin_loaded` - 插件加载后

## 扩展点

### 自定义AI模型
```python
from ai_cli.core.ai import AIModel

class CustomModel(AIModel):
    def __init__(self, config):
        super().__init__(config)
        # 自定义初始化
    
    def generate(self, prompt, system_prompt=None):
        # 自定义生成逻辑
        return "自定义响应"
```

### 自定义命令
```python
import click
from ai_cli.cli import cli

@cli.command()
@click.argument('name')
def greet(name):
    """打招呼命令"""
    click.echo(f"Hello, {name}!")
```

### 自定义输出格式
```python
from rich.console import Console
from rich.table import Table

console = Console()

def custom_output(data):
    table = Table(title="自定义输出")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in data.items():
        table.add_row(key, str(value))
    
    console.print(table)
```

## 最佳实践

### 1. 错误处理
```python
from ai_cli.utils.errors import handle_error

@handle_error
def risky_operation():
    # 可能失败的操作
    pass
```

### 2. 性能优化
```python
from ai_cli.core.performance import cache_result

@cache_result(ttl=300)  # 5分钟缓存
def expensive_api_call():
    pass
```

### 3. 配置管理
```python
# 使用环境变量而非硬编码
import os
api_key = os.getenv("MOONSHOT_API_KEY")
```

### 4. 插件开发
```python
# 保持插件轻量
# 使用钩子而非修改核心代码
# 提供清晰的文档
```

## 版本兼容性

### Python版本
- Python 3.8+
- 推荐 Python 3.10+

### 依赖版本
- click >= 8.0.0
- rich >= 13.0.0
- pyyaml >= 6.0.0
- openai >= 0.27.0 (可选)

### 向后兼容
- 主要版本变更可能破坏API
- 次要版本保持向后兼容
- 补丁版本只修复bug

---

**更多信息**：
- 查看 [插件开发指南](./PLUGIN_GUIDE.md)
- 参考 [示例代码](../examples/)
- 提交 [Issue](https://github.com/Mai-xiyu/Fu-Ling-CLI/issues)