#!/usr/bin/env python3
"""
集成测试 - 测试AI-CLI整体功能
"""

import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import subprocess

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestEndToEnd:
    """端到端测试"""
    
    def setup_method(self):
        """测试设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # 创建测试文件
        (Path(self.temp_dir) / "test.py").write_text("print('Hello, World!')")
        (Path(self.temp_dir) / "README.md").write_text("# Test Project")
        (Path(self.temp_dir) / "data.txt").write_text("test data\nanother line")
    
    def teardown_method(self):
        """测试清理"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_cli_basic_commands(self):
        """测试CLI基础命令"""
        from ai_cli.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # 测试版本
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()
        
        # 测试帮助
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "Commands:" in result.output
    
    def test_config_commands(self):
        """测试配置命令"""
        from ai_cli.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # 测试配置显示
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0
        assert "Configuration" in result.output or "配置" in result.output
        
        # 测试状态命令
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "Status" in result.output or "状态" in result.output
    
    def test_ai_commands_with_mock(self):
        """测试AI命令（使用模拟）"""
        from ai_cli.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # 测试解释命令
        result = runner.invoke(cli, ["explain", "ls -la"])
        assert result.exit_code == 0
        # 可能返回AI解释或错误消息
        
        # 测试建议命令
        result = runner.invoke(cli, ["suggest"])
        assert result.exit_code == 0
        # 应该返回一些建议
    
    def test_file_commands(self):
        """测试文件相关命令"""
        from ai_cli.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # 测试查找命令
        result = runner.invoke(cli, ["find", "test"])
        assert result.exit_code == 0
        # 可能找到文件或返回空结果
        
        # 测试grep命令
        result = runner.invoke(cli, ["grep", "data"])
        assert result.exit_code == 0
        # 可能找到内容或返回空结果

