# 🔌 AI-CLI 插件开发指南

## 概述

AI-CLI 插件系统允许开发者扩展 CLI 功能，添加自定义命令和钩子。插件自动加载，支持热重载。

## 快速开始

### 1. 创建插件目录
```bash
mkdir -p ~/.config/ai-cli/plugins
```

### 2. 创建插件文件
```python
# ~/.config/ai-cli/plugins/my_plugin.py
from ai_cli.core.plugins import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("myplugin", "1.0.0")
        self.description = "我的第一个插件"
        self.author = "开发者"
        
        # 注册命令
        self.register_command(
            "hello",
            self.hello_command,
            "打招呼命令"
        )
    
    def hello_command(self, name="World"):
        """打招呼"""
        from rich.console import Console
        console = Console()
        console.print(f"[bold green]👋 Hello, {name}![/]")
        return f"Greeted {name}"
```

### 3. 使用插件
```bash
# 重启AI-CLI或运行
ai plugin list  # 查看插件
ai hello        # 使用插件命令
```

## 插件结构

### 基本结构
```python
from ai_cli.core.plugins import Plugin

class YourPlugin(Plugin):
    def __init__(self):
        # 基本信息
        super().__init__(
            name="plugin-name",      # 插件名称（英文，小写）
            version="1.0.0",         # 版本号
            description="插件描述",   # 描述
            author="作者名"          # 作者
        )
        
        # 注册命令
        self.register_command(...)
        
        # 注册钩子
        self.register_hook(...)
    
    # 命令实现
    def your_command(self, *args):
        pass
    
    # 钩子实现
    def your_hook(self, *args):
        pass
```

### 必需属性
- `name`: 插件名称（唯一标识）
- `version`: 版本号（语义化版本）
- `description`: 插件描述
- `author`: 作者信息

### 可选属性
- `commands`: 命令字典（自动管理）
- `hooks`: 钩子字典（自动管理）

## 命令系统

### 注册命令
```python
def __init__(self):
    # 基本注册
    self.register_command(
        name="command-name",      # 命令名称
        func=self.command_func,   # 命令函数
        help_text="命令帮助文本"   # 帮助文本
    )
    
    # 带参数的注册
    self.register_command(
        name="greet",
        func=self.greet_command,
        help_text="打招呼: greet <name> [--formal]"
    )
```

### 命令函数
```python
def greet_command(self, name="World", formal=False):
    """
    命令函数
    
    Args:
        name: 名称（默认 "World"）
        formal: 是否正式（默认 False）
    
    Returns:
        任意可序列化的结果
    """
    from rich.console import Console
    console = Console()
    
    if formal:
        greeting = f"Good day, {name}."
    else:
        greeting = f"Hey {name}!"
    
    console.print(f"[bold green]{greeting}[/]")
    return {"greeting": greeting, "name": name}
```

### 参数处理
```python
def complex_command(self, *args, **kwargs):
    """
    处理复杂参数
    
    AI-CLI会自动将命令行参数转换为函数参数：
    ai mycommand arg1 arg2 --option value
    
    转换为：
    func("arg1", "arg2", option="value")
    """
    # args: 位置参数列表
    # kwargs: 关键字参数字典
    
    if not args:
        return "需要参数"
    
    # 处理逻辑
    return f"处理了 {len(args)} 个参数"
```

## 钩子系统

### 可用钩子
```python
# 命令执行前
self.register_hook("before_command", self.before_hook)

# 命令执行后
self.register_hook("after_command", self.after_hook)

# 配置加载后
self.register_hook("config_loaded", self.config_hook)

# 插件加载后
self.register_hook("plugin_loaded", self.plugin_hook)
```

### 钩子函数
```python
def before_hook(self, command_name, args):
    """
    命令执行前钩子
    
    Args:
        command_name: 命令名称
        args: 参数列表
    
    Returns:
        任意结果（会被收集）
    """
    from rich.console import Console
    console = Console()
    console.print(f"[dim]🔧 准备执行: {command_name}[/]")
    
    # 可以修改args或返回数据供后续使用
    return {"plugin": self.name, "command": command_name}

def after_hook(self, command_name, args, result):
    """
    命令执行后钩子
    
    Args:
        command_name: 命令名称
        args: 参数列表
        result: 命令执行结果
    
    Returns:
        任意结果（会被收集）
    """
    from rich.console import Console
    console = Console()
    console.print(f"[dim]✅ 完成执行: {command_name}[/]")
    
    # 可以记录日志或处理结果
    return {"plugin": self.name, "result": result}
```

## 最佳实践

### 1. 错误处理
```python
def safe_command(self, *args):
    """安全的命令实现"""
    from rich.console import Console
    from ai_cli.utils.errors import format_error
    
    console = Console()
    
    try:
        # 可能失败的操作
        result = risky_operation()
        console.print(f"[green]✓ 成功: {result}[/]")
        return result
        
    except Exception as e:
        # 友好错误提示
        console.print(format_error("命令执行失败", e))
        
        # 返回错误信息
        return {"error": str(e), "success": False}
```

### 2. 配置管理
```python
import json
from pathlib import Path

def load_config(self):
    """加载插件配置"""
    config_path = Path.home() / ".config" / "ai-cli" / f"{self.name}.json"
    
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        # 默认配置
        default_config = {
            "enabled": True,
            "settings": {},
        }
        
        # 保存默认配置
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
```

