# 👥 贡献指南

欢迎为 AI-CLI 项目做出贡献！无论你是修复 bug、添加新功能还是改进文档，我们都非常感谢。

## 开始之前

### 行为准则
请阅读并遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

### 开发环境
- Python 3.8+
- Git
- 推荐使用虚拟环境

### 设置开发环境
```bash
# 1. 克隆仓库
git clone https://github.com/xiyu-bot-assistant/ai-cli.git
cd ai-cli

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 安装预提交钩子
pre-commit install
```

## 贡献流程

### 1. 创建 Issue
在开始工作之前，请先创建一个 Issue 描述你想要解决的问题或添加的功能。

### 2. 创建分支
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/issue-number-description
```

**分支命名约定**：
- `feature/` - 新功能
- `fix/` - bug修复
- `docs/` - 文档更新
- `test/` - 测试相关
- `refactor/` - 代码重构
- `style/` - 代码风格

### 3. 编写代码
遵循我们的编码规范：
- 使用 Black 格式化代码
- 使用 Flake8 检查代码风格
- 添加类型提示
- 编写文档字符串

### 4. 编写测试
- 为新功能添加测试
- 确保所有测试通过
- 测试覆盖率不应降低

```bash
# 运行测试
pytest tests/

# 运行特定测试
pytest tests/test_cli.py -v

# 检查覆盖率
pytest --cov=ai_cli tests/
```

### 5. 提交更改
```bash
# 添加更改
git add .

# 提交（遵循约定式提交）
git commit -m "feat: add new feature"
# 或
git commit -m "fix: resolve issue #123"
```

**提交信息格式**：
```
类型(范围): 描述

详细描述（可选）

关联 Issue: #123
```

**类型**：
- `feat` - 新功能
- `fix` - bug修复
- `docs` - 文档
- `style` - 格式
- `refactor` - 重构
- `test` - 测试
- `chore` - 维护

### 6. 推送分支
```bash
git push origin your-branch-name
```

### 7. 创建 Pull Request
1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板
3. 关联相关 Issue
4. 等待代码审查

## 代码规范

### Python 代码
```python
# ✅ 正确
from typing import List, Dict, Optional
import os
from pathlib import Path

def function_name(param: str) -> Optional[str]:
    """函数文档字符串。
    
    Args:
        param: 参数描述
        
    Returns:
        返回值描述
    """
    if not param:
        return None
    
    return param.upper()

# ❌ 避免
def badFunction(param):
    if param==None:
        return
    return param.upper()
```

### 导入顺序
1. 标准库
2. 第三方库
3. 本地模块

```python
import os
import sys
from pathlib import Path
from typing import Dict, List

import click
from rich.console import Console

from ai_cli.core.config import get_config
```

### 错误处理
```python
# ✅ 正确
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"值错误: {e}")
    raise
except Exception as e:
    logger.exception("未知错误")
    raise CustomError("操作失败") from e

# ❌ 避免
try:
    result = risky_operation()
except:
    pass  # 不要静默忽略错误
```

## 测试指南

### 测试结构
```
tests/
├── test_cli.py              # CLI测试
├── test_ai_integration.py   # AI集成测试
├── test_plugins.py          # 插件测试
├── test_performance.py      # 性能测试
└── conftest.py             # 测试配置
```

### 编写测试
```python
import pytest
from unittest.mock import Mock, patch

def test_function_success():
    """测试成功情况"""
    result = function_under_test("input")
    assert result == "expected"

def test_function_failure():
    """测试失败情况"""
    with pytest.raises(ValueError):
        function_under_test("")

@patch("module.function")
def test_with_mock(mock_func):
    """使用模拟对象测试"""
    mock_func.return_value = "mocked"
    result = function_under_test()
    assert result == "mocked"
```

### 测试覆盖率
目标：核心模块 > 80% 覆盖率
```bash
# 生成覆盖率报告
pytest --cov=ai_cli --cov-report=html tests/

# 查看报告
open htmlcov/index.html
```

## 文档指南

### 文档结构
```
docs/
├── QUICK_START.md      # 快速开始
├── API_REFERENCE.md    # API参考
├── PLUGIN_GUIDE.md     # 插件指南
├── CONFIGURATION.md    # 配置说明
└── CONTRIBUTING.md     # 贡献指南
```

### 编写文档
- 使用 Markdown 格式
- 包含代码示例
- 添加截图（如果需要）
- 保持更新

### 代码注释
```python
def complex_function(param1: int, param2: str) -> Dict[str, Any]:
    """函数功能描述。
    
    详细描述函数的功能、算法或实现细节。
    
    Args:
        param1: 第一个参数，描述用途
        param2: 第二个参数，描述用途
        
    Returns:
        返回值的详细描述，包括数据结构
        
    Raises:
        ValueError: 当参数无效时
        RuntimeError: 当操作失败时
        
    Examples:
        >>> complex_function(1, "test")
        {'result': 'test1'}
    """
```

## 插件开发

### 插件规范
- 继承 `Plugin` 基类
- 提供完整的元数据
- 处理错误情况
- 编写测试

### 插件测试
```python
def test_plugin_loading():
    """测试插件加载"""
    from ai_cli.core.plugins import PluginManager
    
    manager = PluginManager()
    manager.load_plugins()
    
    plugin = manager.get_plugin("example")
    assert plugin is not None
    assert plugin.name == "example"
```

## 发布流程

### 版本管理
使用语义化版本：
- `MAJOR.MINOR.PATCH`
- `1.0.0` - 初始发布
- `1.1.0` - 向后兼容的新功能
- `1.1.1` - bug修复

### 发布检查清单
- [ ] 所有测试通过
- [ ] 文档更新
- [ ] 版本号更新
- [ ] CHANGELOG 更新
- [ ] 代码审查完成

### 创建发布
```bash
# 更新版本号
# 在 setup.py 和 __init__.py 中

# 更新 CHANGELOG
# 添加新版本条目

# 创建标签
git tag v1.0.0
git push --tags

# 构建发布包
python -m build

# 上传到 PyPI
twine upload dist/*
```

## 获取帮助

### 讨论区
- [GitHub Discussions](https://github.com/xiyu-bot-assistant/ai-cli/discussions)
- [Issue Tracker](https://github.com/xiyu-bot-assistant/ai-cli/issues)

### 沟通渠道
- 在 Issue 中讨论
- 在 PR 中审查代码
- 在 Discussions 中提问

### 寻求帮助
如果你遇到问题：
1. 查看文档
2. 搜索现有 Issue
3. 创建新的 Issue
4. 在 Discussions 中提问

## 致谢

感谢所有贡献者！你的工作使这个项目变得更好。

### 贡献者名单
查看 [贡献者页面](https://github.com/xiyu-bot-assistant/ai-cli/graphs/contributors)。

---

**记住**：开源贡献应该是愉快和有教育意义的。如果你有任何问题或需要帮助，请随时询问！ 🚀