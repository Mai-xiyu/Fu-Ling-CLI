#!/usr/bin/env python3
"""
符灵 (Fú Líng) - 增强版本
集成多AI提供商和主题系统
"""

import click
import sys
import os
from pathlib import Path

# 导入符灵模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fuling.fuling_core import config, get_config
    from fuling.fuling_ai import explain_command, chat_completion, test_ai_connection
    from fuling.fuling_theme import show_banner, format_text
except ImportError:
    # 备用导入
    from .fuling_core import config, get_config
    from .fuling_ai import explain_command, chat_completion, test_ai_connection
    from .fuling_theme import show_banner, format_text

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="0.1.0", prog_name='符灵')
def cli():
    """符灵 (Fú Líng) - 智能命令行助手
    
    古代符咒之灵，现代AI智能。
    使用AI增强你的命令行体验。
    """
    if sys.stdin.isatty() and sys.stdout.isatty():
        # 检查是否显示横幅
        fuling_config = get_config()
        features = fuling_config.get('features', {})
        
        if features.get('show_banner', True):
            show_banner()
            click.echo("输入 'fl --help' 查看所有命令\n")

@cli.command()
@click.option('--theme', type=click.Choice(['ancient', 'modern', 'dark', 'light']), 
              default='ancient', help='主题风格')
def init(theme):
    """初始化符灵配置"""
    click.echo(format_text("初始化符灵...", "prompt"))
    
    # 加载默认配置
    default_config = config.get_default_config()
    
    # 更新主题
    default_config['theme']['name'] = theme
    
    # 保存配置
    config.save_config(default_config)
    
    config_file = config.config_file
    click.echo(format_text(f"符咒配置已创建: {config_file}", "success"))
    
    click.echo("\n" + format_text("下一步:", "info"))
    click.echo(format_text("  1. 设置灵力源: export MOONSHOT_API_KEY='your_key'", "command"))
    click.echo(format_text("  2. 测试符咒: fl explain 'ls -la'", "command"))
    click.echo(format_text("  3. 召唤灵体: fl chat", "command"))
    click.echo(format_text("  4. 查看状态: fl power", "command"))

@cli.command()
@click.argument('command')
@click.option('--context', '-c', help='上下文信息')
def explain(command, context):
    """解释shell命令（符咒解读）"""
    click.echo(format_text(f"解读符咒: {command}", "prompt"))
    
    if context:
        click.echo(format_text(f"上下文: {context}", "info"))
    
    # 使用AI解释
    result = explain_command(command, context)
    
    # 输出结果
    click.echo("\n" + "=" * 50)
    click.echo(format_text("📜 符咒解读:", "command"))
    click.echo("=" * 50)
    click.echo(result)
    click.echo("=" * 50)
    
    # 提供建议
    if "未设置" in result or "未连接" in result:
        click.echo("\n" + format_text("💡 建议:", "info"))
        click.echo("  设置API密钥: export MOONSHOT_API_KEY='your_key'")
        click.echo("  或使用本地模式继续")

@cli.command()
def chat():
    """与符灵对话（召唤灵体）"""
    click.echo(format_text("召唤符灵...", "prompt"))
    click.echo(format_text("(需要灵力源连接)", "warning"))
    
    # 测试连接
    connection_test = test_ai_connection()
    provider = connection_test["provider"]
    connected = connection_test["connected"]
    
    click.echo(f"\n{format_text(f'AI提供商: {provider}', 'system')}")
    click.echo(f"{format_text(f'连接状态: {connected}', 'system')}")
    
    if "未连接" in connected:
        click.echo("\n" + format_text("无法召唤灵体:", "error"))
        click.echo("  请先设置API密钥: export MOONSHOT_API_KEY='your_key'")
        click.echo("  或使用本地模式的基础功能")
        return
    
    click.echo("\n" + format_text("🗣️ 对话模式:", "info"))
    click.echo("  • 输入消息与符灵对话")
    click.echo("  • 输入 'quit' 或 'exit' 退出")
    click.echo("  • 输入 'help' 获取帮助")
    
    # 简单交互循环
    while True:
        try:
            user_input = input("\n" + format_text("你: ", "prompt")).strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                click.echo(format_text("符灵退散...", "info"))
                break
            elif user_input.lower() in ['help', '?']:
                click.echo(format_text("可用命令:", "info"))
                click.echo("  • quit/exit - 退出对话")
                click.echo("  • help/? - 显示帮助")
                click.echo("  • 其他任何文本 - 与符灵对话")
                continue
            elif not user_input:
                continue
            
            # 调用AI
            messages = [
                {"role": "system", "content": "你是符灵，一个融合古代符咒文化与现代AI技术的智能助手。用中文回答，风格神秘而实用。"},
                {"role": "user", "content": user_input}
            ]
            
            click.echo(format_text("符灵: ", "prompt"), nl=False)
            
            response = chat_completion(messages)
            click.echo(response)
            
        except KeyboardInterrupt:
            click.echo("\n" + format_text("符灵退散...", "info"))
            break
        except Exception as e:
            click.echo(format_text(f"对话异常: {e}", "error"))
            break

