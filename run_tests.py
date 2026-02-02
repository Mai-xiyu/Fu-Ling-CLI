#!/usr/bin/env python3
"""
运行符灵测试
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def run_basic_tests():
    """运行基础测试"""
    print("🧪 运行符灵基础测试...")
    print("=" * 50)
    
    tests = []
    
    # 测试1: 检查核心文件
    print("\n📁 测试1: 检查核心文件")
    required_files = [
        "fuling/__init__.py",
        "fuling/fuling_core.py",
        "fuling/fuling_ai.py",
        "fuling/fuling_theme.py",
        "fuling/fuling_cli_enhanced.py",
        "setup.py",
        "requirements.txt",
        "README.md",
        "README_CN.md",
        "LICENSE",
        ".gitignore",
    ]
    
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        tests.append((f"文件: {file}", exists))
        print(f"  {status} {file}")
    
    # 测试2: 检查Python包结构
    print("\n🐍 测试2: 检查Python包结构")
    try:
        import fuling
        tests.append(("导入fuling包", True))
        print("  ✅ 成功导入fuling包")
        
        # 检查版本
        if hasattr(fuling, '__version__'):
            tests.append(("检查版本号", True))
            print(f"  ✅ 版本号: {fuling.__version__}")
        else:
            tests.append(("检查版本号", False))
            print("  ❌ 缺少版本号")
            
    except ImportError as e:
        tests.append(("导入fuling包", False))
        print(f"  ❌ 导入失败: {e}")
    
    # 测试3: 检查CLI命令
    print("\n🚀 测试3: 检查CLI命令")
    try:
        from fuling.fuling_cli import cli as cli_basic
        tests.append(("导入基础CLI", True))
        print("  ✅ 导入基础CLI")
    except ImportError as e:
        tests.append(("导入基础CLI", False))
        print(f"  ❌ 导入基础CLI失败: {e}")
    
    try:
        from fuling.fuling_cli_enhanced import cli as cli_enhanced
        tests.append(("导入增强CLI", True))
        print("  ✅ 导入增强CLI")
    except ImportError as e:
        tests.append(("导入增强CLI", False))
        print(f"  ❌ 导入增强CLI失败: {e}")
    
    # 测试4: 检查配置系统
    print("\n⚙️  测试4: 检查配置系统")
    try:
        from fuling.fuling_core import FulingConfig
        config = FulingConfig()
        default_config = config.get_default_config()
        
        if default_config and 'fuling' in default_config:
            tests.append(("配置系统", True))
            print("  ✅ 配置系统工作正常")
            print(f"    默认主题: {default_config.get('theme', {}).get('name', 'unknown')}")
        else:
            tests.append(("配置系统", False))
            print("  ❌ 配置系统异常")
            
    except Exception as e:
        tests.append(("配置系统", False))
        print(f"  ❌ 配置系统失败: {e}")
    
    # 测试5: 检查AI系统
    print("\n🤖 测试5: 检查AI系统")
    try:
        from fuling.fuling_ai import explain_command
        result = explain_command("ls -la")
        
        if result and len(result) > 0:
            tests.append(("AI解释命令", True))
            print("  ✅ AI解释命令工作正常")
            print(f"    示例输出: {result[:50]}...")
        else:
            tests.append(("AI解释命令", False))
            print("  ❌ AI解释命令返回空结果")
            
    except Exception as e:
        tests.append(("AI解释命令", False))
        print(f"  ❌ AI解释命令失败: {e}")
    
    # 测试6: 检查主题系统
    print("\n🎨 测试6: 检查主题系统")
    try:
        from fuling.fuling_theme import get_theme, format_text
        theme = get_theme()
        
        if theme and hasattr(theme, 'name'):
            tests.append(("主题系统", True))
            print(f"  ✅ 主题系统工作正常 (当前主题: {theme.name})")
            
            # 测试文本格式化
            formatted = format_text("测试", "success")
            if formatted:
                tests.append(("文本格式化", True))
                print("  ✅ 文本格式化工作正常")
            else:
                tests.append(("文本格式化", False))
                print("  ❌ 文本格式化失败")
        else:
            tests.append(("主题系统", False))
            print("  ❌ 主题系统异常")
            
    except Exception as e:
        tests.append(("主题系统", False))
        print(f"  ❌ 主题系统失败: {e}")
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {status} - {test_name}")
    
    print(f"\n🎯 通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！符灵项目准备就绪！")
        return True
    else:
        print(f"\n⚠️  有 {total-passed} 个测试失败，需要修复")
        return False

def check_installation():
    """检查安装"""
    print("\n📦 检查安装状态...")
    
    try:
        # 尝试开发安装
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ 开发安装成功")
            
            # 测试fl命令
            result = subprocess.run(
                ["fl", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ fl命令工作正常")
                print(f"  版本: {result.stdout.strip()}")
                return True
            else:
                print("❌ fl命令失败")
                print(f"  错误: {result.stderr}")
                return False
        else:
            print("❌ 开发安装失败")
            print(f"  错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装检查异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 符灵项目测试套件")
    print("=" * 50)
    
    # 运行基础测试
    if not run_basic_tests():
        print("\n❌ 基础测试失败，停止后续测试")
        sys.exit(1)
    
    # 检查安装
    print("\n" + "=" * 50)
    if check_installation():
        print("\n🎊 所有检查和测试通过！")
        print("\n📋 下一步:")
        print("  1. 提交代码到GitHub")
        print("  2. 创建v0.1.0标签")
        print("  3. 发布到PyPI (可选)")
        print("  4. 宣传和推广")
    else:
        print("\n⚠️  安装检查失败，需要修复")
        sys.exit(1)

if __name__ == "__main__":
    main()