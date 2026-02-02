"""
初始化命令 - 首次设置AI-CLI
"""

import os
import click
from pathlib import Path
import sys

from ..core.config import get_config, save_config
from ..utils.errors import format_error

@click.command()
@click.option('--force', '-f', is_flag=True, help='强制重新初始化')
def init(force):
    """初始化AI-CLI配置
    
    首次使用时运行此命令设置API密钥和配置。
    """
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        
        # 检查是否已初始化
        config_dir = Path.home() / ".config" / "ai-cli"
        config_file = config_dir / "config.yaml"
        
        if config_file.exists() and not force:
            console.print(Panel(
                Text().append("✅ AI-CLI 已初始化", style="bold green").append(
                    f"\n配置文件: {config_file}", style="dim"
                ),
                title="状态",
                border_style="green"
            ))
            console.print("\n如需重新初始化，使用: [cyan]ai init --force[/]")
            return
        
        # 显示初始化向导
        console.print(Panel(
            Text().append("🚀 AI-CLI 初始化向导", style="bold cyan"),
            title="欢迎",
            border_style="cyan",
            padding=(1, 2)
        ))
        
        # 创建配置目录
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # 基本配置
        config = {
            "model": {
                "name": "kimi-k2-turbo-preview",
                "provider": "moonshot",
                "api_key": "",  # 用户需要自己设置
                "base_url": "https://api.moonshot.cn/v1",
                "temperature": 0.3,
                "max_tokens": 1000,
                "timeout": 30
            },
            "features": {
                "auto_suggest": True,
                "explain_commands": True,
                "learn_patterns": True,
                "safety_check": True,
                "enable_cache": True,
                "debug_mode": False
            },
            "aliases": {
                "cleanup": "find . -name '*.pyc' -delete",
                "stats": "git log --oneline | wc -l",
                "largefiles": "find . -type f -size +10M",
                "proj": "cd ~/projects",
                "dirsize": "du -sh .",
                "recent": "find . -type f -mtime -1"
            }
        }
        
        # 保存配置
        save_config(config)
        
        # 显示成功信息
        console.print(Panel(
            Text()
                .append("✅ 初始化完成！", style="bold green")
                .append(f"\n配置文件已创建: {config_file}", style="dim")
                .append("\n\n下一步:", style="bold")
                .append("\n1. 编辑配置文件设置API密钥", style="dim")
                .append("\n2. 或设置环境变量: ", style="dim")
                .append("export MOONSHOT_API_KEY='your_key'", style="cyan")
                .append("\n3. 测试: ", style="dim")
                .append("ai explain 'ls -la'", style="cyan"),
            title="完成",
            border_style="green",
            padding=(1, 2)
        ))
        
        # 显示配置文件内容
        console.print("\n[dim]配置文件内容:[/]")
        console.print(f"[dim]{config_file}:[/]")
        with open(config_file, 'r') as f:
            for line in f:
                console.print(f"[dim]  {line.rstrip()}[/]")
        
    except Exception as e:
        print(f"❌ 初始化失败: {format_error(e)}")
        sys.exit(1)