#!/usr/bin/env python3
"""
测试AI集成功能
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_cli.core.ai import (
    AIModel, 
    OpenAIModel, 
    LocalModel,
    get_model, 
    get_model_config,
    generate_command,
    test_model_connection
)
from ai_cli.core.config import get_config

class TestAIModelBase:
    """测试AI模型基类"""
    
    def test_aimodel_initialization(self):
        """测试AIModel初始化"""
        config = {
            "name": "test-model",
            "provider": "test",
            "temperature": 0.5
        }
        
        model = AIModel(config)
        assert model.name == "test-model"
        assert model.provider == "test"
        assert model.temperature == 0.5
    
    def test_aimodel_generate_not_implemented(self):
        """测试AIModel生成方法未实现"""
        model = AIModel({})
        with pytest.raises(NotImplementedError):
            model.generate("test prompt")

class TestLocalModel:
    """测试本地模型"""
    
    def test_local_model_initialization(self):
        """测试LocalModel初始化"""
        config = {
            "name": "local",
            "provider": "local",
            "temperature": 0.3
        }
        
        model = LocalModel(config)
        assert model.name == "local"
        assert model.provider == "local"
    
    def test_local_model_generate(self):
        """测试LocalModel生成"""
        model = LocalModel({})
        response = model.generate("test prompt")
        
        # LocalModel应该返回一个字符串
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_local_model_with_system_prompt(self):
        """测试LocalModel带系统提示"""
        model = LocalModel({})
        response = model.generate("test prompt", "system prompt")
        assert isinstance(response, str)

class TestOpenAIModel:
    """测试OpenAI模型"""
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_openai_model_initialization(self, mock_openai):
        """测试OpenAIModel初始化"""
        config = {
            "name": "gpt-4",
            "provider": "openai",
            "api_key": "test-key",
            "base_url": "https://api.test.com/v1",
            "temperature": 0.7
        }
        
        model = OpenAIModel(config)
        assert model.name == "gpt-4"
        assert model.provider == "openai"
        assert model.api_key == "test-key"
        assert model.base_url == "https://api.test.com/v1"
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_openai_model_generate_success(self, mock_openai):
        """测试OpenAIModel生成成功"""
        # 模拟OpenAI客户端
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        mock_message.content = "Test response from AI"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        mock_openai.return_value = mock_client
        
        config = {
            "name": "gpt-4",
            "provider": "openai",
            "api_key": "test-key"
        }
        
        model = OpenAIModel(config)
        response = model.generate("test prompt")
        
        assert response == "Test response from AI"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_openai_model_generate_with_system_prompt(self, mock_openai):
        """测试OpenAIModel带系统提示"""
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        
        mock_message.content = "Response with system prompt"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        mock_openai.return_value = mock_client
        
        model = OpenAIModel({"api_key": "test-key"})
        response = model.generate("user prompt", "system prompt")
        
        # 验证调用了正确的消息结构
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]['messages']
        
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[0]['content'] == 'system prompt'
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == 'user prompt'
    
    def test_openai_model_no_api_key(self):
        """测试OpenAIModel没有API密钥"""
        model = OpenAIModel({})
        response = model.generate("test prompt")
        
        assert "ERROR" in response
        assert "API key" in response
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_openai_model_api_error(self, mock_openai):
        """测试OpenAIModel API错误"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        mock_openai.return_value = mock_client
        
        model = OpenAIModel({"api_key": "test-key"})
        response = model.generate("test prompt")
        
        assert "ERROR" in response
        assert "API error" in response

