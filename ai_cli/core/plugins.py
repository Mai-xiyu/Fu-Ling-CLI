"""
插件系统 - 允许第三方扩展AI-CLI
"""

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import sys
import os

from rich.console import Console
from rich.table import Table

console = Console()

class Plugin:
    """插件基类"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.description = ""
        self.author = ""
        self.commands = {}  # command_name -> function
        self.hooks = {}     # hook_name -> functions
        
    def register_command(self, name: str, func: Callable, help_text: str = ""):
        """注册一个新命令"""
        self.commands[name] = {
            'function': func,
            'help': help_text
        }
        
    def register_hook(self, hook_name: str, func: Callable):
        """注册一个钩子"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(func)
        
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """执行钩子"""
        results = []
        if hook_name in self.hooks:
            for func in self.hooks[hook_name]:
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    console.print(f"[yellow]⚠ Hook {hook_name} failed in {self.name}: {e}[/]")
        return results

class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.loaded = False
        
    def load_plugins(self, plugin_dir: Optional[Path] = None):
        """加载所有插件"""
        if self.loaded:
            return
            
        if plugin_dir is None:
            plugin_dir = Path.home() / ".config" / "ai-cli" / "plugins"
            
        # 创建插件目录
        plugin_dir.mkdir(parents=True, exist_ok=True)
        
        # 添加插件目录到Python路径
        if str(plugin_dir) not in sys.path:
            sys.path.insert(0, str(plugin_dir))
        
        # 扫描插件目录
        for module_info in pkgutil.iter_modules([str(plugin_dir)]):
            try:
                module = importlib.import_module(module_info.name)
                
                # 查找插件类
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj != Plugin):
                        
                        plugin_instance = obj()
                        self.plugins[plugin_instance.name] = plugin_instance
                        
                        console.print(f"[dim]Loaded plugin: {plugin_instance.name} v{plugin_instance.version}[/]")
                        
            except Exception as e:
                console.print(f"[yellow]⚠ Failed to load plugin {module_info.name}: {e}[/]")
        
        self.loaded = True
        
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """获取插件"""
        return self.plugins.get(name)
    
    def get_all_plugins(self) -> List[Plugin]:
        """获取所有插件"""
        return list(self.plugins.values())
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """在所有插件中执行钩子"""
        results = []
        for plugin in self.plugins.values():
            plugin_results = plugin.execute_hook(hook_name, *args, **kwargs)
            results.extend(plugin_results)
        return results
    
    def get_command(self, command_name: str) -> Optional[Dict[str, Any]]:
        """获取命令定义"""
        for plugin in self.plugins.values():
            if command_name in plugin.commands:
                return {
                    'plugin': plugin.name,
                    **plugin.commands[command_name]
                }
        return None
    
    def list_commands(self) -> Dict[str, Dict[str, Any]]:
        """列出所有插件命令"""
        commands = {}
        for plugin in self.plugins.values():
            for cmd_name, cmd_info in plugin.commands.items():
                commands[cmd_name] = {
                    'plugin': plugin.name,
                    'help': cmd_info['help'],
                    'function': cmd_info['function']
                }
        return commands

# 全局插件管理器实例
plugin_manager = PluginManager()

def load_plugins():
    """加载插件（惰性加载）"""
    if not plugin_manager.loaded:
        plugin_manager.load_plugins()

def get_plugin_manager() -> PluginManager:
    """获取插件管理器"""
    load_plugins()
    return plugin_manager

