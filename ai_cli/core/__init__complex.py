"""
AI-CLI 核心模块

提供AI集成、配置管理、上下文跟踪等核心功能。
"""

__version__ = "0.1.0"
__author__ = "AI-CLI Team"
__license__ = "MIT"

from .config import get_config, save_config, update_config
from .ai import AIProvider, get_ai_provider, explain_command, suggest_command
from .context import ContextManager, get_context
from .plugins import Plugin, PluginManager, get_plugin_manager
from .performance import PerformanceMonitor, measure_performance, cache_result
from .learning import LearningManager, learn_from_interaction
from .dynamic_commands import DynamicCommandManager, register_dynamic_command

# 导出核心功能
__all__ = [
    # 配置
    "get_config",
    "save_config", 
    "update_config",
    
    # AI功能
    "AIProvider",
    "get_ai_provider",
    "explain_command",
    "suggest_command",
    
    # 上下文管理
    "ContextManager",
    "get_context",
    
    # 插件系统
    "Plugin",
    "PluginManager",
    "get_plugin_manager",
    
    # 性能监控
    "PerformanceMonitor",
    "measure_performance",
    "cache_result",
    
    # 学习系统
    "LearningManager",
    "learn_from_interaction",
    
    # 动态命令
    "DynamicCommandManager",
    "register_dynamic_command",
]

# 初始化检查
def check_dependencies():
    """检查依赖是否可用"""
    import sys
    missing = []
    
    required = ["click", "rich", "yaml"]
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"警告：缺少依赖: {', '.join(missing)}")
        print("运行: pip install -r requirements.txt")
        return False
    
    return True

# 自动检查
if __name__ == "__main__":
    check_dependencies()