#!/usr/bin/env python3
"""
AI-CLI 基础使用示例
"""

import subprocess
import sys
import os
from pathlib import Path

def run_ai_command(command):
    """运行AI-CLI命令"""
    print(f"\n🚀 执行: ai {command}")
    print("-" * 50)
    
    cmd = ["ai"] + command.split()
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("输出:")
        print(result.stdout[:500])
        if len(result.stdout) > 500:
            print("... (输出截断)")
    
    if result.stderr:
        print("错误:")
        print(result.stderr[:200])
    
    return result.returncode == 0

def example_1_basic_commands():
    """示例1：基础命令"""
    print("=" * 60)
    print("📚 示例1：基础命令")
    print("=" * 60)
    
    commands = [
        "--version",
        "--help",
        "status",
        "config",
        "commands",
    ]
    
    for cmd in commands:
        run_ai_command(cmd)

def example_2_ai_features():
    """示例2：AI功能"""
    print("\n" + "=" * 60)
    print("🤖 示例2：AI功能")
    print("=" * 60)
    
    commands = [
        "explain 'ls -la'",
        "explain 'find . -name \"*.py\" -exec grep -l import {} \\;'",
        "suggest",
        "find 'python files'",
        "grep 'import'",
    ]
    
    for cmd in commands:
        run_ai_command(cmd)

def example_3_plugin_system():
    """示例3：插件系统"""
    print("\n" + "=" * 60)
    print("🔌 示例3：插件系统")
    print("=" * 60)
    
    commands = [
        "plugin list",
        "perf resources",
        "perf optimize",
    ]
    
    for cmd in commands:
        run_ai_command(cmd)

def example_4_development_workflow():
    """示例4：开发工作流"""
    print("\n" + "=" * 60)
    print("💻 示例4：开发工作流")
    print("=" * 60)
    
    # 模拟开发场景
    scenarios = [
        {
            "description": "1. 开始新项目",
            "commands": [
                "init",
                "status",
            ]
        },
        {
            "description": "2. 学习新命令",
            "commands": [
                "explain 'awk \'{print $1}\' file.txt'",
                "suggest '文本处理'",
            ]
        },
        {
            "description": "3. 项目管理",
            "commands": [
                "find '大文件'",
                "grep 'TODO|FIXME'",
                "perf resources",
            ]
        },
        {
            "description": "4. 性能优化",
            "commands": [
                "perf optimize",
                "perf report",
            ]
        },
    ]
    
    for scenario in scenarios:
        print(f"\n📋 {scenario['description']}")
        for cmd in scenario["commands"]:
            run_ai_command(cmd)

def example_5_custom_plugin():
    """示例5：自定义插件示例"""
    print("\n" + "=" * 60)
    print("🎨 示例5：自定义插件")
    print("=" * 60)
    
    plugin_code = '''
"""
自定义插件示例
保存为: ~/.config/ai-cli/plugins/my_plugin.py
"""

from ai_cli.core.plugins import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("myplugin", "1.0.0")
        self.description = "我的自定义插件"
        self.author = "开发者"
        
        # 注册命令
        self.register_command(
            "greet",
            self.greet_command,
            "打招呼: greet <name>"
        )
        
        self.register_command(
            "project-info",
            self.project_info,
            "显示项目信息"
        )
    
    def greet_command(self, name="World"):
        """打招呼命令"""
        from rich.console import Console
        console = Console()
        console.print(f"[bold green]👋 Hello, {name}![/]")
        return f"Greeted {name}"
    
    def project_info(self):
        """项目信息命令"""
        import os
        from pathlib import Path
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        table = Table(title="项目信息")
        table.add_column("项目", style="cyan")
        table.add_column("值", style="green")
        
        # 当前目录信息
        cwd = Path.cwd()
        table.add_row("当前目录", str(cwd))
        table.add_row("文件数", str(len(list(cwd.glob("*")))))
        table.add_row("Python文件", str(len(list(cwd.glob("*.py")))))
        
        # Git信息（如果有）
        try:
            import subprocess
            git_branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            if git_branch:
                table.add_row("Git分支", git_branch)
        except:
            pass
        
        console.print(table)
        return "Project info displayed"
'''
    
    print("📝 插件代码示例:")
    print(plugin_code[:500] + "...")
    
    print("\n📋 使用步骤:")
    print("  1. 创建插件目录: mkdir -p ~/.config/ai-cli/plugins")
    print("  2. 保存代码到: ~/.config/ai-cli/plugins/my_plugin.py")
    print("  3. 重启AI-CLI或运行: ai plugin list")
    print("  4. 使用新命令: ai greet '开发者'")

def example_6_integration_with_other_tools():
    """示例6：与其他工具集成"""
    print("\n" + "=" * 60)
    print("🔗 示例6：与其他工具集成")
    print("=" * 60)
    
    integrations = [
        {
            "tool": "Git",
            "commands": [
                "explain 'git log --oneline --graph --all'",
                "suggest 'git工作流'",
            ]
        },
        {
            "tool": "Docker",
            "commands": [
                "explain 'docker-compose up -d'",
                "find 'Dockerfile'",
            ]
        },
        {
            "tool": "Python",
            "commands": [
                "explain 'python -m venv venv'",
                "grep 'def test_'",
            ]
        },
    ]
    
    for integration in integrations:
        print(f"\n🛠️  与 {integration['tool']} 集成:")
        for cmd in integration["commands"]:
            run_ai_command(cmd)

def main():
    """运行所有示例"""
    print("🚀 AI-CLI 使用示例")
    print("=" * 60)
    
    # 检查AI-CLI是否安装
    try:
        result = subprocess.run(["ai", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ AI-CLI未安装或不在PATH中")
            print("安装命令: pip install -e .")
            return 1
    except FileNotFoundError:
        print("❌ AI-CLI未安装")
        print("安装命令: pip install -e .")
        return 1
    
    # 运行示例
    examples = [
        example_1_basic_commands,
        example_2_ai_features,
        example_3_plugin_system,
        example_4_development_workflow,
        example_5_custom_plugin,
        example_6_integration_with_other_tools,
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\n⏹️  示例中断")
            break
        except Exception as e:
            print(f"\n⚠️  示例错误: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("🎉 示例运行完成！")
    print("=" * 60)
    
    print("\n📚 下一步:")
    print("  1. 查看文档: docs/ 目录")
    print("  2. 运行测试: python -m pytest tests/")
    print("  3. 创建插件: 参考 examples/")
    print("  4. 贡献代码: 查看 CONTRIBUTING.md")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())