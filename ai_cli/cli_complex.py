#!/usr/bin/env python3
"""
AI-CLI 主命令行接口
"""

import os
import sys
import click
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入核心模块
from ai_cli.core.config import get_config
from ai_cli.core.ai import test_model_connection
from ai_cli.core.plugins import get_plugin_manager
from ai_cli.utils.errors import format_error

# 导入命令模块
from ai_cli.commands.init import init
from ai_cli.commands.config import config
from ai_cli.commands.status import status
from ai_cli.commands.explain import explain
from ai_cli.commands.find import find
from ai_cli.commands.suggest import suggest
from ai_cli.commands.grep import grep
from ai_cli.commands.history import history
from ai_cli.commands.learn import learn
from ai_cli.commands.interactive import interactive
from ai_cli.commands.chat import chat  # 新增聊天命令

# 导入插件和性能命令
try:
    from ai_cli.commands.plugin import plugin
    from ai_cli.commands.perf import perf
    from ai_cli.commands.commands import commands
except ImportError as e:
    print(f"注意: 部分命令加载失败: {e}")

# 版本信息
__version__ = "0.1.0"

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--debug', is_flag=True, help='启用调试模式')
@click.option('--config', 'config_file', type=click.Path(), help='配置文件路径')
@click.option('--model', help='使用的AI模型')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@click.version_option(version=__version__, prog_name='AI-CLI')
@click.pass_context
def cli(ctx, debug, config_file, model, verbose):
    """AI-CLI - 智能命令行助手
    
    \b
    示例:
      ai --help                   显示帮助
      ai init                     初始化配置
      ai explain "ls -la"         解释命令
      ai suggest                  获取命令建议
      ai find "*.py"              查找文件
      ai grep "import"            在文件中搜索
      ai chat                     交互式聊天模式
      ai plugin list              列出插件
      ai perf report              性能报告
    
    \b
    功能特性:
      • AI驱动的命令解释
      • 智能建议
      • 交互式聊天模式
      • 插件系统扩展
      • 性能监控
      • 上下文感知交互
      • 学习使用模式
    """
    # 确保上下文对象存在
    ctx.ensure_object(dict)
    
    # 存储选项到上下文
    ctx.obj['DEBUG'] = debug
    ctx.obj['VERBOSE'] = verbose
    
    # 设置环境变量
    if config_file:
        os.environ['AI_CLI_CONFIG'] = config_file
    
    if model:
        os.environ['AI_CLI_MODEL'] = model
    
    if debug:
        os.environ['AI_CLI_DEBUG'] = '1'
        click.echo(f"🔧 调试模式已启用")
    
    if verbose:
        os.environ['AI_CLI_VERBOSE'] = '1'
    
    # 显示欢迎信息（仅在交互式模式且非debug）
    is_interactive = sys.stdin.isatty() and sys.stdout.isatty()
    
    if is_interactive and not debug and not verbose:
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text
            
            console = Console()
            
            # 创建欢迎文本
            welcome_text = Text()
            welcome_text.append("🤖 AI-CLI ", style="bold cyan")
            welcome_text.append(f"v{__version__}", style="bold green")
            welcome_text.append("\n智能命令行助手", style="italic dim")
            
            # 创建面板
            panel = Panel(
                welcome_text,
                title="[bold]欢迎[/bold]",
                border_style="cyan",
                padding=(1, 2),
                subtitle="输入 'ai --help' 查看命令"
            )
            
            console.print(panel)
            
            # 显示快速提示
            if verbose:
                console.print("\n[dim]快速提示:[/dim]")
                console.print("  • 使用 [cyan]ai explain[/cyan] 解释命令")
                console.print("  • 使用 [cyan]ai suggest[/cyan] 获取建议")
                console.print("  • 使用 [cyan]ai chat[/cyan] 交互式聊天")
                console.print("  • 使用 [cyan]ai init[/cyan] 首次设置")
                console.print("  • 添加 [cyan]--verbose[/cyan] 查看详细输出")
            
        except ImportError:
            # Rich不可用，使用简单输出
            click.echo(f"AI-CLI v{__version__} - 智能命令行助手")
            click.echo("输入 'ai --help' 查看可用命令")
    
    # 如果没有子命令被调用，显示帮助
    if ctx.invoked_subcommand is None:
        if not debug and not verbose:
            click.echo("\n[dim]未指定命令，显示帮助:[/dim]\n")
        click.echo(ctx.get_help())

# 注册核心命令
cli.add_command(init)
cli.add_command(config)
cli.add_command(status)
cli.add_command(explain)
cli.add_command(find)
cli.add_command(suggest)
cli.add_command(grep)
cli.add_command(history)
cli.add_command(learn)
cli.add_command(interactive)
cli.add_command(chat)  # 注册聊天命令

# 注册可选命令（如果可用）
try:
    cli.add_command(plugin)
    cli.add_command(perf)
    cli.add_command(commands)
except NameError:
    pass  # 命令未加载，跳过

def main():
    """主入口点"""
    try:
        cli()
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
        sys.exit(1)
    except Exception as e:
        if os.environ.get('AI_CLI_DEBUG'):
            import traceback
            traceback.print_exc()
        print(f"❌ 错误: {format_error(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()