class TestPluginIntegration:
    """测试插件集成"""
    
    def setup_method(self):
        """测试设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.plugin_dir = Path(self.temp_dir) / "plugins"
        self.plugin_dir.mkdir()
        
        # 创建测试插件
        plugin_code = '''
from ai_cli.core.plugins import Plugin

class TestPlugin(Plugin):
    def __init__(self):
        super().__init__("test-plugin", "1.0.0")
        self.description = "测试插件"
        self.author = "测试"
        
        self.register_command("test", self.test_command, "测试命令")
        self.register_command("echo", self.echo_command, "回声命令")
    
    def test_command(self):
        return "test passed"
    
    def echo_command(self, *args):
        return " ".join(args) if args else "echo"
'''
        
        (self.plugin_dir / "test_plugin.py").write_text(plugin_code)
    
    def teardown_method(self):
        """测试清理"""
        shutil.rmtree(self.temp_dir)
    
    @patch('ai_cli.core.plugins.Path')
    def test_plugin_loading_integration(self, mock_path):
        """测试插件加载集成"""
        # 模拟Path.home()返回临时目录
        mock_home = Mock()
        mock_home.__truediv__.return_value = self.plugin_dir.parent
        mock_path.home.return_value = mock_home
        
        from ai_cli.core.plugins import get_plugin_manager
        
        manager = get_plugin_manager()
        
        # 插件应该被加载
        plugin = manager.get_plugin("test-plugin")
        assert plugin is not None
        assert plugin.name == "test-plugin"
        
        # 命令应该可用
        cmd_info = manager.get_command("test")
        assert cmd_info is not None
        assert cmd_info["plugin"] == "test-plugin"
        
        # 执行命令
        func = cmd_info["function"]
        result = func()
        assert result == "test passed"

class TestPerformanceIntegration:
    """测试性能集成"""
    
    def test_performance_monitoring(self):
        """测试性能监控集成"""
        from ai_cli.core.performance import (
            PerformanceMonitor,
            measure_performance,
            monitor as global_monitor
        )
        
        # 保存原始状态
        original_metrics = global_monitor.metrics.copy()
        
        @measure_performance("integration_test")
        def test_function():
            # 模拟一些工作
            total = 0
            for i in range(100):
                total += i
            return total
        
        # 调用函数
        result = test_function()
        assert result == sum(range(100))
        
        # 验证性能指标
        assert "integration_test" in global_monitor.metrics
        assert len(global_monitor.metrics["integration_test"]) == 1
        
        # 清理
        global_monitor.metrics = original_metrics
    
    def test_cache_integration(self):
        """测试缓存集成"""
        from ai_cli.core.performance import cache_result
        
        call_count = 0
        
        @cache_result(ttl=60)
        def expensive_operation(x):
            nonlocal call_count
            call_count += 1
            return x * x
        
        # 第一次调用
        result1 = expensive_operation(5)
        assert result1 == 25
        assert call_count == 1
        
        # 第二次调用（应该使用缓存）
        result2 = expensive_operation(5)
        assert result2 == 25
        assert call_count == 1

class TestErrorHandlingIntegration:
    """测试错误处理集成"""
    
    def test_error_handling_in_commands(self):
        """测试命令中的错误处理"""
        from ai_cli.cli import cli
        from click.testing import CliRunner
        
        runner = CliRunner()
        
        # 测试无效命令
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "Error" in result.output or "error" in result.output.lower()
        
        # 测试带调试模式
        result = runner.invoke(cli, ["--debug", "invalid-command"])
        # 调试模式可能显示更多信息
    
    def test_config_error_handling(self):
        """测试配置错误处理"""
        import yaml
        from pathlib import Path
        
        # 创建无效的配置文件
        config_dir = Path.home() / ".config" / "ai-cli"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = config_dir / "config.yaml"
        original_content = None
        
        if config_file.exists():
            original_content = config_file.read_text()
        
        try:
            # 写入无效YAML
            config_file.write_text("invalid: yaml: content: [")
            
            # 尝试加载配置（应该处理错误）
            from ai_cli.core.config import get_config
            
            try:
                config = get_config()
                # 如果加载成功，配置应该使用默认值
                assert isinstance(config, dict)
            except yaml.YAMLError:
                # 允许YAML解析错误
                pass
                
        finally:
            # 恢复原始配置
            if original_content:
                config_file.write_text(original_content)
            elif config_file.exists():
                config_file.unlink()

class TestModuleIntegration:
    """测试模块集成"""
    
    def test_all_modules_import(self):
        """测试所有模块导入"""
        modules = [
            "ai_cli",
            "ai_cli.cli",
            "ai_cli.core",
            "ai_cli.core.config",
            "ai_cli.core.ai",
            "ai_cli.core.context",
            "ai_cli.core.plugins",
            "ai_cli.core.performance",
            "ai_cli.commands",
            "ai_cli.commands.explain",
            "ai_cli.commands.find",
            "ai_cli.commands.suggest",
            "ai_cli.commands.grep",
            "ai_cli.commands.history",
            "ai_cli.utils",
            "ai_cli.utils.errors",
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")
        
        assert True
    
    def test_command_availability(self):
        """测试命令可用性"""
        from ai_cli.cli import cli
        
        # 检查核心命令
        core_commands = [
            "init",
            "config",
            "status",
            "explain",
            "find",
            "suggest",
            "grep",
            "history",
            "learn",
            "interactive",
            "plugin",
            "perf",
            "commands",
        ]
        
        available_commands = list(cli.commands.keys())
        
        for cmd in core_commands:
            assert cmd in available_commands, f"Command {cmd} not found"
    
    def test_config_defaults(self):
        """测试配置默认值"""
        from ai_cli.core.config import get_config
        
        config = get_config()
        
        # 检查必需字段
        assert "model" in config
        assert "features" in config
        assert "aliases" in config
        
        model_config = config["model"]
        assert "name" in model_config
        assert "provider" in model_config
        assert "temperature" in model_config
        
        features = config["features"]
        assert isinstance(features, dict)
        
        aliases = config.get("aliases", {})
        assert isinstance(aliases, dict)

def test_example_scripts():
    """测试示例脚本"""
    example_dir = Path(__file__).parent.parent / "examples"
    
    if not example_dir.exists():
        pytest.skip("Examples directory not found")
    
    example_files = list(example_dir.glob("*.py"))
    
    for example_file in example_files:
        # 检查文件是否可以导入（不实际运行）
        try:
            # 将示例目录添加到路径
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                f"example_{example_file.stem}",
                example_file
            )
            module = importlib.util.module_from_spec(spec)
            
            # 只检查语法，不执行
            with open(example_file, "r") as f:
                source = f.read()
                compile(source, example_file.name, "exec")
                
        except SyntaxError as e:
            pytest.fail(f"Syntax error in {example_file}: {e}")
        except Exception as e:
            # 其他错误可能由于依赖问题，可以接受
            print(f"Note: {example_file} has import issues (may be expected): {e}")

def test_documentation_files():
    """测试文档文件"""
    docs_dir = Path(__file__).parent.parent / "docs"
    
    if not docs_dir.exists():
        pytest.skip("Docs directory not found")
    
    required_docs = [
        "QUICK_START.md",
        "API_REFERENCE.md",
        "PLUGIN_GUIDE.md",
        "CONFIGURATION.md",
    ]
    
    for doc_file in required_docs:
        doc_path = docs_dir / doc_file
        assert doc_path.exists(), f"Required documentation {doc_file} not found"
        
        # 检查文件不为空
        content = doc_path.read_text()
        assert len(content.strip()) > 0, f"Documentation {doc_file} is empty"

if __name__ == "__main__":
    # 直接运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))