#!/usr/bin/env python3
"""
配置AI-CLI使用Moonshot AI (Kimi)
"""

import yaml
from pathlib import Path

config_file = Path.home() / ".config" / "ai-cli" / "config.yaml"

if config_file.exists():
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # 更新为Moonshot AI配置
    config['model'] = {
        'name': 'kimi-k2-turbo-preview',
        'provider': 'moonshot',
        'temperature': 0.3,
        'api_key': 'sk-sXGx75wQCACzecihdAEIXMMzrRt5L22GwiqlaKVPu41gJLn5',
        'base_url': 'https://api.moonshot.cn/v1',
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("✅ 配置已更新为 Moonshot AI (Kimi)")
    print(f"   模型: kimi-k2-turbo-preview")
    print(f"   API端点: https://api.moonshot.cn/v1")
    
else:
    print("❌ 配置文件不存在，请先运行 'ai init'")