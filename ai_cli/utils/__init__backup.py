"""
AI-CLI 工具模块

提供错误处理、日志记录、格式化输出等实用工具。
"""

__all__ = [
    "AIError",
    "ConfigError",
    "PluginError",
    "format_output",
    "log_debug",
    "log_info",
    "log_warning",
    "log_error",
    "progress_bar",
    "spinner",
    "confirm",
    "select_option",
]

from .errors import (
    AIError,
    ConfigError,
    CommandError,
    SafetyError,
)

from .logging import (
    setup_logging,
    log_debug,
    log_info,
    log_warning,
    log_error,
    get_logger,
)

from .formatters import (
    format_output,
    format_table,
    format_json,
    format_yaml,
    format_markdown,
)

from .ui import (
    progress_bar,
    spinner,
    confirm,
    select_option,
    input_with_default,
    print_success,
    print_error,
    print_warning,
    print_info,
)

from .validators import (
    validate_api_key,
    validate_config_file,
    validate_plugin,
    validate_command,
)

# 工具函数
def get_version():
    """获取版本信息"""
    from .. import __version__
    return __version__

def get_system_info():
    """获取系统信息"""
    import platform
    import sys
    
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

def check_environment():
    """检查运行环境"""
    import os
    import sys
    
    info = {
        "python_executable": sys.executable,
        "working_directory": os.getcwd(),
        "user_home": os.path.expanduser("~"),
        "environment_variables": {
            "PATH": os.getenv("PATH", ""),
            "PYTHONPATH": os.getenv("PYTHONPATH", ""),
            "VIRTUAL_ENV": os.getenv("VIRTUAL_ENV", ""),
        }
    }
    
    return info

# 初始化日志
try:
    setup_logging()
except:
    pass  # 静默失败，使用默认日志