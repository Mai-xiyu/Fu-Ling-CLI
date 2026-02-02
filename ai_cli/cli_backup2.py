#!/usr/bin/env python3
"""
AI-CLI 简化版命令行接口
"""

import os
import sys
import click
from pathlib import Path

# 版本信息
__version__ = "0.1.0"

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('--debug', is_flag=True, help='启用调试模式')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@click.version_option(version=__version__, prog_name='AI-CLI')
@click.pass_context
def cli(ctx, debug, verbose):
    """AI-CLI - 智能命令行助手
    
    使用AI增强你的命令行体验。
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['VERBOSE'] = verbose
    
    if debug:
        os.environ['AI_CLI_DEBUG'] = '1'
    
    if verbose:
        os.environ['AI_CLI_VERBOSE'] = '1'
    
    # 简单欢迎信息
    if sys.stdin.isatty() and sys.stdout.isatty() and not debug:
        click.echo(f"🤖 AI-CLI v{__version__} - 智能命令行助手")
        click.echo("输入 'ai --help' 查看命令\n")

# 动态导入和注册命令
def register_commands():
    """动态注册所有命令"""
    
    # 基础命令
    try:
        from .commands.init import init
        cli.add_command(init)
    except ImportError as e:
        print(f"注意: init命令加载失败: {e}")
    
    try:
        from .commands.chat import chat
        cli.add_command(chat)
    except ImportError as e:
        print(f"注意: chat命令加载失败: {e}")
    
    try:
        from .commands.explain import explain
        cli.add_command(explain)
    except ImportError as e:
        print(f"注意: explain命令加载失败: {e}")
    
    try:
        from .commands.find import find
        cli.add_command(find)
    except ImportError as e:
        print(f"注意: find命令加载失败: {e}")
    
    try:
        from .commands.suggest import suggest
        cli.add_command(suggest)
    except ImportError as e:
        print(f"注意: suggest命令加载失败: {e}")
    
    try:
        from .commands.grep import grep
        cli.add_command(grep)
    except ImportError as e:
        print(f"注意: grep命令加载失败: {e}")
    
    try:
        from .commands.history import history
        cli.add_command(history)
    except ImportError as e:
        print(f"注意: history命令加载失败: {e}")

# 注册命令
register_commands()

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
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()