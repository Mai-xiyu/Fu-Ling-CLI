#!/usr/bin/env python3
"""
插件开发示例
"""

import os
import sys
from pathlib import Path

def create_weather_plugin():
    """创建天气插件示例"""
    
    plugin_code = '''"""
天气插件 - 获取天气信息
"""

from ai_cli.core.plugins import Plugin
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json

class WeatherPlugin(Plugin):
    """天气插件"""
    
    def __init__(self):
        super().__init__("weather", "1.0.0")
        self.description = "获取天气信息和预报"
        self.author = "AI-CLI Team"
        
        # 注册命令
        self.register_command(
            "weather",
            self.get_weather,
            "获取天气: weather <城市> [--days 3]"
        )
        
        self.register_command(
            "weather-setup",
            self.setup_api,
            "配置天气API"
        )
        
        self.register_command(
            "weather-alerts",
            self.get_alerts,
            "获取天气警报"
        )
    
    def get_weather(self, city="北京", days="3"):
        """获取天气信息"""
        console = Console()
        
        try:
            days = int(days)
            if days < 1 or days > 7:
                console.print("[red]天数必须在1-7之间[/]")
                return
            
            # 模拟天气数据（实际应使用API）
            weather_data = self._mock_weather_data(city, days)
            
            # 显示天气信息
            self._display_weather(console, city, weather_data)
            
            return weather_data
            
        except ValueError:
            console.print("[red]天数必须是数字[/]")
        except Exception as e:
            console.print(f"[red]获取天气失败: {e}[/]")
    
    def setup_api(self):
        """配置天气API"""
        console = Console()
        
        console.print(Panel.fit(
            "[bold cyan]天气API配置[/]\\n\\n"
            "1. 注册并获取API密钥\\n"
            "2. 设置环境变量:\\n"
            "   export WEATHER_API_KEY='your_key'\\n"
            "3. 或编辑配置文件:\\n"
            "   ~/.config/ai-cli/weather.json",
            title="配置说明",
            border_style="cyan"
        ))
        
        # 创建示例配置文件
        config_example = {
            "api_key": "YOUR_API_KEY_HERE",
            "provider": "openweathermap",  # 或 weatherstack, accuweather
            "units": "metric",  # metric 或 imperial
            "language": "zh",
        }
        
        config_path = Path.home() / ".config" / "ai-cli" / "weather.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "w") as f:
            json.dump(config_example, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✓ 示例配置文件已创建: {config_path}[/]")
    
    def get_alerts(self, city="北京"):
        """获取天气警报"""
        console = Console()
        
        # 模拟警报数据
        alerts = [
            {
                "type": "高温",
                "level": "黄色",
                "message": "预计最高气温将超过35°C",
                "time": "今天下午",
            },
            {
                "type": "大风",
                "level": "蓝色",
                "message": "预计有6-7级阵风",
                "time": "明天",
            },
        ]
        
        table = Table(title=f"天气警报 - {city}")
        table.add_column("类型", style="cyan")
        table.add_column("级别", style=lambda x: {
            "红色": "bold red",
            "橙色": "yellow",
            "黄色": "yellow",
            "蓝色": "blue",
        }.get(x, "white"))
        table.add_column("信息", style="green")
        table.add_column("时间", style="dim")
        
        for alert in alerts:
            table.add_row(
                alert["type"],
                alert["level"],
                alert["message"],
                alert["time"],
            )
        
        console.print(table)
        
        if not alerts:
            console.print("[green]✓ 当前无天气警报[/]")
    
    def _mock_weather_data(self, city, days):
        """模拟天气数据"""
        import random
        from datetime import datetime, timedelta
        
        weather_types = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "雷阵雨"]
        
        forecast = []
        today = datetime.now()
        
        for i in range(days):
            date = today + timedelta(days=i)
            high_temp = random.randint(20, 35)
            low_temp = random.randint(10, high_temp - 5)
            weather = random.choice(weather_types)
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()],
                "weather": weather,
                "high_temp": high_temp,
                "low_temp": low_temp,
                "humidity": random.randint(40, 90),
                "wind_speed": random.randint(1, 10),
                "wind_direction": random.choice(["北风", "南风", "东风", "西风"]),
            })
        
        return {
            "city": city,
            "current": {
                "temp": random.randint(15, 30),
                "feels_like": random.randint(15, 32),
                "weather": random.choice(weather_types),
                "humidity": random.randint(40, 80),
                "wind_speed": random.randint(1, 8),
                "pressure": random.randint(1000, 1020),
                "visibility": random.randint(5, 20),
            },
            "forecast": forecast,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    def _display_weather(self, console, city, weather_data):
        """显示天气信息"""
        current = weather_data["current"]
        forecast = weather_data["forecast"]
        
        # 当前天气
        current_panel = Panel.fit(
            f"[bold]{city}[/] 当前天气\\n\\n"
            f"🌡️  温度: [cyan]{current['temp']}°C[/] (体感: {current['feels_like']}°C)\\n"
            f"☁️  天气: [green]{current['weather']}[/]\\n"
            f"💧湿度: {current['humidity']}%\\n"
            f"🌬️ 风速: {current['wind_speed']} km/h\\n"
            f"📊气压: {current['pressure']} hPa\\n"
            f"👁️ 能见度: {current['visibility']} km",
            title="当前天气",
            border_style="blue"
        )
        
        console.print(current_panel)
        
        # 天气预报
        if forecast:
            table = Table(title=f"{city} 天气预报")
            table.add_column("日期", style="cyan")
            table.add_column("星期", style="dim")
            table.add_column("天气", style="green")
            table.add_column("温度", style="yellow")
            table.add_column("湿度", style="blue")
            table.add_column("风速", style="dim")
            
            for day in forecast:
                temp_str = f"{day['low_temp']}°C ~ {day['high_temp']}°C"
                weather_emoji = {
                    "晴": "☀️",
                    "多云": "⛅",
                    "阴": "☁️",
                    "小雨": "🌦️",
                    "中雨": "🌧️",
                    "大雨": "⛈️",
                    "雷阵雨": "⚡",
                }.get(day["weather"], "🌤️")
                
                table.add_row(
                    day["date"],
                    day["weekday"],
                    f"{weather_emoji} {day['weather']}",
                    temp_str,
                    f"{day['humidity']}%",
                    f"{day['wind_speed']} km/h {day['wind_direction']}",
                )
            
            console.print(table)
        
        console.print(f"[dim]更新时间: {weather_data['updated_at']}[/]")

def create_git_enhancer_plugin():
    """创建Git增强插件"""
    
    plugin_code = '''"""
Git增强插件 - 提供高级Git功能
"""