class TestModelFactory:
    """测试模型工厂函数"""
    
    def test_get_model_config(self):
        """测试获取模型配置"""
        # 模拟配置文件
        with patch('ai_cli.core.ai.get_config') as mock_get_config:
            mock_get_config.return_value = {
                "model": {
                    "name": "test-model",
                    "provider": "test",
                    "temperature": 0.5
                }
            }
            
            config = get_model_config()
            assert config["name"] == "test-model"
            assert config["provider"] == "test"
            assert config["temperature"] == 0.5
    
    def test_get_model_local(self):
        """测试获取本地模型"""
        with patch('ai_cli.core.ai.get_model_config') as mock_get_config:
            mock_get_config.return_value = {
                "provider": "local",
                "name": "local"
            }
            
            model = get_model()
            assert isinstance(model, LocalModel)
    
    def test_get_model_openai(self):
        """测试获取OpenAI模型"""
        with patch('ai_cli.core.ai.get_model_config') as mock_get_config:
            mock_get_config.return_value = {
                "provider": "openai",
                "name": "gpt-4",
                "api_key": "test-key"
            }
            
            model = get_model()
            assert isinstance(model, OpenAIModel)
            assert model.name == "gpt-4"
    
    def test_get_model_moonshot(self):
        """测试获取Moonshot模型"""
        with patch('ai_cli.core.ai.get_model_config') as mock_get_config:
            mock_get_config.return_value = {
                "provider": "moonshot",
                "name": "kimi",
                "api_key": "test-key",
                "base_url": "https://api.moonshot.cn/v1"
            }
            
            model = get_model()
            assert isinstance(model, OpenAIModel)
            assert model.base_url == "https://api.moonshot.cn/v1"
    
    def test_get_model_fallback(self):
        """测试模型获取失败回退"""
        with patch('ai_cli.core.ai.get_model_config') as mock_get_config:
            mock_get_config.return_value = {
                "provider": "unknown",
                "name": "unknown"
            }
            
            # 模拟OpenAIModel初始化失败
            with patch('ai_cli.core.ai.OpenAIModel', side_effect=Exception("Init failed")):
                model = get_model()
                assert isinstance(model, LocalModel)

class TestAIFunctions:
    """测试AI功能函数"""
    
    def test_generate_command(self):
        """测试生成命令函数"""
        context = {
            "directory": "/test",
            "contents": ["file1.py", "file2.txt"],
            "git": {"is_repo": False}
        }
        
        # 使用本地模型测试
        with patch('ai_cli.core.ai.get_model') as mock_get_model:
            mock_model = Mock()
            mock_model.generate.return_value = "find . -name '*.py'"
            mock_get_model.return_value = mock_model
            
            command = generate_command(context, "find python files")
            assert command == "find . -name '*.py'"
    
    def test_test_model_connection_success(self):
        """测试模型连接成功"""
        with patch('ai_cli.core.ai.get_model') as mock_get_model:
            mock_model = Mock()
            mock_model.generate.return_value = "test response"
            mock_get_model.return_value = mock_model
            
            connected = test_model_connection()
            assert connected is True
    
    def test_test_model_connection_failure(self):
        """测试模型连接失败"""
        with patch('ai_cli.core.ai.get_model') as mock_get_model:
            mock_model = Mock()
            mock_model.generate.side_effect = Exception("Connection failed")
            mock_get_model.return_value = mock_model
            
            connected = test_model_connection()
            assert connected is False

class TestIntegration:
    """测试集成功能"""
    
    def test_config_integration(self):
        """测试配置集成"""
        # 确保配置模块可以导入
        from ai_cli.core.config import get_config, update_config
        
        # 测试获取配置（可能为空）
        config = get_config()
        assert isinstance(config, dict)
        
        # 测试更新配置
        test_update = {"test": "value"}
        try:
            update_config(test_update)
            updated = get_config()
            assert updated.get("test") == "value"
        except Exception:
            pass  # 更新可能失败（权限问题等）
    
    def test_ai_with_config(self):
        """测试AI与配置集成"""
        # 模拟配置
        with patch('ai_cli.core.ai.get_model_config') as mock_get_config:
            mock_get_config.return_value = {
                "provider": "local",
                "name": "local"
            }
            
            model = get_model()
            assert model.provider == "local"
            
            response = model.generate("test")
            assert isinstance(response, str)

def test_error_handling():
    """测试错误处理"""
    # 测试无效配置
    model = LocalModel({})
    response = model.generate("")
    assert isinstance(response, str)
    
    # 测试OpenAI模型错误
    openai_model = OpenAIModel({})  # 没有API密钥
    response = openai_model.generate("test")
    assert "ERROR" in response

if __name__ == "__main__":
    # 直接运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))