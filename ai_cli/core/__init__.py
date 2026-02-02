"""
AI-CLI 核心模块
简化版本，避免导入错误
"""

__version__ = "0.1.0"
__author__ = "AI-CLI Team"
__license__ = "MIT"

# 延迟导入，避免循环依赖
def get_config():
    from .config import get_config as _get_config
    return _get_config()

def save_config(config):
    from .config import save_config as _save_config
    return _save_config(config)

def get_ai_provider(config=None):
    from .ai import get_ai_provider as _get_ai_provider
    return _get_ai_provider(config)

def explain_command(command, context=None):
    from .ai import explain_command as _explain_command
    return _explain_command(command, context)

def suggest_command(context=None):
    from .ai import suggest_command as _suggest_command
    return _suggest_command(context)

def get_context():
    from .context import get_context as _get_context
    return _get_context()

def get_plugin_manager():
    from .plugins import get_plugin_manager as _get_plugin_manager
    return _get_plugin_manager()

def measure_performance(func):
    from .performance import measure_performance as _measure_performance
    return _measure_performance(func)

def cache_result(ttl=300):
    from .performance import cache_result as _cache_result
    return _cache_result(ttl)

# 导出核心功能
__all__ = [
    "get_config",
    "save_config", 
    "get_ai_provider",
    "explain_command",
    "suggest_command",
    "get_context",
    "get_plugin_manager",
    "measure_performance",
    "cache_result",
]