from ai_cli.core.plugins import Plugin
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os

class GitEnhancerPlugin(Plugin):
    """Git增强插件"""
    
    def __init__(self):
        super().__init__("git-enhancer", "1.0.0")
        self.description = "Git版本控制增强功能"
        self.author = "AI-CLI Team"
        
        # 注册命令
        self.register_command(
            "git-graph",
            self.git_graph,
            "显示Git提交图"
        )
        
        self.register_command(
            "git-cleanup",
            self.git_cleanup,
            "清理Git仓库"
        )
        
        self.register_command(
            "git-stats",
            self.git_stats,
            "显示Git统计信息"
        )
        
        self.register_command(
            "git-search",
            self.git_search,
            "搜索Git提交历史"
        )
    
    def git_graph(self, depth="20"):
        """显示Git提交图"""
        console = Console()
        
        try:
            depth = int(depth)
            cmd = ["git", "log", "--oneline", "--graph", f"--all", f"-{depth}"]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(Panel(
                    result.stdout,
                    title="Git提交图",
                    border_style="green"
                ))
            else:
                console.print("[red]不是Git仓库或Git命令失败[/]")
                console.print(f"[dim]{result.stderr}[/]")
                
        except ValueError:
            console.print("[red]深度必须是数字[/]")
        except Exception as e:
            console.print(f"[red]执行失败: {e}[/]")
    
    def git_cleanup(self):
        """清理Git仓库"""
        console = Console()
        
        cleanup_steps = [
            ("清理远程分支", "git remote prune origin"),
            ("清理本地分支", "git branch --merged | grep -v '\\*\\|main\\|master' | xargs -n 1 git branch -d"),
            ("清理reflog", "git reflog expire --expire=30.days --all"),
            ("清理垃圾", "git gc --prune=now"),
        ]
        
        table = Table(title="Git清理操作")
        table.add_column("操作", style="cyan")
        table.add_column("命令", style="dim")
        table.add_column("状态", style="bold")
        
        for description, command in cleanup_steps:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    status = "[green]✅ 成功[/]"
                else:
                    status = f"[yellow]⚠ 警告: {result.stderr[:50]}[/]"
                
                table.add_row(description, command, status)
                
            except Exception as e:
                table.add_row(description, command, f"[red]❌ 失败: {e}[/]")
        
        console.print(table)
        
        console.print("\\n[bold]建议:[/]")
        console.print("  1. 定期运行 git cleanup")
        console.print("  2. 删除已合并的分支")
        console.print("  3. 清理过期的reflog")
    
    def git_stats(self):
        """显示Git统计信息"""
        console = Console()
        
        stats_commands = [
            ("提交总数", "git rev-list --count HEAD"),
            ("作者统计", "git shortlog -s -n"),
            ("文件统计", "git ls-files | wc -l"),
            ("代码行数", "git ls-files | xargs cat | wc -l"),
            ("首次提交", "git log --reverse --oneline | head -1"),
            ("最后提交", "git log --oneline | head -1"),
        ]
        
        table = Table(title="Git统计信息")
        table.add_column("统计项", style="cyan")
        table.add_column("值", style="green")
        
        for description, command in stats_commands:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    value = result.stdout.strip()
                    if not value:
                        value = "N/A"
                else:
                    value = f"错误: {result.stderr[:30]}"
                
                table.add_row(description, value)
                
            except Exception as e:
                table.add_row(description, f"异常: {e}")
        
        console.print(table)
    
    def git_search(self, query):
        """搜索Git提交历史"""
        console = Console()
        
        search_commands = [
            ("提交信息", f"git log --oneline --grep='{query}'"),
            ("作者", f"git log --oneline --author='{query}'"),
            ("文件内容", f"git log -p -S '{query}'"),
            ("文件路径", f"git log --oneline --name-only -- '*{query}*'"),
        ]
        
        for description, command in search_commands:
            console.print(f"\\n[bold]{description}:[/]")
            
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    console.print(Panel(
                        result.stdout[:500],
                        border_style="dim"
                    ))
                else:
                    console.print("[dim]无结果[/]")
                    
            except Exception as e:
                console.print(f"[red]搜索失败: {e}[/]")