### 3. 依赖检查
```python
def check_dependencies(self):
    """检查依赖"""
    import importlib
    
    dependencies = {
        "requests": "用于HTTP请求",
        "pandas": "用于数据分析（可选）",
    }
    
    missing = []
    
    for package, description in dependencies.items():
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append((package, description))
    
    if missing:
        from rich.console import Console
        console = Console()
        
        console.print("[yellow]⚠ 缺少依赖:[/]")
        for package, desc in missing:
            console.print(f"  - {package}: {desc}")
        
        console.print("\\n安装命令:")
        console.print(f"  pip install {' '.join(pkg for pkg, _ in missing)}")
        
        return False
    
    return True
```

### 4. 性能优化
```python
from ai_cli.core.performance import cache_result

@cache_result(ttl=300)  # 5分钟缓存
def expensive_operation(self, query):
    """昂贵的操作（带缓存）"""
    # 这里可能是API调用或复杂计算
    return process_query(query)
```

## 示例插件

### 天气插件
```python
"""
完整示例：天气插件
参考：examples/plugin_development.py
"""
```

### Git增强插件
```python
"""
完整示例：Git增强插件
参考：examples/plugin_development.py
"""
```

### 数据库插件
```python
class DatabasePlugin(Plugin):
    """数据库管理插件"""
    
    def __init__(self):
        super().__init__("database", "1.0.0")
        self.description = "数据库连接和查询"
        self.author = "AI-CLI Team"
        
        self.register_command("db-connect", self.connect)
        self.register_command("db-query", self.query)
        self.register_command("db-backup", self.backup)
    
    def connect(self, connection_string):
        """连接数据库"""
        # 实现数据库连接逻辑
        pass
    
    def query(self, sql):
        """执行SQL查询"""
        # 实现查询逻辑
        pass
    
    def backup(self, output_path):
        """备份数据库"""
        # 实现备份逻辑
        pass
```

## 调试和测试

### 调试插件
```python
# 添加调试输出
import logging
logging.basicConfig(level=logging.DEBUG)

# 或在命令中添加调试信息
def debug_command(self):
    from rich.console import Console
    console = Console()
    
    console.print(f"[dim]插件名称: {self.name}[/]")
    console.print(f"[dim]插件版本: {self.version}[/]")
    console.print(f"[dim]注册命令: {list(self.commands.keys())}[/]")
    console.print(f"[dim]注册钩子: {list(self.hooks.keys())}[/]")
```

### 测试插件
```python
# 创建测试文件
# tests/test_my_plugin.py

import pytest
from ai_cli.core.plugins import PluginManager

def test_plugin_loading():
    """测试插件加载"""
    manager = PluginManager()
    manager.load_plugins()
    
    plugin = manager.get_plugin("myplugin")
    assert plugin is not None
    assert plugin.name == "myplugin"
    assert plugin.version == "1.0.0"

def test_plugin_command():
    """测试插件命令"""
    manager = PluginManager()
    manager.load_plugins()
    
    cmd_info = manager.get_command("hello")
    assert cmd_info is not None
    assert cmd_info["plugin"] == "myplugin"
    
    # 执行命令
    func = cmd_info["function"]
    result = func("Test")
    assert "Test" in result
```

## 发布插件

### 1. 准备发布
```bash
# 确保代码质量
python -m black my_plugin.py
python -m flake8 my_plugin.py
python -m pytest tests/test_my_plugin.py

# 更新版本号
# 更新README（如果有）
```

### 2. 发布到GitHub
```bash
# 创建仓库
git init
git add my_plugin.py README.md
git commit -m "feat: myplugin v1.0.0"
git tag v1.0.0
git push origin main --tags
```

### 3. 分享插件
```markdown
# MyPlugin

AI-CLI 插件：提供 XXX 功能

## 安装
1. 下载插件文件
2. 放到 ~/.config/ai-cli/plugins/
3. 重启 AI-CLI

## 使用
```bash
ai mycommand --help
```

## 功能
- 功能1
- 功能2
- 功能3
```

## 常见问题

### Q1: 插件不加载
**检查**：
1. 文件是否在正确目录：`~/.config/ai-cli/plugins/`
2. 文件名是否为 `.py` 扩展名
3. 类名是否正确继承 `Plugin`
4. 是否有语法错误

### Q2: 命令不显示
**检查**：
1. 是否在 `__init__` 中注册命令
2. 命令名称是否冲突
3. 是否重启了 AI-CLI

### Q3: 钩子不执行
**检查**：
1. 钩子名称是否正确
2. 钩子函数签名是否正确
3. 是否在正确的时间点注册

### Q4: 性能问题
**建议**：
1. 使用 `@cache_result` 装饰器
2. 异步执行耗时操作
3. 优化算法和数据结构

## 资源

### 官方资源
- [API 参考](../docs/API_REFERENCE.md)
- [示例代码](../examples/)
- [GitHub 仓库](https://github.com/xiyu-bot-assistant/ai-cli)

### 社区插件
- [插件列表](https://github.com/xiyu-bot-assistant/ai-cli/wiki/Plugins)
- [插件模板](https://github.com/xiyu-bot-assistant/ai-cli-plugin-template)

### 开发工具
- [Python 3.8+](https://www.python.org/)
- [Rich](https://rich.readthedocs.io/) - 终端美化
- [Click](https://click.palletsprojects.com/) - CLI框架

## 贡献

欢迎贡献插件！请：
1. 遵循代码规范
2. 添加测试用例
3. 更新文档
4. 提交 Pull Request

---

**提示**：从简单插件开始，逐步增加功能。参考现有插件学习最佳实践。 🚀