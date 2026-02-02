#!/usr/bin/env python3
"""
测试插件系统
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import shutil

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestPluginBase:
    """测试插件基类"""
    
    def test_plugin_initialization(self):
        """测试插件初始化"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test-plugin", "1.0.0")
        
        assert plugin.name == "test-plugin"
        assert plugin.version == "1.0.0"
        assert plugin.description == ""
        assert plugin.author == ""
        assert plugin.commands == {}
        assert plugin.hooks == {}
    
    def test_plugin_with_metadata(self):
        """测试带元数据的插件"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test", "1.0.0")
        plugin.description = "测试插件"
        plugin.author = "测试作者"
        
        assert plugin.description == "测试插件"
        assert plugin.author == "测试作者"
    
    def test_register_command(self):
        """测试注册命令"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test", "1.0.0")
        
        def test_command():
            return "test"
        
        plugin.register_command("test", test_command, "测试命令")
        
        assert "test" in plugin.commands
        assert plugin.commands["test"]["function"] == test_command
        assert plugin.commands["test"]["help"] == "测试命令"
    
    def test_register_hook(self):
        """测试注册钩子"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test", "1.0.0")
        
        def test_hook():
            return "hook"
        
        plugin.register_hook("before_command", test_hook)
        
        assert "before_command" in plugin.hooks
        assert len(plugin.hooks["before_command"]) == 1
        assert plugin.hooks["before_command"][0] == test_hook
        
        # 测试注册多个钩子
        def another_hook():
            return "another"
        
        plugin.register_hook("before_command", another_hook)
        assert len(plugin.hooks["before_command"]) == 2
    
    def test_execute_hook(self):
        """测试执行钩子"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test", "1.0.0")
        
        results = []
        
        def hook1():
            results.append("hook1")
            return "result1"
        
        def hook2():
            results.append("hook2")
            return "result2"
        
        plugin.register_hook("test_hook", hook1)
        plugin.register_hook("test_hook", hook2)
        
        hook_results = plugin.execute_hook("test_hook")
        
        assert results == ["hook1", "hook2"]
        assert hook_results == ["result1", "result2"]
    
    def test_execute_hook_with_exception(self):
        """测试钩子执行异常"""
        from ai_cli.core.plugins import Plugin
        
        plugin = Plugin("test", "1.0.0")
        
        def good_hook():
            return "good"
        
        def bad_hook():
            raise ValueError("hook error")
        
        plugin.register_hook("test", good_hook)
        plugin.register_hook("test", bad_hook)
        
        # 异常不应该传播，应该被捕获
        results = plugin.execute_hook("test")
        assert results == ["good"]  # 只有成功的钩子返回结果

