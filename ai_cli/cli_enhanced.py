#!/usr/bin/env python3
"""
增强版 CLI 入口点 - 模拟真人多次改进
"""

import click
import sys
import os
import time
from datetime import datetime
from pathlib import Path

# 尝试导入 Rich，但优雅降级
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.columns import Columns
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("注意: Rich 库未安装，使用基础输出")

from ai_cli import __version__
from ai_cli.core.config import get_config, save_config
from ai_cli.core.ai import get_ai_provider
from ai_cli.core.context import get_context
from ai_cli.core.performance import PerformanceMonitor
from ai_cli.utils.errors import handle_error, format_error, format_success

# 全局控制台
console = Console() if RICH_AVAILABLE else None

def print_welcome():
    """打印欢迎信息 - 模拟真人精心设计"""
    if not RICH_AVAILABLE:
        print(f"\n🤖 AI-CLI v{__version__}")
        print("=" * 40)
        print("Intelligent Command Line Assistant")
        print("Type 'ai --help' for commands")
        print("=" * 40)
        return
    
    # 精心设计的欢迎界面
    welcome_text = Text()
    welcome_text.append("🤖 ", style="bold cyan")
    welcome_text.append("AI-CLI ", style="bold cyan")
    welcome_text.append(f"v{__version__}", style="bold green")
    welcome_text.append("\n")
    welcome_text.append("Intelligent Command Line Assistant", style="italic dim")
    
    # 功能亮点
    features_table = Table(show_header=False, box=None, padding=(0, 2))
    features_table.add_column("Icon", width=3)
    features_table.add_column("Feature", width=30)
    
    features = [
        ("🔍", "AI-powered command explanations"),
        ("💡", "Intelligent suggestions"),
        ("🧩", "Extensible plugin system"),
        ("📊", "Performance monitoring"),
        ("🧠", "Context-aware interactions"),
        ("📚", "Learning from usage"),
    ]
    
    for icon, feature in features:
        features_table.add_row(f"[cyan]{icon}[/]", f"[white]{feature}[/]")
    
    # 使用提示
    tips = [
        "[cyan]ai explain[/] 'ls -la'  - Understand commands",
        "[cyan]ai suggest[/]           - Get recommendations",
        "[cyan]ai find[/] '*.py'       - Search for files",
        "[cyan]ai plugin list[/]       - List available plugins",
        "[cyan]ai perf report[/]       - View performance stats",
    ]
    
    # 创建主面板
    from rich.layout import Layout
    from rich import print as rprint
    
    panel = Panel(
        welcome_text,
        title="[bold]Welcome to AI-CLI[/]",
        border_style="cyan",
        padding=(1, 2),
        subtitle="[dim]Your intelligent terminal companion[/]"
    )
    
    console.print(panel)
    console.print("\n[bold]Features:[/]")
    console.print(features_table)
    console.print("\n[bold]Quick start:[/]")
    for tip in tips:
        console.print(f"  {tip}")

def check_environment():
    """检查环境 - 模拟真人调试"""
    issues = []
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required (current: {sys.version_info.major}.{sys.version_info.minor})")
    
    # 检查配置文件
    config_path = Path.home() / ".config" / "ai-cli" / "config.yaml"
    if not config_path.exists():
        issues.append("Configuration file not found. Run 'ai init'")
    
    # 检查API密钥
    if not os.getenv("MOONSHOT_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        issues.append("No API key found. Set MOONSHOT_API_KEY or OPENAI_API_KEY")
    
    return issues

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--debug', is_flag=True, help='Enable debug mode with detailed output')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--config', type=click.Path(), help='Custom config file path')
@click.option('--model', help='Override AI model')
@click.option('--no-banner', is_flag=True, help='Skip welcome banner')
@click.version_option(version=__version__, prog_name='AI-CLI')
def cli(debug, verbose, config, model, no_banner):
    """AI-CLI - Your intelligent command line assistant
    
    \b
    AI-CLI enhances your terminal with AI capabilities:
    • Explain complex commands in simple terms
    • Suggest commands based on context
    • Search and analyze files intelligently
    • Extend functionality with plugins
    • Monitor and optimize performance
    
    \b
    Get started:
      ai init                    # First-time setup
      ai explain "docker ps -a"  # Understand commands
      ai suggest                 # Get recommendations
      ai --help                  # See all commands
    """
    # 设置环境变量
    if debug:
        os.environ['AI_CLI_DEBUG'] = '1'
        click.echo("🔧 [yellow]Debug mode enabled[/yellow]")
    
    if verbose:
        os.environ['AI_CLI_VERBOSE'] = '1'
    
    if config:
        os.environ['AI_CLI_CONFIG'] = str(config)
        if verbose:
            click.echo(f"📁 Using config: {config}")
    
    if model:
        os.environ['AI_CLI_MODEL'] = model
        if verbose:
            click.echo(f"🤖 Using model: {model}")
    
    # 显示欢迎信息（如果适用）
    is_interactive = sys.stdin.isatty() and sys.stdout.isatty()
    show_banner = is_interactive and not no_banner and not debug
    
    if show_banner:
        print_welcome()
        
        # 环境检查
        issues = check_environment()
        if issues and verbose:
            console.print("\n[yellow]⚠️  Environment notes:[/yellow]")
            for issue in issues:
                console.print(f"  • {issue}")
    
    # 性能监控
    if debug:
        monitor = PerformanceMonitor()
        monitor.start_timer("cli_startup")

