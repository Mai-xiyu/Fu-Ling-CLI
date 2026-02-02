"""
解释命令 - 使用AI解释shell命令
"""

import click

@click.command()
@click.argument('command')
@click.option('--context', '-c', help='额外上下文信息')
def explain(command, context):
    """使用AI解释shell命令的功能
    
    \b
    示例:
      ai explain "ls -la"
      ai explain "grep -r pattern ." --context "在项目中搜索"
    """
    try:
        from ..core.ai import explain_command
        
        explanation = explain_command(command, context)
        
        # 简单输出
        click.echo(f"🤖 命令解释: [cyan]{command}[/]")
        if context:
            click.echo(f"📝 上下文: {context}")
        click.echo("\n" + explanation)
        
    except Exception as e:
        click.echo(f"❌ 解释失败: {e}")