# 示例插件
class ExamplePlugin(Plugin):
    """示例插件 - 演示插件系统功能"""
    
    def __init__(self):
        super().__init__("example", "1.0.0")
        self.description = "示例插件，演示插件系统功能"
        self.author = "AI-CLI Team"
        
        # 注册命令
        self.register_command(
            "hello",
            self.hello_command,
            "打招呼命令"
        )
        
        self.register_command(
            "calc",
            self.calc_command,
            "简单计算器"
        )
        
        # 注册钩子
        self.register_hook("before_command", self.before_command_hook)
        self.register_hook("after_command", self.after_command_hook)
    
    def hello_command(self, name: str = "World"):
        """打招呼"""
        from rich import print as rprint
        rprint(f"[bold green]Hello, {name}![/]")
        rprint(f"[dim]来自 {self.name} 插件[/]")
        return f"Greeted {name}"
    
    def calc_command(self, expression: str):
        """简单计算"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            console.print(f"[bold]Result:[/] {expression} = [green]{result}[/]")
            return result
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return None
    
    def before_command_hook(self, command_name: str, args: List[str]):
        """命令执行前钩子"""
        console.print(f"[dim]📝 Plugin {self.name}: Before command '{command_name}'[/]")
        return {"plugin": self.name, "hook": "before", "command": command_name}
    
    def after_command_hook(self, command_name: str, args: List[str], result: Any):
        """命令执行后钩子"""
        console.print(f"[dim]✅ Plugin {self.name}: After command '{command_name}'[/]")
        return {"plugin": self.name, "hook": "after", "command": command_name, "result": result}

# 内置插件
class GitPlugin(Plugin):
    """Git集成插件"""
    
    def __init__(self):
        super().__init__("git", "1.0.0")
        self.description = "Git版本控制集成"
        self.author = "AI-CLI Team"
        
        self.register_command(
            "git-status",
            self.git_status,
            "显示Git状态（增强版）"
        )
        
        self.register_command(
            "git-branch-info",
            self.git_branch_info,
            "显示分支详细信息"
        )
    
    def git_status(self):
        """增强的Git状态"""
        import subprocess
        
        try:
            # 基本状态
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    console.print("[bold]Git Status:[/]")
                    for line in output.split('\n'):
                        if line:
                            status = line[:2]
                            file = line[3:]
                            color = "green" if status == "??" else "yellow" if "M" in status else "red"
                            console.print(f"  [{color}]{status}[/] {file}")
                else:
                    console.print("[green]✓ Working directory clean[/]")
            else:
                console.print("[yellow]⚠ Not a git repository[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    def git_branch_info(self):
        """分支信息"""
        import subprocess
        
        try:
            # 当前分支
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            )
            
            if branch_result.returncode == 0:
                current_branch = branch_result.stdout.strip()
                console.print(f"[bold]Current branch:[/] [cyan]{current_branch}[/]")
                
                # 最后提交
                log_result = subprocess.run(
                    ["git", "log", "-1", "--oneline"],
                    capture_output=True,
                    text=True
                )
                
                if log_result.returncode == 0:
                    console.print(f"[bold]Last commit:[/] [dim]{log_result.stdout.strip()}[/]")
                    
                # 远程信息
                remote_result = subprocess.run(
                    ["git", "remote", "-v"],
                    capture_output=True,
                    text=True
                )
                
                if remote_result.returncode == 0 and remote_result.stdout:
                    console.print("[bold]Remotes:[/]")
                    for line in remote_result.stdout.strip().split('\n'):
                        if line:
                            console.print(f"  [dim]{line}[/]")
            else:
                console.print("[yellow]⚠ Not a git repository[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

def list_plugins_command():
    """列出所有插件"""
    manager = get_plugin_manager()
    plugins = manager.get_all_plugins()
    
    if not plugins:
        console.print("[yellow]No plugins loaded[/]")
        return
    
    table = Table(title="Loaded Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description", style="dim")
    table.add_column("Author", style="dim")
    
    for plugin in plugins:
        table.add_row(
            plugin.name,
            plugin.version,
            plugin.description,
            plugin.author
        )
    
    console.print(table)
    
    # 列出命令
    commands = manager.list_commands()
    if commands:
        console.print("\n[bold]Available Plugin Commands:[/]")
        for cmd_name, cmd_info in commands.items():
            console.print(f"  [green]{cmd_name}[/] - {cmd_info['help']} ([dim]{cmd_info['plugin']}[/])")

def plugin_info_command(plugin_name: str):
    """显示插件详细信息"""
    manager = get_plugin_manager()
    plugin = manager.get_plugin(plugin_name)
    
    if not plugin:
        console.print(f"[red]Plugin '{plugin_name}' not found[/]")
        return
    
    console.print(f"[bold]Plugin:[/] [cyan]{plugin.name}[/] v{plugin.version}")
    console.print(f"[bold]Description:[/] {plugin.description}")
    console.print(f"[bold]Author:[/] {plugin.author}")
    
    if plugin.commands:
        console.print("\n[bold]Commands:[/]")
        for cmd_name, cmd_info in plugin.commands.items():
            console.print(f"  [green]{cmd_name}[/] - {cmd_info['help']}")
    
    if plugin.hooks:
        console.print("\n[bold]Hooks:[/]")
        for hook_name, hook_funcs in plugin.hooks.items():
            console.print(f"  [dim]{hook_name}[/] ({len(hook_funcs)} functions)")