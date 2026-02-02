"""
DeepSeek AI提供商
"""

import os
import json
from typing import Dict, Any, List, Optional
import requests
from .fuling_ai import AIProvider


class DeepSeekProvider(AIProvider):
    """DeepSeek AI提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', 'https://api.deepseek.com/v1')
        self.model = config.get('model', 'deepseek-chat')
        self.timeout = config.get('timeout', 30)
        
        # 如果API密钥是环境变量格式，则从环境变量获取
        if self.api_key.startswith("${") and self.api_key.endswith("}"):
            env_var = self.api_key[2:-1]
            self.api_key = os.environ.get(env_var, '')
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """DeepSeek聊天补全"""
        if not self.api_key:
            return "❌ DeepSeek API密钥未配置。请运行 'fl config' 进行配置。"
        
        try:
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建请求数据
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get('temperature', self.config.get('temperature', 0.3)),
                "max_tokens": kwargs.get('max_tokens', self.config.get('max_tokens', 1000)),
                "stream": False,
            }
            
            # 可选参数
            if 'top_p' in kwargs:
                data['top_p'] = kwargs['top_p']
            
            response = requests.post(
                url, 
                headers=headers, 
                json=data, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 记录使用情况
                usage = result.get('usage', {})
                self._log_usage(usage)
                
                return content
            else:
                error_msg = f"DeepSeek API错误: HTTP {response.status_code}"
                try:
                    error_detail = response.json().get('error', {}).get('message', '')
                    if error_detail:
                        error_msg += f" - {error_detail}"
                except:
                    pass
                
                return f"❌ {error_msg}"
                
        except requests.exceptions.Timeout:
            return "❌ DeepSeek API请求超时。请检查网络连接或稍后重试。"
        except requests.exceptions.ConnectionError:
            return "❌ 无法连接到DeepSeek API。请检查网络连接。"
        except Exception as e:
            return f"❌ DeepSeek API调用异常: {str(e)}"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令（使用DeepSeek）"""
        if not self.api_key:
            return super().explain_command(command, context)
        
        messages = [
            {
                "role": "system",
                "content": "你是一个命令行专家，专门解释Linux/Unix命令。"
                "请用中文解释命令，包含：1) 命令作用 2) 常用参数 3) 使用示例 4) 注意事项。"
                "保持专业但易懂。"
            },
            {
                "role": "user",
                "content": f"请解释这个命令: {command}"
            }
        ]
        
        if context:
            messages[1]["content"] += f"\n上下文: {context}"
        
        return self.chat_completion(messages)
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令（使用DeepSeek）"""
        if not self.api_key:
            return super().suggest_commands(context)
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一个命令行专家。根据用户需求推荐3-5个最相关的Linux/Unix命令。"
                    "每个命令包含：命令、简短描述、基本用法示例。"
                    "用JSON格式返回，格式: [{\"command\": \"cmd\", \"description\": \"desc\", \"example\": \"example\"}]"
                },
                {
                    "role": "user",
                    "content": f"根据这个需求推荐命令: {context or '日常系统管理'}"
                }
            ]
            
            response = self.chat_completion(messages)
            
            # 尝试解析JSON响应
            try:
                # 提取JSON部分（如果响应包含其他文本）
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    commands = json.loads(json_match.group())
                else:
                    commands = json.loads(response)
                
                if isinstance(commands, list):
                    return commands
            except:
                # 如果解析失败，返回默认建议
                pass
            
            return super().suggest_commands(context)
            
        except:
            return super().suggest_commands(context)
    
    def _log_usage(self, usage: Dict):
        """记录API使用情况"""
        try:
            log_file = os.path.expanduser("~/.config/fuling/deepseek_usage.log")
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            log_entry = {
                "timestamp": self._current_timestamp(),
                "model": self.model,
                "prompt_tokens": usage.get('prompt_tokens', 0),
                "completion_tokens": usage.get('completion_tokens', 0),
                "total_tokens": usage.get('total_tokens', 0),
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except:
            pass  # 静默失败，不影响主要功能
    
    def _current_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


def configure_deepseek():
    """配置DeepSeek提供商"""
    import click
    
    click.echo("\n🤖 配置DeepSeek AI提供商")
    click.echo("-" * 30)
    
    # 检查环境变量
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if api_key:
        click.echo(f"✅ 检测到环境变量 DEEPSEEK_API_KEY: {api_key[:8]}****")
        use_env = click.confirm("使用环境变量中的API密钥？", default=True)
    else:
        click.echo("⚠️  未检测到DEEPSEEK_API_KEY环境变量")
        use_env = False
    
    if use_env:
        api_key = "${DEEPSEEK_API_KEY}"
    else:
        api_key = click.prompt("请输入DeepSeek API密钥", hide_input=True)
        if not api_key.startswith("${") and not api_key.endswith("}"):
            save_to_env = click.confirm("是否保存为环境变量？", default=False)
            if save_to_env:
                os.environ['DEEPSEEK_API_KEY'] = api_key
                click.echo("✅ 已设置环境变量 DEEPSEEK_API_KEY")
                api_key = "${DEEPSEEK_API_KEY}"
    
    # 模型选择
    click.echo("\n可选模型:")
    click.echo("  1. deepseek-chat (推荐)")
    click.echo("  2. deepseek-coder")
    click.echo("  3. 自定义模型")
    
    model_choice = click.prompt("选择模型", type=int, default=1)
    
    if model_choice == 1:
        model_name = "deepseek-chat"
    elif model_choice == 2:
        model_name = "deepseek-coder"
    else:
        model_name = click.prompt("请输入模型名称", default="deepseek-chat")
    
    # 更新配置
    from .fuling_core import get_config, config as config_manager
    
    update_config = get_config()
    update_config['model'] = {
        "provider": "deepseek",
        "name": model_name,
        "api_key": api_key,
        "base_url": "https://api.deepseek.com/v1",
        "temperature": 0.3,
        "max_tokens": 1000,
        "timeout": 30,
    }
    
    config_manager.save_config(update_config)
    
    click.echo(f"\n✅ DeepSeek配置完成")
    click.echo(f"   模型: {model_name}")
    click.echo(f"   API密钥: {'环境变量' if api_key.startswith('${') else '直接配置'}")
    
    # 测试连接
    if click.confirm("是否测试连接？", default=True):
        test_deepseek_connection(api_key if not api_key.startswith("${") else os.environ.get('DEEPSEEK_API_KEY'))


def test_deepseek_connection(api_key: str):
    """测试DeepSeek连接"""
    if not api_key:
        click.echo("❌ 无法测试：API密钥为空")
        return
    
    import click
    
    click.echo("\n🔗 测试DeepSeek连接...")
    
    try:
        url = "https://api.deepseek.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            click.echo("✅ DeepSeek连接测试成功")
            models = response.json().get('data', [])
            available_models = [m['id'] for m in models[:3]]
            click.echo(f"   可用模型: {', '.join(available_models)}")
        elif response.status_code == 401:
            click.echo("❌ API密钥无效")
        elif response.status_code == 429:
            click.echo("⚠️  请求频率超限")
        else:
            click.echo(f"❌ 连接测试失败: HTTP {response.status_code}")
            
    except Exception as e:
        click.echo(f"❌ 连接测试异常: {e}")