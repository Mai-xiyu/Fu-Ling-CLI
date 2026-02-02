#!/usr/bin/env python3
"""
符灵核心模块测试
"""

import os
import tempfile
import pytest
from pathlib import Path

# 添加父目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from fuling.fuling_core import FulingConfig

class TestFulingConfig:
    """测试配置管理"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = FulingConfig()
        # 修改配置目录为临时目录
        self.config.config_dir = Path(self.temp_dir) / ".config" / "fuling"
        self.config.config_file = self.config.config_dir / "config.yaml"
    
    def teardown_method(self):
        """每个测试后的清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_default_config(self):
        """测试默认配置"""
        config = self.config.get_default_config()
        
        assert "fuling" in config
        assert "model" in config
        assert "features" in config
        assert "theme" in config
        
        # 检查必要字段
        assert config["fuling"]["name"] == "符灵"
        assert config["fuling"]["version"] == "0.1.0"
        assert config["theme"]["name"] == "ancient"
    
    def test_save_and_load_config(self):
        """测试配置保存和加载"""
        test_config = {
            "fuling": {"name": "测试符灵", "version": "0.1.0"},
            "model": {"provider": "local"},
            "features": {"test": True},
            "theme": {"name": "test"}
        }
        
        # 保存配置
        self.config.save_config(test_config)
        
        # 验证文件存在
        assert self.config.config_file.exists()
        
        # 加载配置
        loaded_config = self.config.load_config()
        
        # 验证加载的配置
        assert loaded_config["fuling"]["name"] == "测试符灵"
        assert loaded_config["model"]["provider"] == "local"
        assert loaded_config["features"]["test"] is True
        assert loaded_config["theme"]["name"] == "test"
    
    def test_load_nonexistent_config(self):
        """测试加载不存在的配置"""
        # 确保配置文件不存在
        if self.config.config_file.exists():
            self.config.config_file.unlink()
        
        # 应该返回默认配置
        config = self.config.load_config()
        assert config is not None
        assert "fuling" in config
    
    def test_get_model_config(self):
        """测试获取模型配置"""
        test_config = {
            "model": {
                "provider": "moonshot",
                "api_key": "${MOONSHOT_API_KEY}",
                "temperature": 0.5
            }
        }
        
        self.config.save_config(test_config)
        
        # 设置环境变量
        os.environ["MOONSHOT_API_KEY"] = "test_key_123"
        
        model_config = self.config.get_model_config()
        
        assert model_config["provider"] == "moonshot"
        assert model_config["api_key"] == "test_key_123"  # 应该被替换
        assert model_config["temperature"] == 0.5
        
        # 清理环境变量
        del os.environ["MOONSHOT_API_KEY"]
    
    def test_get_model_config_no_env_var(self):
        """测试没有环境变量时的模型配置"""
        test_config = {
            "model": {
                "api_key": "${NONEXISTENT_KEY}",
            }
        }
        
        self.config.save_config(test_config)
        
        model_config = self.config.get_model_config()
        
        # 不存在的环境变量应该被替换为空字符串
        assert model_config["api_key"] == ""

class TestAIProviders:
    """测试AI提供商"""
    
    def test_local_provider_explain(self):
        """测试本地提供商的命令解释"""
        from fuling.fuling_ai import LocalProvider
        
        config = {
            "name": "local",
            "provider": "local"
        }
        
        provider = LocalProvider(config)
        
        # 测试已知命令
        result = provider.explain_command("ls -la")
        assert "天眼符" in result or "列出" in result
        
        # 测试未知命令
        result = provider.explain_command("unknown_command_xyz")
        assert "未找到" in result or "未知" in result
    
    def test_local_provider_chat(self):
        """测试本地提供商的聊天"""
        from fuling.fuling_ai import LocalProvider
        
        config = {"name": "local"}
        provider = LocalProvider(config)
        
        messages = [
            {"role": "user", "content": "解释命令 `ls -la`"}
        ]
        
        result = provider.chat_completion(messages)
        assert result is not None
        assert len(result) > 0
    
    def test_get_ai_provider(self):
        """测试获取AI提供商"""
        from fuling.fuling_ai import get_ai_provider, LocalProvider
        
        # 测试本地提供商
        provider = get_ai_provider()
        assert isinstance(provider, LocalProvider)
    
    def test_explain_command_function(self):
        """测试解释命令函数"""
        from fuling.fuling_ai import explain_command
        
        result = explain_command("pwd")
        assert result is not None
        assert len(result) > 0

class TestThemeSystem:
    """测试主题系统"""
    
    def test_get_theme(self):
        """测试获取主题"""
        from fuling.fuling_theme import get_theme
        
        theme = get_theme()
        assert theme is not None
        assert hasattr(theme, 'name')
        assert hasattr(theme, 'format_text')
        assert hasattr(theme, 'get_banner')
    
    def test_format_text(self):
        """测试文本格式化"""
        from fuling.fuling_theme import format_text
        
        # 测试各种样式
        text = format_text("测试", "prompt")
        assert "测试" in text
        
        text = format_text("成功", "success")
        assert "成功" in text
        
        text = format_text("错误", "error")
        assert "错误" in text
        
        # 测试无样式
        text = format_text("普通文本")
        assert text == "普通文本"
    
    def test_theme_classes(self):
        """测试主题类"""
        from fuling.fuling_theme import AncientTheme, ModernTheme, DarkTheme, LightTheme
        
        config = {
            "colors": {},
            "symbols": {}
        }
        
        # 测试古风主题
        ancient = AncientTheme("ancient", config)
        assert ancient.name == "ancient"
        banner = ancient.get_banner()
        assert "符灵" in banner or "Fuling" in banner
        
        # 测试现代主题
        modern = ModernTheme("modern", config)
        assert modern.name == "modern"
        
        # 测试暗黑主题
        dark = DarkTheme("dark", config)
        assert dark.name == "dark"
        
        # 测试明亮主题
        light = LightTheme("light", config)
        assert light.name == "light"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])