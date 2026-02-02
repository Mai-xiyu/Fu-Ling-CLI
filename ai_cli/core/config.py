"""
Configuration management for AI-CLI
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

CONFIG_DIR = Path.home() / ".config" / "ai-cli"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_CONFIG = {
    "model": {
        "name": "phi3:mini",
        "temperature": 0.3,
        "provider": "ollama",  # ollama, openai, local
    },
    "features": {
        "auto_suggest": True,
        "explain_commands": True,
        "safety_check": True,
        "learn_patterns": True,
    },
    "aliases": {
        "cleanup": "find . -name '*.pyc' -delete",
        "stats": "git log --oneline | wc -l",
    },
    "paths": {
        "history_file": str(CONFIG_DIR / "history.json"),
        "learning_data": str(CONFIG_DIR / "learning.json"),
    }
}

def ensure_config_dir():
    """Ensure configuration directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def init_config():
    """Initialize configuration file with defaults"""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    return load_config()

def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f) or {}
        
        # Merge with defaults for missing keys
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        return merged_config
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_config() -> Dict[str, Any]:
    """Get current configuration"""
    return load_config()

def update_config(updates: Dict[str, Any]):
    """Update configuration with new values"""
    config = load_config()
    
    # Deep merge updates
    def deep_merge(base, update):
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
    
    deep_merge(config, updates)
    save_config(config)
    return config

def get_model_config() -> Dict[str, Any]:
    """Get model-specific configuration"""
    config = load_config()
    return config.get("model", DEFAULT_CONFIG["model"])

def get_feature_config() -> Dict[str, Any]:
    """Get feature-specific configuration"""
    config = load_config()
    return config.get("features", DEFAULT_CONFIG["features"])

def add_alias(alias: str, command: str):
    """Add a new command alias"""
    config = load_config()
    
    if "aliases" not in config:
        config["aliases"] = {}
    
    config["aliases"][alias] = command
    save_config(config)

def get_alias(alias: str) -> Optional[str]:
    """Get command for an alias"""
    config = load_config()
    return config.get("aliases", {}).get(alias)

def list_aliases() -> Dict[str, str]:
    """List all aliases"""
    config = load_config()
    return config.get("aliases", {})

def remove_alias(alias: str) -> bool:
    """Remove an alias"""
    config = load_config()
    
    if alias in config.get("aliases", {}):
        del config["aliases"][alias]
        save_config(config)
        return True
    
    return False