def main():
    """主函数"""
    print("🔌 插件开发示例")
    print("=" * 60)
    
    print("\\n📁 示例插件:")
    print("  1. 天气插件 (weather)")
    print("  2. Git增强插件 (git-enhancer)")
    
    print("\\n📝 使用步骤:")
    print("  1. 创建插件目录: mkdir -p ~/.config/ai-cli/plugins")
    print("  2. 保存插件代码到对应文件")
    print("  3. 重启AI-CLI或运行: ai plugin list")
    print("  4. 使用插件命令")
    
    print("\\n💡 提示:")
    print("  - 插件自动加载")
    print("  - 支持热重载（修改后重启AI-CLI）")
    print("  - 可以创建任意数量的插件")
    
    # 创建插件目录示例
    plugin_dir = Path.home() / ".config" / "ai-cli" / "plugins"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\\n📂 插件目录: {plugin_dir}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    return plugin_code

def main():
    """运行插件开发示例"""
    print("🔌 AI-CLI 插件开发示例")
    print("=" * 60)
    
    # 显示天气插件代码
    print("\n📦 天气插件示例代码:")
    print("-" * 40)
    weather_plugin = create_weather_plugin()
    print(weather_plugin[:1000] + "...")
    
    # 显示Git插件代码
    print("\n📦 Git增强插件示例代码:")
    print("-" * 40)
    git_plugin = create_git_enhancer_plugin()
    print(git_plugin[:1000] + "...")
    
    print("\n🎯 插件开发要点:")
    print("  1. 继承 Plugin 基类")
    print("  2. 在 __init__ 中注册命令和钩子")
    print("  3. 使用装饰器或直接注册")
    print("  4. 提供清晰的帮助文本")
    print("  5. 处理错误和异常")
    
    print("\n🚀 开始开发:")
    print("  1. 参考 examples/plugin_development.py")
    print("  2. 查看 docs/PLUGIN_GUIDE.md")
    print("  3. 运行现有插件示例")
    print("  4. 提交PR到GitHub")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())