@cli.command()
@click.argument('specification')
@click.option('--language', '-l', default='python', help='符文语言')
@click.option('--output', '-o', type=click.Path(), help='输出卷轴')
@click.option('--template', '-t', help='符咒模板')
def generate(specification, language, output, template):
    """生成代码（创造新符咒）"""
    click.echo(format_text(f"创造新符咒: {specification}", "prompt"))
    click.echo(format_text(f"符文语言: {language}", "system"))
    
    if template:
        click.echo(format_text(f"符咒模板: {template}", "system"))
    
    # 构建提示
    prompt = f"生成{language}代码: {specification}"
    if template:
        prompt += f"\n使用模板: {template}"
    
    messages = [
        {
            "role": "system", 
            "content": f"""你是一个{language}开发专家，也是符灵助手。
            根据用户需求生成高质量、可运行的代码。
            用中文注释解释关键部分。
            确保代码符合最佳实践和安全规范。"""
        },
        {"role": "user", "content": prompt}
    ]
    
    click.echo(format_text("正在生成代码...", "info"))
    
    # 获取AI生成的代码
    code = chat_completion(messages)
    
    # 清理代码（移除可能的markdown）
    if code.startswith('```'):
        lines = code.split('\n')
        if len(lines) >= 3:
            code = '\n'.join(lines[1:-1])
    
    # 输出结果
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(code)
            click.echo(format_text(f"符咒已刻印: {output}", "success"))
        except Exception as e:
            click.echo(format_text(f"保存失败: {e}", "error"))
    else:
        click.echo("\n" + "=" * 50)
        click.echo(format_text(f"📜 新生符咒 ({language}):", "command"))
        click.echo("=" * 50)
        click.echo(code)
        click.echo("=" * 50)
        
        # 提供使用建议
        click.echo("\n" + format_text("💡 使用建议:", "info"))
        click.echo(f"  保存到文件: fl generate \"{specification}\" -o output.{language}")
        if language == 'python':
            click.echo(f"  直接运行: python -c \"{code[:100]}...\"")

@cli.command()
def wisdom():
    """获取智慧（帮助和建议）"""
    click.echo(format_text("符灵智慧库", "prompt"))
    
    # 获取配置信息
    fuling_config = get_config()
    theme_name = fuling_config.get('theme', {}).get('name', 'ancient')
    
    click.echo(f"\n{format_text('当前主题:', 'system')} {theme_name}")
    
    click.echo("\n" + format_text("📚 常用符咒:", "command"))
    click.echo("  fl init          - 初始化符灵")
    click.echo("  fl explain CMD   - 解读符咒")
    click.echo("  fl generate SPEC - 创造新符咒")
    click.echo("  fl chat          - 召唤灵体对话")
    click.echo("  fl wisdom        - 获取智慧（当前）")
    click.echo("  fl power         - 显示灵力状态")
    click.echo("  fl fortune       - 今日运势")
    
    click.echo("\n" + format_text("💡 智慧箴言:", "info"))
    click.echo("  • 善用符咒，勿滥用灵力")
    click.echo("  • 学习凡人手册，理解符咒本质")
    click.echo("  • 定期备份卷轴，防止符咒丢失")
    click.echo("  • 分享智慧，壮大符灵社群")
    
    click.echo("\n" + format_text("🔧 技术提示:", "system"))
    click.echo("  • 设置API密钥: export MOONSHOT_API_KEY='your_key'")
    click.echo("  • 切换主题: fl init --theme modern")
    click.echo("  • 查看配置: cat ~/.config/fuling/config.yaml")

