"""
多AI提供商支持
支持: Moonshot (Kimi), OpenAI, Anthropic, Ollama, 本地回退
"""

import os
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """AI提供商基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'unknown')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 1000)
        self.timeout = config.get('timeout', 30)
    
    @abstractmethod
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """聊天补全"""
        pass
    
    @abstractmethod
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        pass
    
    @abstractmethod
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令"""
        pass

class MoonshotProvider(AIProvider):
    """Moonshot AI (Kimi) 提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key') or os.environ.get('MOONSHOT_API_KEY')
        self.base_url = config.get('base_url', 'https://api.moonshot.cn/v1')
        
        if not self.api_key:
            raise ValueError("Moonshot API密钥未设置")
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """Moonshot聊天补全"""
        import requests
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
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
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Moonshot API错误: {e}"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        prompt = f"解释这个shell命令的功能和用法: {command}"
        if context:
            prompt += f"\n上下文: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个Linux/Unix系统专家，专门解释shell命令。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令"""
        prompt = "建议一些有用的shell命令"
        if context:
            prompt += f" 相关于: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个经验丰富的系统管理员，提供实用、安全的shell命令建议。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages)
        
        # 解析响应为命令列表
        commands = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('`' in line or '$' in line or line.startswith('- ')):
                # 提取命令和描述
                import re
                cmd_match = re.search(r'`([^`]+)`', line)
                if cmd_match:
                    command = cmd_match.group(1)
                    description = line.replace(f'`{command}`', '').strip(' -')
                    commands.append({
                        "command": command,
                        "description": description or "有用的shell命令"
                    })
        
        return commands[:5]  # 返回前5个

class OpenAIProvider(AIProvider):
    """OpenAI 提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
        self.base_url = config.get('base_url', 'https://api.openai.com/v1')
        
        if not self.api_key:
            raise ValueError("OpenAI API密钥未设置")
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """OpenAI聊天补全"""
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            response = client.chat.completions.create(
                model=self.name,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "错误: 未安装openai库，运行: pip install openai"
        except Exception as e:
            return f"OpenAI API错误: {e}"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        prompt = f"Explain this shell command: {command}"
        if context:
            prompt += f"\nContext: {context}"
        
        messages = [
            {"role": "system", "content": "You are a Linux/Unix system expert specializing in explaining shell commands."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令"""
        # 使用OpenAI的通用实现
        return MoonshotProvider.suggest_commands(self, context)

class OllamaProvider(AIProvider):
    """Ollama 本地AI提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """Ollama聊天补全"""
        import requests
        
        url = f"{self.base_url}/api/chat"
        
        # 转换消息格式
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        data = {
            "model": self.name,
            "messages": ollama_messages,
            "options": {
                "temperature": kwargs.get('temperature', self.temperature),
                "num_predict": kwargs.get('max_tokens', self.max_tokens),
            }
        }
        
        try:
            response = requests.post(
                url,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result['message']['content']
            
        except Exception as e:
            return f"Ollama API错误: {e} (确保Ollama服务正在运行: ollama serve)"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        prompt = f"解释这个shell命令: {command}"
        if context:
            prompt += f"\n上下文: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个Linux系统专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令"""
        # 基础实现
        return [
            {"command": "ls -la", "description": "列出详细文件信息"},
            {"command": "pwd", "description": "显示当前目录"},
            {"command": "history", "description": "查看命令历史"},
        ]

class LocalProvider(AIProvider):
    """本地回退提供商（无网络依赖）"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.command_db = self._load_command_database()
    
    def _load_command_database(self) -> Dict:
        """加载本地命令数据库"""
        return {
            "ls -la": "列出当前目录所有文件和目录的详细信息，包括隐藏文件",
            "cd": "切换目录",
            "pwd": "打印当前工作目录",
            "mkdir": "创建新目录",
            "rm": "删除文件或目录",
            "cp": "复制文件或目录",
            "mv": "移动或重命名文件",
            "cat": "显示文件内容",
            "grep": "在文件中搜索文本",
            "find": "查找文件",
            "ps aux": "显示所有运行中的进程",
            "kill": "终止进程",
            "chmod": "更改文件权限",
            "chown": "更改文件所有者",
            "tar": "归档文件",
            "ssh": "安全shell连接",
            "scp": "安全复制文件",
            "wget": "下载文件",
            "curl":传输数据",
            "git": "版本控制",
        }
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """本地聊天补全（简单回退）"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "解释" in last_message or "explain" in last_message.lower():
            # 尝试提取命令
            import re
            cmd_match = re.search(r'`([^`]+)`', last_message)
            if cmd_match:
                command = cmd_match.group(1)
                return self.explain_command(command)
        
        return "本地模式: 请设置AI提供商API密钥以使用完整功能。"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令（本地数据库）"""
        explanation = self.command_db.get(command.strip())
        
        if explanation:
            return f"{command}: {explanation}"
        else:
            # 尝试匹配部分命令
            for cmd, desc in self.command_db.items():
                if command in cmd or cmd in command:
                    return f"{cmd}: {desc}"
            
            return f"本地知识库中没有找到命令 '{command}' 的详细解释。"
    
    def suggest_commands(self, context: Optional[str] = None) -> List[Dict]:
        """建议命令（本地数据库）"""
        suggestions = []
        
        for cmd, desc in self.command_db.items():
            suggestions.append({
                "command": cmd,
                "description": desc
            })
        
        return suggestions[:10]

def get_ai_provider(config: Optional[Dict] = None) -> AIProvider:
    """获取AI提供商实例"""
    if config is None:
        from .config import get_config
        config = get_config()
    
    model_config = config.get('model', {})
    provider_name = model_config.get('provider', 'local')
    
    providers = {
        'moonshot': MoonshotProvider,
        'openai': OpenAIProvider,
        'anthropic': OpenAIProvider,  # 暂时使用OpenAI兼容
        'ollama': OllamaProvider,
        'local': LocalProvider,
    }
    
    provider_class = providers.get(provider_name.lower(), LocalProvider)
    
    try:
        return provider_class(model_config)
    except Exception as e:
        print(f"警告: {provider_name} 提供商初始化失败: {e}")
        print("回退到本地模式")
        return LocalProvider(model_config)

# 导出
__all__ = [
    'AIProvider',
    'MoonshotProvider',
    'OpenAIProvider',
    'OllamaProvider',
    'LocalProvider',
    'get_ai_provider',
]