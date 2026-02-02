"""
动态命令系统 - 支持插件命令的动态加载
"""

import click
from typing import Dict, Any, Callable, List
from rich.console import Console

console = Console()

def create_plugin_command(cmd_name: str, cmd_info: Dict[str, Any]) -> Callable:
    """创建插件命令函数"""
    
    def plugin_command_func(*args, **kwargs):
        """插件命令执行函数"""
        try:
            # 执行插件命令
            func = cmd_info['function']
            
            # 处理参数
            if args:
                result = func(*args)
            else:
                result = func()
                
            return result
        except Exception as e:
            console.print(f"[red]Plugin command '{cmd_name}' error: {e}[/]")
            raise
    
    return plugin_command_func

def register_plugin_commands(cli_group: click.Group):
    """注册所有插件命令到CLI组"""
    from ai_cli.core.plugins import get_plugin_manager
    
    try:
        plugin_manager = get_plugin_manager()
        plugin_commands = plugin_manager.list_commands()
        
        registered_commands = set()
        
        for cmd_name, cmd_info in plugin_commands.items():
            # 避免重复注册
            if cmd_name in registered_commands:
                continue
                
            # 创建命令装饰器
            def make_command(cmd_name=cmd_name, cmd_info=cmd_info):
                @cli_group.command(name=cmd_name, help=cmd_info['help'])
                @click.argument('args', nargs=-1)
                @click.pass_context
                def command_func(ctx, args):
                    """插件命令"""
                    try:
                        func = cmd_info['function']
                        
                        # 执行钩子：命令执行前
                        plugin_manager.execute_hook("before_command", cmd_name, list(args))
                        
                        # 执行命令
                        if args:
                            result = func(*args)
                        else:
                            result = func()
                            
                        # 执行钩子：命令执行后
                        plugin_manager.execute_hook("after_command", cmd_name, list(args), result)
                        
                        return result
                    except Exception as e:
                        if ctx.obj.get('DEBUG', False):
                            import traceback
                            traceback.print_exc()
                        console.print(f"[red]Error in plugin command '{cmd_name}': {e}[/]")
                        raise
                
                return command_func
            
            # 注册命令
            make_command()
            registered_commands.add(cmd_name)
            console.print(f"[dim]Registered plugin command: {cmd_name}[/]")
            
    except Exception as e:
        console.print(f"[yellow]⚠ Plugin command registration failed: {e}[/]")

def get_all_commands() -> Dict[str, Dict[str, Any]]:
    """获取所有命令（内置 + 插件）"""
    from ai_cli.core.plugins import get_plugin_manager
    
    commands = {}
    
    # 获取插件命令
    try:
        plugin_manager = get_plugin_manager()
        plugin_commands = plugin_manager.list_commands()
        commands.update(plugin_commands)
    except Exception:
        pass
    
    return commands

def list_all_commands():
    """列出所有可用命令"""
    from ai_cli.core.plugins import get_plugin_manager
    
    console.print("[bold]Available Commands[/]")
    console.print("=" * 40)
    
    # 内置命令组
    console.print("\n[bold cyan]Core Commands:[/]")
    core_commands = [
        ("init", "Initialize configuration"),
        ("find", "Find files with natural language"),
        ("explain", "Explain what a command does"),
        ("suggest", "Get command suggestions"),
        ("grep", "Search file contents"),
        ("history", "Search command history"),
        ("learn", "Learn from usage patterns"),
        ("config", "Show configuration"),
        ("status", "Check system status"),
        ("interactive", "Start interactive session"),
        ("plugin", "Plugin management"),
    ]
    
    for cmd, desc in core_commands:
        console.print(f"  [green]{cmd:15}[/] {desc}")
    
    # 插件命令
    try:
        plugin_manager = get_plugin_manager()
        plugin_commands = plugin_manager.list_commands()
        
        if plugin_commands:
            console.print("\n[bold cyan]Plugin Commands:[/]")
            for cmd_name, cmd_info in plugin_commands.items():
                plugin_name = cmd_info.get('plugin', 'unknown')
                help_text = cmd_info.get('help', 'No description')
                console.print(f"  [green]{cmd_name:15}[/] {help_text} ([dim]{plugin_name}[/])")
    except Exception as e:
        console.print(f"[dim]Plugin commands: {e}[/]")
    
    console.print("\n[dim]Use 'ai <command> --help' for more information[/]")