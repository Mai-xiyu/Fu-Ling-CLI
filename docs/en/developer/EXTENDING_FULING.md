# Extending Fuling

## 🎯 Overview

Fuling is designed to be extensible. You can:
- Create custom commands
- Add new AI providers
- Develop plugins
- Customize themes
- Integrate with other tools

## 🚀 Quick Extension Examples

### 1. Create a Custom Command

**File**: `~/.config/fuling/plugins/my_commands.py`
```python
import click
from fuling import format_text

@click.command()
@click.argument('name')
def hello(name):
    """Say hello"""
    click.echo(format_text(f"Hello, {name}!", "success"))

# Register with Fuling
def register_commands(cli):
    cli.add_command(hello)
```

**Usage**:
```bash
# Add to your config.yaml
plugins:
  - ~/.config/fuling/plugins/my_commands.py

# Use the command
fl hello World
```

### 2. Add a Simple AI Provider

**File**: `~/.config/fuling/providers/custom_provider.py`
```python
from fuling.fuling_ai import AIProvider
from typing import Dict, Any, List, Optional

class CustomProvider(AIProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config.get('api_url', '')
    
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        # Your custom AI integration
        return "Response from custom provider"
    
    def explain_command(self, command: str, context: Optional[str] = None) -> str:
        return f"Custom explanation for: {command}"
```

## 📦 Plugin System

### Plugin Structure
```
my_fuling_plugin/
├── __init__.py
├── commands.py      # Custom commands
├── providers.py     # AI providers
├── themes.py        # Custom themes
└── config.yaml      # Plugin configuration
```

### Plugin Registration
```python
# In your plugin's __init__.py
from .commands import register_commands
from .providers import CustomProvider

__all__ = ['register_commands', 'CustomProvider']
```

### Configuration
```yaml
# config.yaml
plugins:
  - /path/to/plugin1
  - /path/to/plugin2
  
plugin_settings:
  plugin1:
    enabled: true
    config_key: value
```

## 🤖 Custom AI Providers

### Provider Interface
```python
from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    def chat_completion(self, messages: List[Dict], **kwargs) -> str:
        pass
    
    @abstractmethod
    def explain_command(self, command: str, context: str = None) -> str:
        pass
    
    @abstractmethod
    def suggest_commands(self, context: str = None) -> List[Dict]:
        pass
```

### Example: Local File Provider
```python
class FileProvider(AIProvider):
    def __init__(self, config):
        super().__init__(config)
        self.knowledge_file = config.get('knowledge_file', '')
    
    def explain_command(self, command, context=None):
        # Read from local knowledge base
        with open(self.knowledge_file, 'r') as f:
            knowledge = json.load(f)
        return knowledge.get(command, "Command not found in knowledge base")
```

## 🎨 Custom Themes

### Theme Structure
```python
from fuling.fuling_theme import Theme

class MyCustomTheme(Theme):
    def get_banner(self):
        return """
    ╔══════════════════════════╗
    ║     My Custom Theme      ║
    ╚══════════════════════════╝
    """
    
    def format_text(self, text, style=None):
        # Custom formatting logic
        symbols = {
            'success': '🎉',
            'error': '💥',
            'info': '💡',
        }
        symbol = symbols.get(style, '•')
        return f"{symbol} {text}"
```

### Register Theme
```python
# Add to your config.yaml
theme:
  name: "mycustom"
  # Theme configuration
```

## 🔌 Integration Examples

### 1. Integrate with Git
```python
@click.command()
@click.option('--message', '-m', required=True)
def git_commit(message):
    """Git commit with AI-generated message"""
    from fuling import chat_completion
    
    # Generate commit message using AI
    messages = [
        {"role": "system", "content": "Generate a git commit message"},
        {"role": "user", "content": f"Changes: {message}"}
    ]
    
    ai_message = chat_completion(messages)
    os.system(f'git commit -m "{ai_message}"')
```

### 2. System Monitoring Plugin
```python
@click.command()
def system_health():
    """Check system health"""
    import psutil
    
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    click.echo(f"CPU: {cpu}%")
    click.echo(f"Memory: {memory}%")
    click.echo(f"Disk: {disk}%")
```

### 3. Docker Helper
```python
@click.command()
@click.argument('service')
def docker_logs(service):
    """Show docker logs with filtering"""
    import subprocess
    
    # Get logs
    result = subprocess.run(
        ['docker', 'logs', '--tail', '100', service],
        capture_output=True,
        text=True
    )
    
    # Use AI to analyze logs
    from fuling import explain_command
    analysis = explain_command(f"docker logs analysis: {result.stdout[:500]}")
    
    click.echo(analysis)
```

## 🧪 Testing Extensions

### Unit Tests
```python
import pytest
from my_plugin.commands import hello

def test_hello_command():
    from click.testing import CliRunner
    
    runner = CliRunner()
    result = runner.invoke(hello, ['World'])
    
    assert result.exit_code == 0
    assert 'Hello' in result.output
```

### Integration Tests
```python
def test_plugin_integration():
    # Test that plugin loads correctly
    from fuling import get_config
    config = get_config()
    
    assert 'plugins' in config
    assert 'my_plugin' in config['plugins']
```

## 📁 Project Structure for Extensions

### Recommended Structure
```
fuling-extension/
├── pyproject.toml          # Package configuration
├── README.md              # Documentation
├── src/
│   └── fuling_extension/
│       ├── __init__.py
│       ├── commands.py
│       ├── providers.py
│       └── themes.py
├── tests/                 # Tests
└── examples/             # Usage examples
```

### Package Configuration
```toml
# pyproject.toml
[project]
name = "fuling-extension-example"
version = "0.1.0"
description = "Example extension for Fuling"

[project.entry-points."fuling.plugins"]
example = "fuling_extension:register_plugin"
```

## 🚀 Publishing Extensions

### 1. Package Your Extension
```bash
# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

### 2. Share on GitHub
```bash
# Create repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/fuling-extension.git
git push -u origin main
```

### 3. Community Sharing
- Add to Fuling's plugin registry
- Share in GitHub discussions
- Create documentation
- Provide examples

## 🔧 Advanced Topics

### 1. Configuration Management
```python
# Dynamic configuration
from fuling.fuling_core import get_config, config

def update_config():
    current = get_config()
    current['custom_key'] = 'value'
    config.save_config(current)
```

### 2. Event System
```python
# Subscribe to events
def on_command_executed(command, result):
    print(f"Command executed: {command}")
    # Log to file, send notification, etc.

# Register event handler
register_event_handler('command_executed', on_command_executed)
```

### 3. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_explanation(command):
    # Expensive operation
    return expensive_ai_call(command)
```

## 📚 Resources

### Official Documentation
- [Fuling API Reference](API_REFERENCE.md)
- [Plugin Development Guide](PLUGIN_DEVELOPMENT.md)
- [Theme Customization](THEME_CUSTOMIZATION.md)

### Community Resources
- [GitHub Repository](https://github.com/mai-xiyu/Fu-Ling-CLI)
- [Plugin Examples](https://github.com/mai-xiyu/Fu-Ling-CLI/tree/main/examples)
- [Discussion Forum](https://github.com/mai-xiyu/Fu-Ling-CLI/discussions)

### Tools and Libraries
- Click: CLI framework
- PyYAML: Configuration management
- Requests: HTTP client
- Pytest: Testing framework

---

**Start extending Fuling today! Check the examples directory for more inspiration.** 🚀