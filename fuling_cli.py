#!/usr/bin/env python3
"""
符灵 (Fú Líng) - 智能命令行助手
古代符咒之灵，现代AI智能
"""

import click
import sys
import os
from pathlib import Path

def show_banner():
    """显示符灵横幅"""
    banner = """
    ┌─────────────────────────────────────┐
    │    ██▓▓▓▓██                         │
    │    ▓▓    ▓▓    符灵 v0.1.0          │
    │    ▓▓  ██▓▓    智能命令行助手       │
    │    ▓▓▓▓██▓▓                         │
    │    ▓▓  ▓▓▓▓    古代智慧 · 现代AI    │
    │    ██▓▓▓▓██                         │
    └─────────────────────────────────────┘
    """
    click.echo(banner)

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="0.1.0", prog_name='符灵')
def cli():
    """符灵 (Fú Líng) - 智能命令行助手
    
    古代符咒之灵，现代AI智能。
    使用AI增强你的命令行体验。
    """
    if sys.stdin.isatty() and sys.stdout.isatty():
        show_banner()
        click.echo("输入 'fl --help' 查看所有命令\n")

# 基础命令
@cli.command()
def init():
    """初始化符灵配置"""
    click.echo("🎯 初始化符灵...")
    
    # 创建配置目录
    config_dir = os.path.expanduser("~/.config/fuling")
    os.makedirs(config_dir, exist_ok=True)
    
    # 创建配置文件
    config_file = os.path.join(config_dir, "config.yaml")
    config_content = """# 符灵配置
# 古代符咒之灵，现代AI智能

model:
  name: "kimi-k2-turbo-preview"
  provider: "moonshot"
  api_key: "${MOONSHOT_API_KEY}"  # 使用环境变量
  base_url: "https://api.moonshot.cn/v1"
  temperature: 0.3
  max_tokens: 1000

features:
  auto_suggest: true
  explain_commands: true
  learn_patterns: true
  enable_cache: true

theme:
  name: "ancient"
  colors:
    primary: "#1a237e"  # 深蓝
    accent: "#ffd700"   # 金色
    text: "#ffffff"     # 白色
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    click.echo(f"✅ 符咒配置已创建: {config_file}")
    click.echo("\n📜 下一步:")
    click.echo("  1. 设置灵力源: export MOONSHOT_API_KEY='your_key'")
    click.echo("  2. 测试符咒: fl explain 'ls -la'")
    click.echo("  3. 召唤灵体: fl chat")

@cli.command()
@click.argument('command')
def explain(command):
    """解释shell命令（符咒解读）"""
    click.echo(f"🔮 解读符咒: {command}")
    
    # 模拟AI解释
    explanations = {
        "ls -la": "天眼符：显现当前目录所有隐秘与显明之物",
        "grep pattern file": "寻迹符：在卷轴中追踪特定符文轨迹",
        "find . -name '*.py'": "探宝符：寻觅当前领域所有Python秘宝",
        "ps aux | grep python": "观灵符：观察所有运行的Python灵体",
        "git commit -m": "刻印符：在时光卷轴上留下印记",
        "docker run": "召唤符：从虚空召唤容器灵体",
        "kubectl get pods": "统御符：查看掌管的容器仆从",
    }
    
    if command in explanations:
        click.echo(f"📜 {explanations[command]}")
    else:
        click.echo("💭 此符咒含义深奥，需更多灵力解读")
        click.echo("🔍 使用 'man 命令名' 查看凡间手册")

@cli.command()
def chat():
    """与符灵对话（召唤灵体）"""
    click.echo("👻 召唤符灵...")
    click.echo("(需要灵力源连接)")
    click.echo("\n🗣️ 对话模式:")
    click.echo("  • 自然语言交流")
    click.echo("  • 符咒解读与创造")
    click.echo("  • 智慧问答")
    click.echo("\n⚡ 连接灵力源:")
    click.echo("  export MOONSHOT_API_KEY='your_key'")

@cli.command()
@click.argument('specification')
@click.option('--language', '-l', default='python', help='符文语言')
@click.option('--output', '-o', type=click.Path(), help='输出卷轴')
@click.option('--template', '-t', help='符咒模板')
def generate(specification, language, output, template):
    """生成代码（创造新符咒）"""
    click.echo(f"✨ 创造新符咒: {specification}")
    click.echo(f"📝 符文语言: {language}")
    
    if output:
        click.echo(f"📜 将保存到卷轴: {output}")
    
    # 模拟生成
    examples = {
        "python": "def 灵力汇聚():\n    return '符灵之力'",
        "javascript": "function 召唤灵体() {\n  console.log('👻 灵体现身');\n}",
        "bash": "echo '符咒生效！'",
        "sql": "CREATE TABLE 符咒库 (id INT, 名称 TEXT, 威力 INT);",
    }
    
    if language in examples:
        code = examples[language]
        
        if output:
            with open(output, 'w') as f:
                f.write(code)
            click.echo(f"✅ 符咒已刻印: {output}")
        else:
            click.echo("\n" + "=" * 40)
            click.echo("📜 新生符咒:")
            click.echo("=" * 40)
            click.echo(code)
            click.echo("=" * 40)
    else:
        click.echo(f"❌ 未知符文语言: {language}")
        click.echo("可用语言: python, javascript, bash, sql")

@cli.command()
def wisdom():
    """获取智慧（帮助和建议）"""
    click.echo("🧠 符灵智慧库")
    click.echo("\n📚 常用符咒:")
    click.echo("  fl init          - 初始化符灵")
    click.echo("  fl explain CMD   - 解读符咒")
    click.echo("  fl generate SPEC - 创造新符咒")
    click.echo("  fl chat          - 召唤灵体对话")
    click.echo("  fl wisdom        - 获取智慧（当前）")
    click.echo("  fl power         - 显示灵力状态")
    
    click.echo("\n💡 智慧箴言:")
    click.echo("  • 善用符咒，勿滥用灵力")
    click.echo("  • 学习凡人手册，理解符咒本质")
    click.echo("  • 定期备份卷轴，防止符咒丢失")
    click.echo("  • 分享智慧，壮大符灵社群")

@cli.command()
def power():
    """显示灵力状态（系统状态）"""
    click.echo("⚡ 符灵灵力状态")
    
    # 检查配置
    config_dir = os.path.expanduser("~/.config/fuling")
    config_file = os.path.join(config_dir, "config.yaml")
    
    if os.path.exists(config_file):
        click.echo("✅ 符咒配置: 已就绪")
    else:
        click.echo("❌ 符咒配置: 缺失 (运行 'fl init')")
    
    # 检查灵力源
    api_key = os.environ.get('MOONSHOT_API_KEY')
    if api_key:
        click.echo(f"✅ 灵力源: 已连接 ({api_key[:8]}****)")
    else:
        click.echo("❌ 灵力源: 未连接")
        click.echo("   连接: export MOONSHOT_API_KEY='your_key'")
    
    # 显示系统信息
    import platform
    click.echo(f"💻 宿主系统: {platform.system()} {platform.release()}")
    click.echo(f"🐍 Python版本: {platform.python_version()}")
    
    click.echo("\n🎯 建议: 运行 'fl wisdom' 获取更多智慧")

@cli.command()
def fortune():
    """今日运势（随机命令建议）"""
    import random
    
    fortunes = [
        "🔮 今日宜学习新符咒，尝试 'fl generate'",
        "✨ 灵力充沛，适合解读复杂符咒",
        "📚 回顾旧符咒，温故而知新",
        "🚀 尝试自动化，创造工作流符咒",
        "💡 分享你的符咒智慧到社群",
        "🛡️ 检查系统安全，加固符咒防护",
        "🌐 探索网络符咒，学习curl/wget",
        "🗃️ 整理符咒库，优化配置",
    ]
    
    lucky_command = random.choice([
        "ls -laht",
        "find . -name '*.py' -exec grep -l 'def' {} \\;",
        "ps aux --sort=-%mem | head -10",
        "df -h",
        "du -sh * | sort -hr",
        "history | grep 'git'",
    ])
    
    click.echo("🎴 符灵占卜...")
    click.echo(f"\n📜 今日箴言: {random.choice(fortunes)}")
    click.echo(f"🎯 幸运符咒: {lucky_command}")
    click.echo(f"💡 解读: fl explain '{lucky_command}'")

def main():
    """主入口点"""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n🛑 符灵退散...")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ 符咒失效: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()