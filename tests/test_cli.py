#!/usr/bin/env python3
"""
符灵CLI测试
"""

import os
import sys
import tempfile
from pathlib import Path
from click.testing import CliRunner

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fuling.fuling_cli_enhanced import cli

class TestFulingCLI:
    """测试符灵CLI"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        
        # 设置临时的配置目录
        os.environ['HOME'] = self.temp_dir
    
    def teardown_method(self):
        """每个测试后的清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_help(self):
        """测试帮助命令"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert '符灵' in result.output
        assert '--help' in result.output
        assert '--version' in result.output
    
    def test_version(self):
        """测试版本命令"""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    def test_init_command(self):
        """测试初始化命令"""
        # 先删除可能存在的配置
        config_dir = Path(self.temp_dir) / ".config" / "fuling"
        config_file = config_dir / "config.yaml"
        if config_file.exists():
            config_file.unlink()
        
        result = self.runner.invoke(cli, ['init'])
        assert result.exit_code == 0
        assert '初始化符灵' in result.output
        assert '符咒配置已创建' in result.output
        
        # 验证配置文件被创建
        assert config_file.exists()
    
    def test_init_with_theme(self):
        """测试带主题的初始化"""
        result = self.runner.invoke(cli, ['init', '--theme', 'modern'])
        assert result.exit_code == 0
        assert 'modern' in result.output or '现代' in result.output
    
    def test_explain_command(self):
        """测试解释命令"""
        # 先初始化
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['explain', 'ls -la'])
        assert result.exit_code == 0
        assert '解读符咒' in result.output
        assert 'ls -la' in result.output
    
    def test_explain_with_context(self):
        """测试带上下文的解释命令"""
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['explain', 'grep', '--context', '搜索文件'])
        assert result.exit_code == 0
        assert 'grep' in result.output
    
    def test_wisdom_command(self):
        """测试智慧命令"""
        result = self.runner.invoke(cli, ['wisdom'])
        assert result.exit_code == 0
        assert '符灵智慧库' in result.output
        assert '常用符咒' in result.output
        assert 'fl init' in result.output
    
    def test_power_command(self):
        """测试灵力状态命令"""
        # 先初始化
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['power'])
        assert result.exit_code == 0
        assert '符灵灵力状态' in result.output
        assert '符咒配置' in result.output
        assert 'Python版本' in result.output
    
    def test_fortune_command(self):
        """测试运势命令"""
        result = self.runner.invoke(cli, ['fortune'])
        assert result.exit_code == 0
        assert '符灵占卜' in result.output
        assert '今日箴言' in result.output
        assert '幸运符咒' in result.output
    
    def test_generate_command_basic(self):
        """测试基础生成命令"""
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['generate', 'python function'])
        assert result.exit_code == 0
        assert '创造新符咒' in result.output
        assert 'python' in result.output.lower()
    
    def test_generate_command_with_language(self):
        """测试带语言的生成命令"""
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['generate', 'hello world', '--language', 'javascript'])
        assert result.exit_code == 0
        assert 'javascript' in result.output.lower()
    
    def test_generate_command_with_output(self):
        """测试带输出文件的生成命令"""
        self.runner.invoke(cli, ['init'])
        
        output_file = Path(self.temp_dir) / "test_output.py"
        
        result = self.runner.invoke(cli, [
            'generate', 
            'test function', 
            '--language', 'python',
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert '符咒已刻印' in result.output
        assert output_file.exists()
    
    def test_chat_command_no_api_key(self):
        """测试没有API密钥的聊天命令"""
        self.runner.invoke(cli, ['init'])
        
        # 确保没有API密钥
        if 'MOONSHOT_API_KEY' in os.environ:
            del os.environ['MOONSHOT_API_KEY']
        
        result = self.runner.invoke(cli, ['chat'], input='quit\n')
        assert result.exit_code == 0
        assert '召唤符灵' in result.output
        assert '需要灵力源连接' in result.output or '未连接' in result.output
    
    def test_invalid_command(self):
        """测试无效命令"""
        result = self.runner.invoke(cli, ['nonexistent'])
        assert result.exit_code != 0
        assert 'No such command' in result.output or '无效' in result.output
    
    def test_command_abbreviations(self):
        """测试命令缩写"""
        # 测试 wisdom -> wis (如果支持缩写)
        result = self.runner.invoke(cli, ['wis'])
        # 如果命令存在，应该成功；如果不存在，应该显示帮助
        if result.exit_code == 0:
            assert '智慧' in result.output
        else:
            # 应该显示帮助
            assert 'Usage' in result.output or '用法' in result.output

class TestErrorHandling:
    """测试错误处理"""
    
    def test_explain_empty_command(self):
        """测试解释空命令"""
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['explain', ''])
        # 空命令应该被处理，不崩溃
        assert result.exit_code == 0
    
    def test_generate_empty_spec(self):
        """测试生成空规范"""
        self.runner.invoke(cli, ['init'])
        
        result = self.runner.invoke(cli, ['generate', ''])
        assert result.exit_code == 0
    
    def test_invalid_theme(self):
        """测试无效主题（应该被click验证）"""
        result = self.runner.invoke(cli, ['init', '--theme', 'invalid_theme'])
        # Click应该验证选项
        assert result.exit_code != 0
    
    def test_nonexistent_output_dir(self):
        """测试不存在的输出目录"""
        self.runner.invoke(cli, ['init'])
        
        output_file = Path(self.temp_dir) / "nonexistent" / "dir" / "output.py"
        
        result = self.runner.invoke(cli, [
            'generate',
            'test',
            '--output', str(output_file)
        ])
        
        # 应该失败，因为目录不存在
        assert result.exit_code != 0
        assert '保存失败' in result.output or 'Error' in result.output

if __name__ == "__main__":
    pytest.main([__file__, "-v"])