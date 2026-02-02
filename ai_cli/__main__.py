#!/usr/bin/env python3
"""
AI-CLI 主入口点 - 简化版本
"""

import sys
import os

def main():
    """主函数"""
    # 添加项目根目录到路径
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    try:
        # 延迟导入，避免循环依赖
        from .cli_simple import cli
        cli()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("尝试安装依赖: pip install click rich prompt-toolkit pyyaml requests")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()