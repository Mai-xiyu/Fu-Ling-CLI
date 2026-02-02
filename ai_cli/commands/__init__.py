"""
AI-CLI 命令模块
"""

# 导出所有命令
from .chat import chat
from .explain import explain
from .find import find
from .grep import grep
from .history import history
from .suggest import suggest

# 其他命令延迟导入
def get_command(name):
    """动态获取命令"""
    if name == "init":
        from .init import init
        return init
    elif name == "config":
        from .config import config
        return config
    elif name == "status":
        from .status import status
        return status
    elif name == "learn":
        from .learn import learn
        return learn
    elif name == "interactive":
        from .interactive import interactive
        return interactive
    else:
        raise ImportError(f"Command {name} not found")

__all__ = [
    "chat",
    "explain", 
    "find",
    "grep",
    "history",
    "suggest",
    "get_command",
]