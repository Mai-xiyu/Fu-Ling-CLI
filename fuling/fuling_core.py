"""
符灵核心模块 - 集成多AI提供商
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class FulingConfig:
    """符灵配置管理"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "fuling"
        self.config_file = self.config_dir / "config.yaml"
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        if self._config is not None:
            return self._config
        
        if not self.config_file.exists():
            # 返回默认配置
            return self.get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"⚠️ 读取配置失败: {e}")
            self._config = self.get_default_config()
        
        return self._config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """保存配置"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            self._config = config
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "fuling": {
                "name": "符灵",
                "version": "0.1.0",
                "theme": "ancient",
                "language": "zh",  # zh | en
            },
            "model": {
                "provider": "moonshot",  # moonshot | openai | local
                "name": "kimi-k2-turbo-preview",  # 模型名称
                "api_key": "${MOONSHOT_API_KEY}",  # 环境变量
                "base_url": "https://api.moonshot.cn/v1",
                "organization": "",  # OpenAI组织ID
                "temperature": 0.3,
                "max_tokens": 1000,
                "timeout": 30,
                "retry_attempts": 3,
                "retry_delay": 2,
            },
            "features": {
                "auto_suggest": True,
                "explain_commands": True,
                "learn_patterns": True,
                "enable_cache": True,
                "show_banner": True,
                "log_usage": False,
                "save_history": True,
                "max_history": 100,
            },
            "theme": {
                "name": "ancient",  # ancient | modern | dark | light
                "colors": {
                    "primary": "#1a237e",
                    "accent": "#ffd700",
                    "text": "#ffffff",
                    "success": "#4caf50",
                    "warning": "#ff9800",
                    "error": "#f44336",
                    "info": "#2196f3",
                },
                "symbols": {
                    "prompt": "🔮",
                    "success": "✅",
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "💡",
                    "command": "📜",
                    "code": "📝",
                    "system": "💻",
                    "network": "🌐",
                }
            },
            "paths": {
                "config_dir": "~/.config/fuling",
                "cache_dir": "~/.cache/fuling",
                "log_dir": "~/.local/share/fuling/logs",
                "plugin_dir": "~/.config/fuling/plugins",
            }
        }
    
    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        config = self.load_config()
        model_config = config.get("model", {})
        
        # 替换环境变量
        api_key = model_config.get("api_key", "")
        if api_key.startswith("${") and api_key.endswith("}"):
            env_var = api_key[2:-1]
            model_config["api_key"] = os.environ.get(env_var, "")
        
        return model_config

# 全局配置实例
config = FulingConfig()

def get_config() -> Dict[str, Any]:
    """获取配置"""
    return config.load_config()

def get_model_config() -> Dict[str, Any]:
    """获取模型配置"""
    return config.get_model_config()