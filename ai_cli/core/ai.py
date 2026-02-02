"""
AI集成模块 - 使用新的多提供商系统
"""

from .ai_providers import get_ai_provider, AIProvider

class AIError(Exception):
    """AI模型相关错误"""
    pass

def explain_command(command: str, context: str = None) -> str:
    """解释shell命令"""
    try:
        provider = get_ai_provider()
        return provider.explain_command(command, context)
    except Exception as e:
        raise AIError(f"解释命令失败: {e}")

def suggest_commands(context: str = None) -> list:
    """建议相关命令"""
    try:
        provider = get_ai_provider()
        return provider.suggest_commands(context)
    except Exception as e:
        raise AIError(f"建议命令失败: {e}")

def chat_completion(messages: list, **kwargs) -> str:
    """通用聊天补全"""
    try:
        provider = get_ai_provider()
        return provider.chat_completion(messages, **kwargs)
    except Exception as e:
        raise AIError(f"聊天补全失败: {e}")

def test_model_connection() -> bool:
    """测试AI模型连接"""
    try:
        provider = get_ai_provider()
        
        # 简单测试
        test_result = provider.explain_command("ls -la")
        return bool(test_result and len(test_result.strip()) > 0)
        
    except Exception:
        return False

# 向后兼容
def get_ai_provider_instance(config=None):
    """获取AI提供商实例（兼容旧代码）"""
    return get_ai_provider(config)

# 导出
__all__ = [
    'AIError',
    'explain_command',
    'suggest_commands',
    'chat_completion',
    'test_model_connection',
    'get_ai_provider',
    'get_ai_provider_instance',
]