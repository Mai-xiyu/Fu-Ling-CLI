"""
OpenAI提供商实现
"""

import os
from typing import Dict, Any, List, Optional
from .fuling_ai import AIProvider

class OpenAIProvider(AIProvider):
    """OpenAI 提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')
        self.organization = config.get('organization')
        
        if not self.api_key:
            raise ValueError("OpenAI API密钥未设置")
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """OpenAI聊天补全"""
        try:
            # 尝试使用openai库
            try:
                from openai import OpenAI
                
                client_kwargs = {
                    "api_key": self.api_key,
                    "base_url": self.base_url,
                }
                if self.organization:
                    client_kwargs["organization"] = self.organization
                
                client = OpenAI(**client_kwargs)
                
                response = client.chat.completions.create(
                    model=self.name,
                    messages=messages,
                    temperature=kwargs.get('temperature', self.temperature),
                    max_tokens=kwargs.get('max_tokens', self.max_tokens),
                    stream=False,
                )
                
                return response.choices[0].message.content
                
            except ImportError:
                # 回退到requests
                return self._chat_completion_via_requests(messages, kwargs)
                
        except Exception as e:
            error_msg = str(e)
            if "Incorrect API key" in error_msg or "invalid_api_key" in error_msg:
                return "🔑 OpenAI API密钥无效，请检查OPENAI_API_KEY"
            elif "rate limit" in error_msg.lower():
                return "🚫 请求频率超限，请稍后重试"
            elif "insufficient_quota" in error_msg:
                return "💰 API额度不足，请检查账户余额"
            elif "context length" in error_msg.lower():
                return "📏 上下文长度超限，请缩短输入"
            else:
                return f"❌ OpenAI API错误: {error_msg[:150]}"
    
    def _chat_completion_via_requests(self, messages: List[Dict], kwargs: Dict) -> str:
        """通过requests调用OpenAI API"""
        import requests
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        
        data = {
            "model": self.name,
            "messages": messages,
            "temperature": kwargs.get('temperature', self.temperature),
            "max_tokens": kwargs.get('max_tokens', self.max_tokens),
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # 记录使用情况
                if 'usage' in result:
                    self._log_usage(result['usage'])
                
                return content
            else:
                return "❌ OpenAI API返回格式异常"
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "🔑 OpenAI API密钥无效"
            elif e.response.status_code == 429:
                return "🚫 OpenAI请求频率超限"
            elif e.response.status_code == 500:
                return "⚙️ OpenAI服务器内部错误"
            else:
                try:
                    error_detail = e.response.json().get('error', {}).get('message', '未知错误')
                    return f"❌ OpenAI错误: {error_detail}"
                except:
                    return f"❌ OpenAI HTTP错误 {e.response.status_code}"
        except requests.exceptions.Timeout:
            return "⏱️ OpenAI请求超时"
        except requests.exceptions.ConnectionError:
            return "🔌 网络连接失败，无法访问OpenAI"
        except Exception as e:
            return f"❌ OpenAI请求失败: {str(e)[:100]}"
    
    def _log_usage(self, usage: Dict):
        """记录API使用情况"""
        try:
            # 简单记录到控制台
            tokens = usage.get('total_tokens', 0)
            print(f"📊 OpenAI API使用: {tokens} tokens")
        except:
            pass
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        prompt = f"请用中文解释这个shell命令的功能和用法: {command}"
        if context:
            prompt += f"\n上下文: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个Linux/Unix系统专家，专门用中文解释shell命令。回答要简洁明了，包含实际用例。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令"""
        prompt = "请推荐一些有用的shell命令"
        if context:
            prompt += f"，相关于: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个经验丰富的系统管理员，请用中文推荐实用、安全的shell命令。每个命令用反引号`包围，后面跟简短描述。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages)
        
        # 解析响应为命令列表
        commands = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('`' in line or line.startswith('- ') or line.startswith('• ')):
                # 提取命令和描述
                import re
                cmd_match = re.search(r'`([^`]+)`', line)
                if cmd_match:
                    command = cmd_match.group(1)
                    description = re.sub(r'`[^`]+`', '', line).strip(' -•')
                    commands.append({
                        "command": command,
                        "description": description or "有用的shell命令"
                    })
                elif line.startswith('- ') or line.startswith('• '):
                    # 处理无反引号的格式
                    parts = line[2:].split(':', 1)
                    if len(parts) == 2:
                        commands.append({
                            "command": parts[0].strip(),
                            "description": parts[1].strip()
                        })
        
        return commands[:5] if commands else [
            {"command": "ls -la", "description": "列出详细文件信息"},
            {"command": "ps aux", "description": "查看所有进程"},
            {"command": "df -h", "description": "查看磁盘使用情况"},
            {"command": "grep pattern file", "description": "在文件中搜索文本"},
            {"command": "find . -name '*.py'", "description": "查找Python文件"},
        ]