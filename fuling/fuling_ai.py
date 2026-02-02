"""
符灵AI模块 - 集成多AI提供商
"""

import os
import json
from typing import Dict, Any, List, Optional
from .fuling_core import get_model_config

# OpenAIProvider在get_ai_provider中动态导入以避免依赖

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
            "stream": False,
        }
        
        # 添加可选的top_p参数
        if 'top_p' in kwargs:
            data['top_p'] = kwargs['top_p']
        
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
                
                # 记录使用情况（可选）
                if 'usage' in result:
                    usage = result['usage']
                    self._log_usage(usage)
                
                return content
            else:
                return "❌ API返回格式异常，未找到有效回复"
            
        except requests.exceptions.Timeout:
            return "⏱️ 请求超时，请检查网络连接或增加超时时间"
        except requests.exceptions.ConnectionError:
            return "🔌 网络连接失败，请检查网络连接"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "🔑 API密钥无效，请检查MOONSHOT_API_KEY"
            elif e.response.status_code == 429:
                return "🚫 请求过于频繁，请稍后重试"
            elif e.response.status_code == 500:
                return "⚙️ 服务器内部错误，请稍后重试"
            else:
                return f"❌ HTTP错误 {e.response.status_code}: {e.response.text[:200]}"
        except Exception as e:
            return f"❌ Moonshot API错误: {str(e)[:150]}"
    
    def _log_usage(self, usage: Dict):
        """记录API使用情况（可选）"""
        try:
            # 可以在这里实现使用情况记录
            # 例如：保存到文件、数据库或发送到监控系统
            pass
        except:
            # 静默失败，不影响主要功能
            pass
    
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
        self.code_templates = self._load_code_templates()
    
    def _load_command_database(self) -> Dict:
        """加载本地命令数据库"""
        return {
            # 基础命令
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
            
            # 系统命令
            "ps aux": "观灵符：显示所有运行中的进程信息",
            "kill": "驱散符：终止指定进程",
            "top": "观天符：实时显示系统进程和资源使用",
            "htop": "观天符（增强）：交互式系统监控",
            "df -h": "量地符：查看磁盘使用情况（人类可读格式）",
            "du -sh": "测容符：查看目录大小",
            "free -h": "查灵符：查看内存使用情况",
            
            # 权限命令
            "chmod": "改权符：更改文件或目录的权限",
            "chown": "易主符：更改文件或目录的所有者",
            "sudo": "升权符：以超级用户权限执行命令",
            
            # 网络命令
            "ping": "探网符：测试网络连接",
            "curl": "通联符：与网络服务器传输数据",
            "wget": "下载符：从网络下载文件",
            "ssh": "通灵符：安全连接到远程服务器",
            "scp": "传物符：安全地在本地和远程之间复制文件",
            "netstat": "观网符：显示网络连接、路由表等",
            
            # 开发命令
            "git": "时光符：版本控制系统，记录代码历史",
            "docker": "容器符：容器化应用程序管理",
            "kubectl": "统御符：Kubernetes集群管理",
            "python": "灵蛇符：Python解释器",
            "node": "节点符：Node.js运行时",
            "npm": "包管符：Node.js包管理器",
            
            # 文本处理
            "awk": "炼文符：文本处理和数据提取",
            "sed": "改文符：流编辑器，文本替换和转换",
            "sort": "排序符：对文本行进行排序",
            "uniq": "去重符：去除重复的文本行",
            "wc": "计数符：统计行数、单词数、字符数",
            
            # 压缩归档
            "tar": "封印符：将多个文件打包或解包",
            "gzip": "压缩符：文件压缩",
            "zip": "打包符：创建ZIP压缩包",
            "unzip": "解包符：解压ZIP文件",
            
            # 其他实用命令
            "history": "忆往符：查看命令历史",
            "alias": "化名符：创建命令别名",
            "export": "设境符：设置环境变量",
            "source": "引源符：执行脚本文件",
            "man": "天书符：查看命令手册",
            "which": "寻踪符：查找命令位置",
        }
    
    def _load_code_templates(self) -> Dict:
        """加载代码模板"""
        return {
            "python_function": """def {function_name}({parameters}):
    \"\"\"{description}\"\"\"
    {body}
    return result""",
            
            "python_class": """class {class_name}:
    \"\"\"{description}\"\"\"
    
    def __init__(self{init_params}):
        {init_body}
    
    def {method_name}(self{method_params}):
        \"\"\"{method_description}\"\"\"
        {method_body}
        return result""",
            
            "bash_script": """#!/bin/bash
# {description}

{code_body}

echo "完成！\"""",
            
            "sql_table": """CREATE TABLE {table_name} (
    id INT PRIMARY KEY AUTO_INCREMENT,
    {columns}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);""",
            
            "dockerfile": """FROM {base_image}
WORKDIR /app
COPY . .
RUN {build_commands}
CMD {run_command}""",
        }
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        """本地聊天补全"""
        if not messages:
            return "🔮 符灵本地模式：请输入消息与我对话。"
        
        last_message = messages[-1]["content"]
        all_messages = " ".join([msg["content"] for msg in messages])
        
        # 检测命令解释请求
        if any(keyword in last_message.lower() for keyword in ["解释", "explain", "what is", "how to use"]):
            import re
            # 尝试提取命令
            cmd_match = re.search(r'`([^`]+)`', last_message)
            if cmd_match:
                command = cmd_match.group(1)
                return self.explain_command(command)
            else:
                # 尝试从文本中提取命令
                words = last_message.split()
                for word in words:
                    if word in self.command_db:
                        return self.explain_command(word)
        
        # 检测代码生成请求
        if any(keyword in last_message.lower() for keyword in ["生成", "generate", "create", "write code", "python", "function"]):
            return self._generate_code_response(last_message)
        
        # 检测命令建议请求
        if any(keyword in last_message.lower() for keyword in ["建议", "suggest", "推荐", "command", "什么命令"]):
            return self._suggest_commands_response(last_message)
        
        # 默认响应
        responses = [
            "🔮 符灵本地模式：我可以解释shell命令、生成简单代码、推荐实用命令。",
            "💡 请设置AI提供商API密钥以使用完整智能对话功能。",
            "📝 示例命令: fl explain 'ls -la'",
            "🚀 设置API密钥: export MOONSHOT_API_KEY='your_key' 或 export OPENAI_API_KEY='your_key'",
            "🎯 当前支持: Moonshot (Kimi), OpenAI, 本地回退模式",
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_code_response(self, prompt: str) -> str:
        """生成代码响应"""
        import random
        
        templates = [
            "📝 本地模式代码生成示例：",
            "```python\ndef hello_world():\n    print('Hello, 符灵!')\n    return '代码生成完成'\n```",
            "💡 设置API密钥以获取智能代码生成：export MOONSHOT_API_KEY='your_key'",
            "🚀 使用示例: fl generate 'python快速排序算法' -l python",
        ]
        
        # 如果是具体的代码请求，尝试提供模板
        if "python" in prompt.lower():
            return "```python\n# Python函数示例\ndef example_function(param1, param2):\n    \"\"\"函数说明\"\"\"\n    result = param1 + param2\n    return result\n\n# 调用示例\nprint(example_function(10, 20))\n```\n\n💡 设置API密钥获取更智能的代码生成。"
        elif "bash" in prompt.lower() or "shell" in prompt.lower():
            return "```bash\n#!/bin/bash\n# Shell脚本示例\necho '开始执行...'\nls -la\ndate\necho '执行完成！'\n```"
        elif "sql" in prompt.lower():
            return "```sql\n-- SQL表示例\nCREATE TABLE users (\n    id INT PRIMARY KEY AUTO_INCREMENT,\n    username VARCHAR(50) NOT NULL,\n    email VARCHAR(100) UNIQUE,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);\n\n-- 插入数据\nINSERT INTO users (username, email) VALUES ('符灵', 'fuling@example.com');\n```"
        
        return random.choice(templates)
    
    def _suggest_commands_response(self, prompt: str) -> str:
        """建议命令响应"""
        import random
        
        # 根据上下文推荐命令
        context = prompt.lower()
        suggestions = []
        
        if any(word in context for word in ["文件", "file", "目录", "folder"]):
            suggestions.extend(["ls -la", "find . -name '*.txt'", "du -sh *", "file filename"])
        
        if any(word in context for word in ["进程", "process", "运行", "running"]):
            suggestions.extend(["ps aux", "top", "htop", "kill PID"])
        
        if any(word in context for word in ["网络", "network", "连接", "connect"]):
            suggestions.extend(["ping google.com", "curl -I example.com", "netstat -tulpn", "ssh user@host"])
        
        if any(word in context for word in ["系统", "system", "状态", "status"]):
            suggestions.extend(["df -h", "free -h", "uptime", "uname -a"])
        
        if not suggestions:
            # 默认推荐
            suggestions = ["ls -la", "grep pattern file", "find . -type f", "ps aux | grep python", "df -h"]
        
        # 随机选择3个
        selected = random.sample(suggestions, min(3, len(suggestions)))
        
        response = "🔍 推荐命令：\n"
        for cmd in selected:
            explanation = self.command_db.get(cmd, "实用命令")
            response += f"  • `{cmd}` - {explanation}\n"
        
        response += "\n💡 使用: fl explain '命令' 获取详细解释"
        return response
    
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
    
    # 基础提供商映射
    base_providers = {
        'moonshot': MoonshotProvider,
        'local': LocalProvider,
    }
    
    # 处理OpenAI提供商（动态导入）
    if provider_name == 'openai':
        try:
            from .openai_provider import OpenAIProvider
            provider_class = OpenAIProvider
        except ImportError:
            print("⚠️ OpenAIProvider导入失败，回退到本地模式")
            provider_class = LocalProvider
    
    # 处理DeepSeek提供商（动态导入）
    elif provider_name == 'deepseek':
        try:
            from .deepseek_provider import DeepSeekProvider
            provider_class = DeepSeekProvider
        except ImportError:
            print("⚠️ DeepSeekProvider导入失败，回退到本地模式")
            provider_class = LocalProvider
    
    else:
        provider_class = base_providers.get(provider_name, LocalProvider)
    
    try:
        provider = provider_class(model_config)
        
        # 测试提供商是否可用
        if provider_name != 'local':
            # 简单测试连接
            test_result = provider.explain_command("pwd")
            if "❌" in test_result or "🔑" in test_result or "🚫" in test_result:
                print(f"⚠️ {provider_name} 提供商测试失败: {test_result[:100]}")
                print("🔮 回退到本地模式")
                return LocalProvider(model_config)
        
        return provider
        
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