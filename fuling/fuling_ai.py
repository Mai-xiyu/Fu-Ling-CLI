"""
符灵AI模块 - 集成多AI提供商
"""

import os
import json
from typing import Dict, Any, List, Optional
from .fuling_core import get_model_config

class AIProvider:
    """AI提供商基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', 'unknown')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 1000)
        self.timeout = config.get('timeout', 30)
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """聊天补全"""
        raise NotImplementedError
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        raise NotImplementedError

class MoonshotProvider(AIProvider):
    """Moonshot AI (Kimi) 提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key') or os.environ.get('MOONSHOT_API_KEY')
        self.base_url = config.get('base_url', 'https://api.moonshot.cn/v1')
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """Moonshot聊天补全"""
        import requests
        
        if not self.api_key:
            return "❌ 未设置Moonshot API密钥。请设置环境变量: export MOONSHOT_API_KEY='your_key'"
        
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
            
        except requests.exceptions.Timeout:
            return "⏱️ 请求超时，请检查网络连接"
        except requests.exceptions.ConnectionError:
            return "🔌 网络连接失败，请检查网络"
        except Exception as e:
            return f"❌ Moonshot API错误: {str(e)[:100]}"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令"""
        prompt = f"解释这个shell命令的功能和用法: {command}"
        if context:
            prompt += f"\n上下文: {context}"
        
        messages = [
            {"role": "system", "content": "你是一个Linux/Unix系统专家，专门解释shell命令。用中文回答。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)

class LocalProvider(AIProvider):
    """本地回退提供商"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.command_db = self._load_command_database()
    
    def _load_command_database(self) -> Dict:
        """加载本地命令数据库"""
        return {
            "ls -la": "天眼符：列出当前目录所有文件和目录的详细信息，包括隐藏文件",
            "cd": "移形符：切换当前工作目录",
            "pwd": "定位符：显示当前所在目录的完整路径",
            "mkdir": "创界符：创建新的目录",
            "rm": "湮灭符：删除文件或目录",
            "cp": "复制符：复制文件或目录到指定位置",
            "mv": "移物符：移动文件或目录，或重命名",
            "cat": "显形符：显示文件内容",
            "grep": "寻迹符：在文件中搜索匹配模式的文本行",
            "find": "探宝符：在目录树中查找文件",
            "ps aux": "观灵符：显示所有运行中的进程信息",
            "kill": "驱散符：终止指定进程",
            "chmod": "改权符：更改文件或目录的权限",
            "chown": "易主符：更改文件或目录的所有者",
            "tar": "封印符：将多个文件打包或解包",
            "ssh": "通灵符：安全连接到远程服务器",
            "scp": "传物符：安全地在本地和远程之间复制文件",
            "wget": "下载符：从网络下载文件",
            "curl": "通联符：与网络服务器传输数据",
            "git": "时光符：版本控制系统，记录代码历史",
            "docker": "容器符：容器化应用程序管理",
            "kubectl": "统御符：Kubernetes集群管理",
        }
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """本地聊天补全"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "解释" in last_message or "explain" in last_message.lower():
            # 尝试提取命令
            import re
            cmd_match = re.search(r'`([^`]+)`', last_message)
            if cmd_match:
                command = cmd_match.group(1)
                return self.explain_command(command)
        
        return "🔮 符灵本地模式：请设置AI提供商API密钥以使用完整功能。\n设置示例: export MOONSHOT_API_KEY='your_key'"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        """解释命令（本地数据库）"""
        explanation = self.command_db.get(command.strip())
        
        if explanation:
            return f"📜 {explanation}"
        else:
            # 尝试匹配部分命令
            for cmd, desc in self.command_db.items():
                if command in cmd or cmd in command:
                    return f"📜 {desc}"
            
            return f"💭 此符咒 '{command}' 含义深奥，本地知识库中未找到详细解释。\n💡 请设置API密钥以获取AI解读。"

def get_ai_provider() -> AIProvider:
    """获取AI提供商实例"""
    model_config = get_model_config()
    provider_name = model_config.get('provider', 'local').lower()
    
    providers = {
        'moonshot': MoonshotProvider,
        'openai': MoonshotProvider,  # 暂时使用Moonshot兼容
        'local': LocalProvider,
    }
    
    provider_class = providers.get(provider_name, LocalProvider)
    
    try:
        return provider_class(model_config)
    except Exception as e:
        print(f"⚠️ {provider_name} 提供商初始化失败: {e}")
        print("🔮 回退到本地模式")
        return LocalProvider(model_config)

# 导出函数
def explain_command(command: str, context: str = None) -> str:
    """解释shell命令"""
    try:
        provider = get_ai_provider()
        return provider.explain_command(command, context)
    except Exception as e:
        return f"❌ 解释命令失败: {e}"

def chat_completion(messages: List[Dict], **kwargs) -> str:
    """通用聊天补全"""
    try:
        provider = get_ai_provider()
        return provider.chat_completion(messages, **kwargs)
    except Exception as e:
        return f"❌ 聊天失败: {e}"

def test_ai_connection() -> Dict[str, Any]:
    """测试AI连接"""
    provider = get_ai_provider()
    provider_name = provider.__class__.__name__.replace('Provider', '')
    
    # 简单测试
    test_command = "ls -la"
    result = provider.explain_command(test_command)
    
    return {
        "provider": provider_name,
        "connected": "✅ 已连接" if "❌" not in result and "⚠️" not in result else "❌ 未连接",
        "test_result": result[:100] + "..." if len(result) > 100 else result,
    }