"""
符灵 (Fú Líng) - 智能命令行助手
古代符咒之灵，现代AI智能
"""

__version__ = "0.1.0"
__author__ = "符灵开发者"
__description__ = "符灵 (Fú Líng) - 智能命令行助手"

from .fuling_core import config, get_config, get_model_config
from .fuling_ai import (
    explain_command, 
    chat_completion, 
    test_ai_connection,
    get_ai_provider,
)
from .fuling_theme import (
    get_theme,
    format_text,
    show_banner,
)

# 导出主CLI
try:
    from .fuling_cli_enhanced import cli, main
except ImportError:
    from .fuling_cli import cli, main

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__description__",
    
    # 核心模块
    "config",
    "get_config",
    "get_model_config",
    
    # AI模块
    "explain_command",
    "chat_completion",
    "test_ai_connection",
    "get_ai_provider",
    
    # 主题模块
    "get_theme",
    "format_text",
    "show_banner",
    
    # CLI
    "cli",
    "main",
]