class TestPluginManager:
    """测试插件管理器"""
    
    def setup_method(self):
        """测试设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.plugin_dir = Path(self.temp_dir) / "plugins"
        self.plugin_dir.mkdir()
    
    def teardown_method(self):
        """测试清理"""
        shutil.rmtree(self.temp_dir)
    
    def create_test_plugin(self, name="test_plugin"):
        """创建测试插件文件"""
        plugin_code = f'''
from ai_cli.core.plugins import Plugin

class {name.title().replace("_", "")}Plugin(Plugin):
    def __init__(self):
        super().__init__("{name}", "1.0.0")
        self.description = "测试插件"
        self.author = "测试作者"
        
        self.register_command("hello", self.hello, "打招呼")
        self.register_command("echo", self.echo, "回声")
    
    def hello(self, name="World"):
        return f"Hello, {{name}}!"
    
    def echo(self, *args):
        return " ".join(args)
'''
        
        plugin_file = self.plugin_dir / f"{name}.py"
        plugin_file.write_text(plugin_code)
        return plugin_file
    
    def test_plugin_manager_initialization(self):
        """测试插件管理器初始化"""
        from ai_cli.core.plugins import PluginManager
        
        manager = PluginManager()
        assert manager.plugins == {}
        assert manager.loaded == False
    
    def test_load_plugins(self):
        """测试加载插件"""
        from ai_cli.core.plugins import PluginManager
        
        # 创建测试插件
        self.create_test_plugin("test_plugin")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        assert manager.loaded == True
        assert "test_plugin" in manager.plugins
        
        plugin = manager.plugins["test_plugin"]
        assert plugin.name == "test_plugin"
        assert plugin.version == "1.0.0"
        assert plugin.description == "测试插件"
    
    def test_load_multiple_plugins(self):
        """测试加载多个插件"""
        from ai_cli.core.plugins import PluginManager
        
        # 创建多个插件
        self.create_test_plugin("plugin1")
        self.create_test_plugin("plugin2")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        assert len(manager.plugins) == 2
        assert "plugin1" in manager.plugins
        assert "plugin2" in manager.plugins
    
    def test_load_plugins_with_errors(self):
        """测试加载插件时的错误处理"""
        from ai_cli.core.plugins import PluginManager
        
        # 创建有语法错误的插件
        bad_plugin = self.plugin_dir / "bad_plugin.py"
        bad_plugin.write_text("invalid python code")
        
        manager = PluginManager()
        
        # 不应该抛出异常
        manager.load_plugins(self.plugin_dir)
        
        # 错误插件不应该加载
        assert "bad_plugin" not in manager.plugins
    
    def test_get_plugin(self):
        """测试获取插件"""
        from ai_cli.core.plugins import PluginManager
        
        self.create_test_plugin("test_plugin")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        plugin = manager.get_plugin("test_plugin")
        assert plugin is not None
        assert plugin.name == "test_plugin"
        
        # 测试不存在的插件
        nonexistent = manager.get_plugin("nonexistent")
        assert nonexistent is None
    
    def test_get_all_plugins(self):
        """测试获取所有插件"""
        from ai_cli.core.plugins import PluginManager
        
        self.create_test_plugin("plugin1")
        self.create_test_plugin("plugin2")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        plugins = manager.get_all_plugins()
        assert len(plugins) == 2
        assert all(p.name in ["plugin1", "plugin2"] for p in plugins)
    
    def test_execute_hook_across_plugins(self):
        """测试跨插件执行钩子"""
        from ai_cli.core.plugins import PluginManager
        
        # 创建多个插件，每个都有钩子
        plugin1_code = '''
from ai_cli.core.plugins import Plugin

class Plugin1Plugin(Plugin):
    def __init__(self):
        super().__init__("plugin1", "1.0.0")
        self.register_hook("test_hook", self.hook)
    
    def hook(self):
        return "plugin1"
'''
        
        plugin2_code = '''
from ai_cli.core.plugins import Plugin

class Plugin2Plugin(Plugin):
    def __init__(self):
        super().__init__("plugin2", "1.0.0")
        self.register_hook("test_hook", self.hook)
    
    def hook(self):
        return "plugin2"
'''
        
        (self.plugin_dir / "plugin1.py").write_text(plugin1_code)
        (self.plugin_dir / "plugin2.py").write_text(plugin2_code)
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        results = manager.execute_hook("test_hook")
        assert set(results) == {"plugin1", "plugin2"}
    
    def test_get_command(self):
        """测试获取命令"""
        from ai_cli.core.plugins import PluginManager
        
        self.create_test_plugin("test_plugin")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        # 测试存在的命令
        cmd_info = manager.get_command("hello")
        assert cmd_info is not None
        assert cmd_info["plugin"] == "test_plugin"
        assert "function" in cmd_info
        assert "help" in cmd_info
        
        # 执行命令
        func = cmd_info["function"]
        result = func("Test")
        assert result == "Hello, Test!"
        
        # 测试不存在的命令
        nonexistent = manager.get_command("nonexistent")
        assert nonexistent is None
    
    def test_list_commands(self):
        """测试列出命令"""
        from ai_cli.core.plugins import PluginManager
        
        self.create_test_plugin("test_plugin")
        
        manager = PluginManager()
        manager.load_plugins(self.plugin_dir)
        
        commands = manager.list_commands()
        assert isinstance(commands, dict)
        assert "hello" in commands
        assert "echo" in commands
        
        cmd_info = commands["hello"]
        assert cmd_info["plugin"] == "test_plugin"
        assert cmd_info["help"] == "打招呼"

class TestExamplePlugin:
    """测试示例插件"""
    
    def test_example_plugin_import(self):
        """测试示例插件导入"""
        # 确保示例插件可以导入
        try:
            from ai_cli.core.plugins import ExamplePlugin, GitPlugin
            assert True
        except ImportError:
            pytest.fail("Failed to import example plugins")
    
    def test_example_plugin_creation(self):
        """测试示例插件创建"""
        from ai_cli.core.plugins import ExamplePlugin
        
        plugin = ExamplePlugin()
        
        assert plugin.name == "example"
        assert plugin.version == "1.0.0"
        assert plugin.description == "示例插件，演示插件系统功能"
        assert plugin.author == "AI-CLI Team"
        
        # 检查命令
        assert "hello" in plugin.commands
        assert "calc" in plugin.commands
        
        # 检查钩子
        assert "before_command" in plugin.hooks
        assert "after_command" in plugin.hooks
    
    def test_example_plugin_commands(self):
        """测试示例插件命令"""
        from ai_cli.core.plugins import ExamplePlugin
        
        plugin = ExamplePlugin()
        
        # 测试 hello 命令
        hello_func = plugin.commands["hello"]["function"]
        result = hello_func("Test")
        assert result == "Greeted Test"
        
        # 测试 calc 命令
        calc_func = plugin.commands["calc"]["function"]
        result = calc_func("1 + 2 * 3")
        assert result == 7
    
    def test_git_plugin_creation(self):
        """测试Git插件创建"""
        from ai_cli.core.plugins import GitPlugin
        
        plugin = GitPlugin()
        
        assert plugin.name == "git"
        assert plugin.version == "1.0.0"
        assert plugin.description == "Git版本控制集成"
        assert plugin.author == "AI-CLI Team"
        
        # 检查命令
        assert "git-status" in plugin.commands
        assert "git-branch-info" in plugin.commands

class TestPluginIntegration:
    """测试插件集成"""
    
    @patch('ai_cli.core.plugins.console')
    def test_plugin_list_command(self, mock_console):
        """测试插件列表命令"""
        from ai_cli.core.plugins import list_plugins_command
        
        # 模拟控制台输出
        mock_print = Mock()
        mock_console.print = mock_print
        
        # 运行命令
        list_plugins_command()
        
        # 验证调用了打印
        assert mock_print.called
    
    @patch('ai_cli.core.plugins.console')
    def test_plugin_info_command(self, mock_console):
        """测试插件信息命令"""
        from ai_cli.core.plugins import plugin_info_command
        
        # 模拟控制台输出
        mock_print = Mock()
        mock_console.print = mock_print
        
        # 测试不存在的插件
        plugin_info_command("nonexistent")
        
        # 验证错误消息
        assert mock_print.called
        # 第一个调用应该是错误消息
        first_call = mock_print.call_args_list[0]
        assert "not found" in str(first_call).lower()

def test_global_plugin_manager():
    """测试全局插件管理器"""
    from ai_cli.core.plugins import plugin_manager, get_plugin_manager
    
    # 测试单例模式
    manager1 = get_plugin_manager()
    manager2 = get_plugin_manager()
    assert manager1 is manager2
    
    # 测试全局实例
    assert plugin_manager is manager1

def test_plugin_module_imports():
    """测试插件模块导入"""
    # 确保所有必要的模块可以导入
    modules = [
        "ai_cli.core.plugins",
        "ai_cli.core.dynamic_commands",
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