@cli.command()
def power():
    """显示灵力状态（系统状态）"""
    click.echo(format_text("符灵灵力状态", "prompt"))
    
    # 检查配置
    config_dir = Path.home() / ".config" / "fuling"
    config_file = config_dir / "config.yaml"
    
    if config_file.exists():
        click.echo(format_text("✅ 符咒配置: 已就绪", "success"))
    else:
        click.echo(format_text("❌ 符咒配置: 缺失", "error"))
        click.echo("  运行: fl init")
    
    # 测试AI连接
    connection_test = test_ai_connection()
    
    click.echo(f"\n{format_text('AI提供商:', 'system')} {connection_test['provider']}")
    click.echo(f"{format_text('连接状态:', 'system')} {connection_test['connected']}")
    
    if connection_test['test_result']:
        click.echo(f"{format_text('测试结果:', 'system')} {connection_test['test_result']}")
    
    # 显示系统信息
    import platform
    click.echo(f"\n{format_text('💻 宿主系统:', 'system')} {platform.system()} {platform.release()}")
    click.echo(f"{format_text('🐍 Python版本:', 'system')} {platform.python_version()}")
    
    # 显示主题信息
    fuling_config = get_config()
    theme_name = fuling_config.get('theme', {}).get('name', 'ancient')
    click.echo(f"{format_text('🎨 当前主题:', 'system')} {theme_name}")
    
    click.echo("\n" + format_text("🎯 建议:", "info"))
    click.echo("  运行 'fl wisdom' 获取更多智慧")
    if "未连接" in connection_test['connected']:
        click.echo("  设置API密钥: export MOONSHOT_API_KEY='your_key'")

@cli.command()
def fortune():
    """今日运势（随机命令建议）"""
    import random
    import datetime
    
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    click.echo(format_text(f"🎴 符灵占卜 - {today}", "prompt"))
    
    fortunes = [
        "🔮 今日宜学习新符咒，尝试 'fl generate'",
        "✨ 灵力充沛，适合解读复杂符咒",
        "📚 回顾旧符咒，温故而知新",
        "🚀 尝试自动化，创造工作流符咒",
        "💡 分享你的符咒智慧到社群",
        "🛡️ 检查系统安全，加固符咒防护",
        "🌐 探索网络符咒，学习curl/wget",
        "🗃️ 整理符咒库，优化配置",
        "🔍 调试代码，寻找隐藏的bug",
        "📊 分析系统性能，优化资源使用",
    ]
    
    lucky_commands = [
        "ls -laht",
        "find . -name '*.py' -exec grep -l 'def' {} \\;",
        "ps aux --sort=-%mem | head -10",
        "df -h",
        "du -sh * | sort -hr",
        "history | grep 'git'",
        "netstat -tulpn",
        "docker ps -a",
        "git log --oneline -10",
        "python -m this",
    ]
    
    lucky_command = random.choice(lucky_commands)
    
    click.echo(f"\n{format_text('📜 今日箴言:', 'info')} {random.choice(fortunes)}")
    click.echo(f"{format_text('🎯 幸运符咒:', 'command')} {lucky_command}")
    click.echo(f"{format_text('💡 解读:', 'info')} fl explain '{lucky_command}'")
    
    # 额外建议
    click.echo(f"\n{format_text('🌟 额外建议:', 'info')}")
    click.echo("  运行 'fl power' 检查系统状态")
    click.echo("  运行 'fl wisdom' 获取更多帮助")

def main():
    """主入口点"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n" + format_text("符灵退散...", "info"))
        sys.exit(1)
    except Exception as e:
        click.echo(format_text(f"❌ 符咒失效: {e}", "error"))
        sys.exit(1)

if __name__ == "__main__":
    main()