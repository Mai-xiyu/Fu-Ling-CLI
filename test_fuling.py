#!/usr/bin/env python3
"""
测试符灵功能
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fuling import main

if __name__ == "__main__":
    # 测试命令行参数
    test_args = [
        ["--help"],
        ["--version"],
        ["init"],
        ["explain", "ls -la"],
        ["wisdom"],
        ["power"],
        ["fortune"],
    ]
    
    print("🧪 开始测试符灵功能...")
    print("=" * 50)
    
    for args in test_args:
        print(f"\n📋 测试命令: fl {' '.join(args)}")
        print("-" * 30)
        
        # 保存原始参数
        original_argv = sys.argv
        
        try:
            # 设置测试参数
            sys.argv = ["fl"] + args
            
            # 运行命令
            main()
        except SystemExit:
            # click会调用sys.exit，这是正常的
            pass
        except Exception as e:
            print(f"❌ 测试失败: {e}")
        finally:
            # 恢复原始参数
            sys.argv = original_argv
    
    print("\n" + "=" * 50)
    print("✅ 符灵功能测试完成！")
    print("\n🎯 下一步:")
    print("  1. 安装符灵: pip install -e .")
    print("  2. 设置API密钥: export MOONSHOT_API_KEY='your_key'")
    print("  3. 使用: fl explain 'docker run'")
    print("  4. 聊天: fl chat")