"""
AI-CLI 工具模块
简化版本
"""

__all__ = [
    "AIError",
    "ConfigError",
    "CommandError",
    "SafetyError",
    "format_error",
    "handle_error",
]

# 延迟导入
def __getattr__(name):
    if name in __all__:
        from .errors import (
            AIError,
            ConfigError,
            CommandError,
            SafetyError,
            format_error,
            handle_error,
        )
        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")