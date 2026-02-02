"""
符灵主题系统
"""

from typing import Dict, Any
from .fuling_core import get_config

class Theme:
    """主题基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.colors = config.get('colors', {})
        self.symbols = config.get('symbols', {})
    
    def format_text(self, text: str, style: str = None) -> str:
        """格式化文本"""
        # 基础实现，可扩展为彩色输出
        return text
    
    def get_symbol(self, symbol_type: str) -> str:
        """获取符号"""
        return self.symbols.get(symbol_type, "•")
    
    def get_banner(self) -> str:
        """获取横幅"""
        raise NotImplementedError

class AncientTheme(Theme):
    """古风主题"""
    
    def get_banner(self) -> str:
        return """
    ┌─────────────────────────────────────┐
    │    ██▓▓▓▓██                         │
    │    ▓▓    ▓▓    符灵 v0.1.0          │
    │    ▓▓  ██▓▓    智能命令行助手       │
    │    ▓▓▓▓██▓▓                         │
    │    ▓▓  ▓▓▓▓    古代智慧 · 现代AI    │
    │    ██▓▓▓▓██                         │
    └─────────────────────────────────────┘
    """
    
    def format_text(self, text: str, style: str = None) -> str:
        symbols = {
            'prompt': '🔮',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': '💡',
            'command': '📜',
            'code': '📝',
            'system': '💻',
            'network': '🌐',
            'file': '📁',
        }
        
        if style in symbols:
            return f"{symbols[style]} {text}"
        return text

class ModernTheme(Theme):
    """现代主题"""
    
    def get_banner(self) -> str:
        return """
    ╔═════════════════════════════════════╗
    ║           符灵 v0.1.0               ║
    ║       Intelligent CLI Assistant     ║
    ╚═════════════════════════════════════╝
    """
    
    def format_text(self, text: str, style: str = None) -> str:
        symbols = {
            'prompt': '❯',
            'success': '✓',
            'error': '✗',
            'warning': '!',
            'info': 'i',
            'command': '>',
            'code': '</>',
            'system': '⚙',
            'network': '↻',
            'file': '📄',
        }
        
        if style in symbols:
            return f"[{symbols[style]}] {text}"
        return text

class DarkTheme(Theme):
    """暗黑主题"""
    
    def get_banner(self) -> str:
        return """
    ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
    ▓▒░     符灵     ░▒▓
    ░▒▓█▓▒░v0.1.0░▒▓█▓▒░
    """
    
    def format_text(self, text: str, style: str = None) -> str:
        symbols = {
            'prompt': '👁',
            'success': '✔',
            'error': '✘',
            'warning': '⚡',
            'info': '🔍',
            'command': '⚔',
            'code': '🔮',
            'system': '💀',
            'network': '🕸',
            'file': '📜',
        }
        
        if style in symbols:
            return f"{symbols[style]} {text}"
        return text

class LightTheme(Theme):
    """明亮主题"""
    
    def get_banner(self) -> str:
        return """
    ╭─────────────────────────────────────╮
    │    ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○    │
    │    ○       符灵 v0.1.0        ○    │
    │    ○   智能命令行助手         ○    │
    │    ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○    │
    ╰─────────────────────────────────────╯
    """
    
    def format_text(self, text: str, style: str = None) -> str:
        symbols = {
            'prompt': '→',
            'success': '✓',
            'error': '✗',
            'warning': '⚠',
            'info': 'ℹ',
            'command': '$',
            'code': '{ }',
            'system': '🖥',
            'network': '📡',
            'file': '📎',
        }
        
        if style in symbols:
            return f"{symbols[style]} {text}"
        return text

def get_theme() -> Theme:
    """获取当前主题"""
    config = get_config()
    theme_config = config.get('theme', {})
    theme_name = theme_config.get('name', 'ancient')
    
    themes = {
        'ancient': AncientTheme,
        'modern': ModernTheme,
        'dark': DarkTheme,
        'light': LightTheme,
    }
    
    theme_class = themes.get(theme_name, AncientTheme)
    return theme_class(theme_name, theme_config)

def format_text(text: str, style: str = None) -> str:
    """格式化文本（快捷函数）"""
    theme = get_theme()
    return theme.format_text(text, style)

def show_banner() -> None:
    """显示横幅"""
    theme = get_theme()
    print(theme.get_banner())

# 导出
__all__ = [
    'Theme',
    'AncientTheme',
    'ModernTheme',
    'DarkTheme',
    'LightTheme',
    'get_theme',
    'format_text',
    'show_banner',
]