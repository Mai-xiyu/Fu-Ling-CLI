"""
聊天模式命令 - 与AI进行交互式对话
"""

import click
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from ..core.ai import get_ai_provider, AIError
from ..core.context import get_context
from ..core.config import get_config
from ..utils.errors import format_error
from ..utils.ui import print_success, print_error, print_info, spinner

console = Console()

@click.command()
@click.option('--model', '-m', help='指定AI模型')
@click.option('--temperature', '-t', type=float, help='温度参数 (0.0-1.0)')
@click.option('--system', '-s', help='系统提示词')
@click.option('--no-history', is_flag=True, help='不使用历史记录')
@click.option('--multiline', is_flag=True, help='启用多行输入')
def chat(model, temperature, system, no_history, multiline):
    """与AI进行交互式对话模式
    
    \b
    示例:
      ai chat                    # 开始聊天
      ai chat -m gpt-4          # 使用特定模型
      ai chat -t 0.7            # 设置创造性
      ai chat -s "你是一个Linux专家"  # 设置角色
    
    \b
    快捷键:
      Ctrl+D 或 /exit          # 退出
      /clear                   # 清屏
      /history                 # 查看历史
      /save <file>             # 保存对话
      /load <file>             # 加载对话
      /model <name>            # 切换模型
      /temperature <value>     # 调整温度
      /help                    # 显示帮助
    """
    
    # 获取配置
    config = get_config()
    if model:
        config['model']['name'] = model
    if temperature is not None:
        config['model']['temperature'] = temperature
    
    # 初始化AI提供商
    try:
        ai_provider = get_ai_provider(config)
    except AIError as e:
        print_error(f"AI初始化失败: {e}")
        return
    
    # 显示欢迎信息
    console.print(Panel(
        Text().append("💬 AI聊天模式", style="bold cyan").append(
            f"\n模型: {config['model']['name']} | 温度: {config['model']['temperature']}",
            style="dim"
        ),
        title="[bold]AI-CLI 聊天[/bold]",
        border_style="cyan",
        subtitle="输入 /help 查看命令，Ctrl+D 退出"
    ))
    
    # 初始化对话历史
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    else:
        messages.append({
            "role": "system", 
            "content": "你是一个有帮助的AI助手，专门帮助用户解决命令行和编程问题。回答要简洁、准确、实用。"
        })
    
    # 设置输入会话
    history_file = os.path.expanduser("~/.config/ai-cli/chat_history")
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    
    session = PromptSession(
        history=FileHistory(history_file) if not no_history else None,
        auto_suggest=AutoSuggestFromHistory(),
        multiline=multiline,
        style=Style.from_dict({
            'prompt': 'ansicyan bold',
            '': '#ffffff',
        })
    )
    
    # 命令处理函数
    def handle_command(cmd):
        cmd = cmd.strip().lower()
        
        if cmd == '/exit' or cmd == '/quit':
            return 'exit'
        elif cmd == '/clear':
            console.clear()
            return 'clear'
        elif cmd == '/history':
            if messages:
                console.print("\n[bold]对话历史:[/bold]")
                for i, msg in enumerate(messages[1:], 1):  # 跳过system消息
                    role = "👤 用户" if msg['role'] == 'user' else "🤖 AI"
                    console.print(f"{i}. {role}: {msg['content'][:100]}...")
            else:
                console.print("[dim]暂无历史[/dim]")
            return 'history'
        elif cmd.startswith('/save '):
            filename = cmd[6:].strip()
            try:
                save_chat(filename, messages)
                print_success(f"对话已保存到 {filename}")
            except Exception as e:
                print_error(f"保存失败: {e}")
            return 'save'
        elif cmd.startswith('/load '):
            filename = cmd[6:].strip()
            try:
                loaded_messages = load_chat(filename)
                messages.clear()
                messages.extend(loaded_messages)
                print_success(f"已加载对话从 {filename}")
            except Exception as e:
                print_error(f"加载失败: {e}")
            return 'load'
        elif cmd.startswith('/model '):
            new_model = cmd[7:].strip()
            config['model']['name'] = new_model
            try:
                ai_provider = get_ai_provider(config)
                print_success(f"已切换模型到 {new_model}")
            except AIError as e:
                print_error(f"模型切换失败: {e}")
            return 'model'
        elif cmd.startswith('/temperature '):
            try:
                new_temp = float(cmd[12:].strip())
                if 0.0 <= new_temp <= 1.0:
                    config['model']['temperature'] = new_temp
                    print_success(f"温度已设置为 {new_temp}")
                else:
                    print_error("温度必须在 0.0 到 1.0 之间")
            except ValueError:
                print_error("无效的温度值")
            return 'temperature'
        elif cmd == '/help':
            show_help()
            return 'help'
        
        return None
    
    def show_help():
        help_text = """
        [bold]聊天命令:[/bold]
        
        [cyan]基本命令:[/cyan]
          /exit, /quit     退出聊天
          /clear           清屏
          /history         查看对话历史
          /help            显示此帮助
        
        [cyan]文件操作:[/cyan]
          /save <文件>     保存当前对话
          /load <文件>     加载保存的对话
        
        [cyan]设置调整:[/cyan]
          /model <名称>    切换AI模型
          /temperature <值> 调整创造性 (0.0-1.0)
        
        [cyan]输入技巧:[/cyan]
          • 按 Tab 自动补全
          • 上下箭头浏览历史
          • Ctrl+D 快速退出
          • 多行模式: 使用 --multiline 参数
        """
        console.print(Panel(Markdown(help_text), title="帮助", border_style="green"))
    
    # 主聊天循环
    conversation_count = 0
    
    while True:
        try:
            # 获取用户输入
            prompt = f"[{conversation_count + 1}] 👤 "
            user_input = session.prompt(prompt)
            
            if not user_input.strip():
                continue
            
            # 检查是否是命令
            if user_input.startswith('/'):
                result = handle_command(user_input)
                if result == 'exit':
                    break
                continue
            
            # 添加到消息历史
            messages.append({"role": "user", "content": user_input})
            
            # 显示思考中
            with Live(Spinner("dots", text="思考中..."), refresh_per_second=10) as live:
                try:
                    # 获取AI响应
                    response = ai_provider.chat_completion(
                        messages=messages,
                        temperature=config['model']['temperature'],
                        max_tokens=config['model'].get('max_tokens', 1000)
                    )
                    
                    # 更新消息历史
                    messages.append({"role": "assistant", "content": response})
                    
                    # 显示响应
                    live.update(
                        Panel(
                            Markdown(response),
                            title="🤖 AI",
                            border_style="blue",
                            subtitle=f"模型: {config['model']['name']} | Tokens: 估计中..."
                        )
                    )
                    
                except AIError as e:
                    print_error(f"AI请求失败: {e}")
                    messages.pop()  # 移除失败的用户消息
                except Exception as e:
                    print_error(f"未知错误: {e}")
                    messages.pop()
            
            conversation_count += 1
            
        except KeyboardInterrupt:
            console.print("\n[yellow]中断，输入 /exit 退出[/yellow]")
            continue
        except EOFError:
            console.print("\n[green]再见！[/green]")
            break
        except Exception as e:
            print_error(f"错误: {e}")
            continue
    
    # 保存历史（可选）
    if conversation_count > 0 and not no_history:
        try:
            save_chat(f"chat_session_{conversation_count}.json", messages)
            console.print(f"[dim]对话已自动保存 ({conversation_count} 轮)[/dim]")
        except:
            pass

def save_chat(filename, messages):
    """保存对话到文件"""
    import json
    import os
    
    # 确保扩展名
    if not filename.endswith('.json'):
        filename += '.json'
    
    # 保存到配置目录
    save_dir = os.path.expanduser("~/.config/ai-cli/chats")
    os.makedirs(save_dir, exist_ok=True)
    
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "version": "1.0",
                "created_at": os.path.getctime(filepath) if os.path.exists(filepath) else None,
                "message_count": len(messages),
                "model": get_config()['model']['name']
            },
            "messages": messages
        }, f, ensure_ascii=False, indent=2)
    
    return filepath

def load_chat(filename):
    """从文件加载对话"""
    import json
    import os
    
    # 确保扩展名
    if not filename.endswith('.json'):
        filename += '.json'
    
    # 从配置目录加载
    save_dir = os.path.expanduser("~/.config/ai-cli/chats")
    filepath = os.path.join(save_dir, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("messages", [])

if __name__ == "__main__":
    chat()