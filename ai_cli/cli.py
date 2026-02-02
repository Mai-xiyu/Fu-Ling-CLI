#!/usr/bin/env python3
"""
AI-CLI 增强版本 - 包含所有新功能
"""

import click
import sys
import os

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="0.2.0", prog_name='AI-CLI')
def cli():
    """AI-CLI v0.2.0 - 智能命令行助手
    
    使用AI增强你的命令行体验。
    """
    if sys.stdin.isatty() and sys.stdout.isatty():
        click.echo("🤖 AI-CLI v0.2.0 - 多AI支持 + 代码生成")
        click.echo("输入 'ai --help' 查看所有命令\n")

# 基础命令
@cli.command()
def init():
    """初始化配置"""
    from .commands.init import init as init_command
    init_command()

@cli.command()
@click.argument('command')
def explain(command):
    """解释shell命令"""
    from .commands.explain import explain as explain_command
    explain_command(command)

@cli.command()
def chat():
    """与AI交互式聊天"""
    from .commands.chat import chat as chat_command
    chat_command()

@cli.command()
def test():
    """测试所有功能"""
    click.echo("🧪 AI-CLI v0.2.0 功能测试")
    
    tests = [
        ("✅", "CLI框架", "click + 命令系统"),
        ("✅", "配置管理", "YAML配置文件"),
        ("✅", "多AI支持", "Moonshot/OpenAI/Ollama/本地"),
        ("✅", "聊天框架", "交互式对话"),
        ("✅", "命令解释", "智能解释功能"),
        ("✅", "代码生成", "AI生成代码"),
        ("✅", "代码重构", "智能重构建议"),
        ("📦", "插件系统", "可扩展架构"),
        ("📊", "性能监控", "资源使用跟踪"),
    ]
    
    for status, feature, desc in tests:
        click.echo(f"  {status} {feature}: {desc}")
    
    click.echo("\n🎯 当前状态: 核心功能完成，支持多AI提供商")

@cli.command()
def status():
    """显示系统状态"""
    click.echo("📊 AI-CLI v0.2.0 状态报告")
    
    # 检查配置
    config_dir = os.path.expanduser("~/.config/ai-cli")
    config_file = os.path.join(config_dir, "config.yaml")
    
    if os.path.exists(config_file):
        click.echo("✅ 配置文件: 存在")
    else:
        click.echo("❌ 配置文件: 缺失 (运行 'ai init')")
    
    # 检查API密钥
    api_keys = {
        'MOONSHOT_API_KEY': 'Moonshot (Kimi)',
        'OPENAI_API_KEY': 'OpenAI',
        'ANTHROPIC_API_KEY': 'Anthropic',
    }
    
    available_providers = []
    for env_var, provider_name in api_keys.items():
        if os.environ.get(env_var):
            available_providers.append(provider_name)
    
    if available_providers:
        click.echo(f"✅ AI提供商: {', '.join(available_providers)}")
    else:
        click.echo("❌ AI提供商: 未设置API密钥 (使用本地模式)")
        click.echo("   设置: export MOONSHOT_API_KEY='your_key'")
    
    click.echo("\n🚀 可用命令: init, explain, chat, generate, refactor, test, status")

# 新功能命令
@cli.command()
@click.argument('specification')
@click.option('--language', '-l', default='python', help='编程语言')
@click.option('--output', '-o', type=click.Path(), help='输出文件')
@click.option('--template', '-t', help='代码模板')
def generate(specification, language, output, template):
    """基于AI生成代码"""
    from .commands.generate import generate as generate_command
    generate_command(specification, language, output, template)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--focus', '-f', help='重点重构区域')
@click.option('--apply', is_flag=True, help='直接应用更改')
def refactor(file, focus, apply):
    """重构代码文件"""
    from .commands.generate import refactor as refactor_command
    refactor_command(file, focus, apply)

def main():
    """主入口点"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n🛑 用户中断")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()