@cli.command()
def init():
    """Initialize AI-CLI configuration"""
    from ai_cli.commands.init import init_config
    init_config()

@cli.command()
@click.argument('command')
def explain(command):
    """Explain what a command does"""
    from ai_cli.commands.explain import explain_command
    explain_command(command)

@cli.command()
@click.argument('pattern')
def find(pattern):
    """Find files matching a pattern"""
    from ai_cli.commands.find import find_files
    find_files(pattern)

@cli.command()
@click.argument('pattern')
def grep(pattern):
    """Search for text in files"""
    from ai_cli.commands.grep import grep_files
    grep_files(pattern)

@cli.command()
def suggest():
    """Get command suggestions"""
    from ai_cli.commands.suggest import get_suggestions
    get_suggestions()

@cli.command()
def history():
    """Show command history"""
    from ai_cli.commands.history import show_history
    show_history()

@cli.command()
def status():
    """Show AI-CLI status and configuration"""
    from ai_cli.commands.status import show_status
    show_status()

@cli.command()
@click.argument('topic')
def learn(topic):
    """Learn about a topic"""
    from ai_cli.commands.learn import learn_topic
    learn_topic(topic)

@cli.group()
def plugin():
    """Manage plugins"""
    pass

@plugin.command(name='list')
def plugin_list():
    """List available plugins"""
    from ai_cli.commands.plugin import list_plugins
    list_plugins()

@plugin.command(name='info')
@click.argument('plugin_name')
def plugin_info(plugin_name):
    """Show plugin information"""
    from ai_cli.commands.plugin import plugin_info
    plugin_info(plugin_name)

@cli.group()
def perf():
    """Performance monitoring and optimization"""
    pass

@perf.command(name='report')
def perf_report():
    """Show performance report"""
    from ai_cli.commands.performance import show_performance_report
    show_performance_report()

@perf.command(name='resources')
def perf_resources():
    """Show system resource usage"""
    from ai_cli.commands.performance import show_resource_usage
    show_resource_usage()

@perf.command(name='optimize')
def perf_optimize():
    """Optimize performance"""
    from ai_cli.commands.performance import optimize_performance
    optimize_performance()

@cli.command(name='commands')
def list_commands():
    """List all available commands"""
    from ai_cli.commands.list_commands import list_all_commands
    list_all_commands()

@cli.command()
def interactive():
    """Start interactive mode"""
    from ai_cli.interactive import start_interactive
    start_interactive()

def main():
    """Main entry point - 模拟真人错误处理"""
    try:
        # 添加启动延迟，模拟真人思考
        if os.getenv('AI_CLI_DEBUG'):
            import time
            time.sleep(0.1)  # 微小延迟
        
        cli()
        
    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[yellow]👋 Interrupted by user[/yellow]")
        else:
            print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        if os.getenv('AI_CLI_DEBUG'):
            # 调试模式显示完整错误
            import traceback
            traceback.print_exc()
        else:
            # 用户友好错误
            error_msg = str(e)
            if RICH_AVAILABLE:
                console.print(f"[red]❌ Error: {error_msg}[/red]")
                console.print("[dim]Run with --debug for details[/dim]")
            else:
                print(f"Error: {error_msg}")
                print("Run with --debug for details")
        sys.exit(1)

if __name__ == '__main__':
    main()