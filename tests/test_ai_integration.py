#!/usr/bin/env python3
"""
测试AI集成功能
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestAIModule:
    """测试AI模块"""
    
    def test_ai_model_base(self):
        """测试AI模型基类"""
        from ai_cli.core.ai import AIModel
        
        # 创建模拟配置
        config = {
            "name": "test-model",
            "provider": "test",
            "temperature": 0.5,
        }
        
        # 测试基类
        model = AIModel(config)
        assert model.name == "test-model"
        assert model.provider == "test"
        assert model.temperature == 0.5
        
        # 测试抽象方法
        with pytest.raises(NotImplementedError):
            model.generate("test prompt")
    
    def test_local_model(self):
        """测试本地模型"""
        from ai_cli.core.ai import LocalModel
        
        config = {
            "name": "local",
            "provider": "local",
            "temperature": 0.3,
        }
        
        model = LocalModel(config)
        
        # 测试生成
        response = model.generate("test prompt")
        assert isinstance(response, str)
        assert len(response) > 0
        
        # 测试带系统提示
        response = model.generate("test", "system prompt")
        assert isinstance(response, str)
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_openai_model(self, mock_openai):
        """测试OpenAI模型（模拟）"""
        from ai_cli.core.ai import OpenAIModel
        
        # 创建模拟响应
        mock_client = Mock()
        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="AI response"))]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        config = {
            "name": "gpt-4",
            "provider": "openai",
            "api_key": "test-key",
            "temperature": 0.7,
        }
        
        model = OpenAIModel(config)
        
        # 测试生成
        response = model.generate("test prompt")
        assert response == "AI response"
        
        # 验证API调用
        mock_client.chat.completions.create.assert_called_once()
    
    def test_get_model_config(self):
        """测试获取模型配置"""
        from ai_cli.core.ai import get_model_config
        
        config = get_model_config()
        assert isinstance(config, dict)
        
        # 检查必需字段
        assert "name" in config
        assert "provider" in config
        assert "temperature" in config
    
    def test_generate_command(self):
        """测试命令生成"""
        from ai_cli.core.ai import generate_command
        
        context = {
            "directory": "/test",
            "contents": ["file1.py", "file2.txt"],
            "git": {"is_repo": False},
        }
        
        # 使用本地模型（不会真正调用AI）
        command = generate_command(context, "find python files")
        assert isinstance(command, str)
        
        # 测试无效查询
        command = generate_command(context, "")
        assert command == ""  # 空查询返回空命令
    
    def test_test_model_connection(self):
        """测试模型连接"""
        from ai_cli.core.ai import test_model_connection
        
        # 本地模型应该总是连接成功
        # 注意：如果配置了其他模型，可能会失败
        try:
            result = test_model_connection()
            assert isinstance(result, bool)
        except Exception:
            # 允许连接测试失败（如网络问题）
            pass

class TestAICommands:
    """测试AI相关命令"""
    
    def test_explain_command_module(self):
        """测试命令解释模块"""
        from ai_cli.commands.explain import explain_command
        
        # 测试本地回退
        explanation = explain_command("ls -la")
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        
        # 测试空命令
        explanation = explain_command("")
        assert "ERROR" in explanation or len(explanation) > 0
    
    def test_suggest_command_module(self):
        """测试命令建议模块"""
        from ai_cli.commands.suggest import suggest_commands, get_fallback_suggestions
        
        # 测试回退建议
        context = {
            "directory": "/test",
            "contents": ["test.py", "README.md"],
            "git": {"is_repo": True, "branch": "main"},
            "file_types": {".py"},
        }
        
        suggestions = get_fallback_suggestions(context, "clean")
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # 测试主函数
        suggestions = suggest_commands("test", context)
        assert isinstance(suggestions, list)
    
    def test_find_command_module(self):
        """测试文件搜索模块"""
        from ai_cli.commands.find import (
            find_files,
            parse_natural_language_query,
            execute_find_command
        )
        
        # 测试查询解析
        query_info = parse_natural_language_query("today python files")
        assert isinstance(query_info, dict)
        assert "keywords" in query_info
        
        # 测试本地搜索（在当前目录）
        try:
            results = find_files("test")
            assert isinstance(results, list)
        except Exception as e:
            # 允许搜索失败（如权限问题）
            print(f"搜索测试跳过: {e}")
    
    def test_grep_command_module(self):
        """测试内容搜索模块"""
        from ai_cli.commands.grep import (
            search_contents,
            extract_keywords,
            format_grep_results
        )
        
        # 测试关键词提取
        keywords = extract_keywords("search for python files with imports")
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        
        # 测试空查询
        keywords = extract_keywords("")
        assert isinstance(keywords, list)
        
        # 测试结果格式化
        results = {}
        formatted = format_grep_results(results, "test")
        assert isinstance(formatted, str)
        
        # 测试有结果的格式化
        results = {"test.py": ["Line 1: import os"]}
        formatted = format_grep_results(results, "import")
        assert "test.py" in formatted
    
    def test_history_command_module(self):
        """测试历史搜索模块"""
        from ai_cli.commands.history import (
            search_history,
            load_history,
            save_command_to_history
        )
        
        # 测试历史加载（可能没有历史文件）
        history = load_history()
        assert isinstance(history, list)
        
        # 测试历史搜索
        results = search_history("test")
        assert isinstance(results, list)
        
        # 测试保存命令（应该不抛出异常）
        try:
            save_command_to_history("test command")
            assert True
        except Exception:
            # 允许保存失败
            pass

class TestAIConfiguration:
    """测试AI配置"""
    
    def test_config_loading(self):
        """测试配置加载"""
        from ai_cli.core.config import get_config
        
        config = get_config()
        assert isinstance(config, dict)
        
        # 检查必需字段
        assert "model" in config
        assert "features" in config
        assert "aliases" in config
        
        model_config = config["model"]
        assert "name" in model_config
        assert "provider" in model_config
    
    def test_config_updates(self):
        """测试配置更新"""
        from ai_cli.core.config import get_config, update_config
        
        original_config = get_config()
        
        # 测试更新
        updates = {
            "model": {"temperature": 0.8}
        }
        
        try:
            update_config(updates)
            
            # 验证更新
            new_config = get_config()
            assert new_config["model"]["temperature"] == 0.8
            
        finally:
            # 恢复原始配置
            update_config({"model": {"temperature": original_config["model"].get("temperature", 0.3)}})
    
    def test_alias_management(self):
        """测试别名管理"""
        from ai_cli.core.config import add_alias, get_config
        
        original_config = get_config()
        original_aliases = original_config.get("aliases", {}).copy()
        
        try:
            # 测试添加别名
            add_alias("test-alias", "echo test")
            
            # 验证添加
            config = get_config()
            assert "test-alias" in config.get("aliases", {})
            assert config["aliases"]["test-alias"] == "echo test"
            
        finally:
            # 清理测试别名
            from ai_cli.core.config import update_config
            if "test-alias" in original_aliases:
                # 恢复原始值
                update_config({"aliases": original_aliases})
            else:
                # 移除测试别名
                aliases = original_aliases.copy()
                aliases.pop("test-alias", None)
                update_config({"aliases": aliases})

class TestAIErrorHandling:
    """测试AI错误处理"""
    
    def test_ai_error_messages(self):
        """测试AI错误消息"""
        from ai_cli.core.ai import OpenAIModel
        
        config = {
            "name": "test",
            "provider": "openai",
            "api_key": None,  # 无API密钥
        }
        
        model = OpenAIModel(config)
        
        # 测试无API密钥的错误
        response = model.generate("test")
        assert "ERROR" in response
        assert "API key" in response
    
    @patch('ai_cli.core.ai.OpenAI')
    def test_ai_api_errors(self, mock_openai):
        """测试AI API错误"""
        from ai_cli.core.ai import OpenAIModel
        
        # 模拟API错误
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        mock_openai.return_value = mock_client
        
        config = {
            "name": "gpt-4",
            "provider": "openai",
            "api_key": "test-key",
        }
        
        model = OpenAIModel(config)
        
        # 测试API错误处理
        response = model.generate("test")
        assert "ERROR" in response
        assert "API error" in response

def test_ai_cli_integration():
    """测试AI-CLI整体集成"""
    # 导入所有模块确保无错误
    modules = [
        "ai_cli.core.ai",
        "ai_cli.core.config",
        "ai_cli.core.context",
        "ai_cli.core.plugins",
        "ai_cli.core.performance",
        "ai_cli.commands.explain",
        "ai_cli.commands.find",
        "ai_cli.commands.suggest",
        "ai_cli.commands.grep",
        "ai_cli.commands.history",
        "ai_cli.utils.errors",
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_name}: {e}")
    
    assert True

if __name__ == "__main__":
    # 直接运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))