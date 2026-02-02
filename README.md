# Fuling (符灵) - Intelligent CLI Assistant

<div align="center">

![Fuling Logo](docs/images/fuling_logo.png)

**Ancient Talisman Spirit · Modern AI Intelligence**

[English](README.md) | [中文](README_CN.md)

</div>

## 🎯 Introduction

**Fuling** (符灵, Fú Líng) is an intelligent command-line assistant that blends ancient talisman culture with modern AI technology. It combines traditional CLI tools with artificial intelligence to provide developers and system administrators with a smarter, more efficient working experience.

### ✨ Core Concept

```
符 (Fú) - Ancient talisman, representing mystical power and wisdom
灵 (Líng) - Spirit, intelligence, representing AI and modern technology

Fuling: The ancient talisman spirit revived in modern times as an intelligent assistant
```

## 🚀 Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/yourusername/fuling.git
cd fuling
pip install -e .

# Or use directly (under development)
python fuling_cli.py --help
```

### Initialization

```bash
# Initialize Fuling configuration
fl init

# Set AI provider API key (optional)
export MOONSHOT_API_KEY='your_api_key_here'
```

### Basic Usage

```bash
# Explain shell commands
fl explain "ls -la"

# Generate code
fl generate "python function for fibonacci sequence" -l python

# Chat with Fuling
fl chat

# Check system status
fl power

# Get daily fortune (random command suggestions)
fl fortune
```

## 🔮 Core Features

### 1. Intelligent Command Explanation
```bash
fl explain "docker run -d nginx"
# Output: Container Talisman: Summon nginx container spirit from the void and run in background
```

### 2. AI Code Generation
```bash
fl generate "quick sort algorithm" -l python -o quicksort.py
fl generate "React button component" -l javascript
fl generate "users table SQL" -l sql
```

### 3. Interactive Chat
```bash
fl chat
# Enter interactive mode to:
# - Ask technical questions
# - Request code help
# - Discuss best practices
```

### 4. System Status Monitoring
```bash
fl power
# Displays:
# - AI connection status
# - System information
# - Configuration status
```

### 5. Wisdom Library
```bash
fl wisdom
# Get usage suggestions, best practices, command references
```

## 🎨 Theme System

Fuling supports multiple themes for different usage scenarios:

```bash
# Ancient theme (default)
fl init --theme ancient

# Modern theme
fl init --theme modern

# Dark theme
fl init --theme dark

# Light theme
fl init --theme light
```

### Theme Previews

**Ancient Theme**:
```
    ██▓▓▓▓██
    ▓▓    ▓▓    Fuling v0.1.0
    ▓▓  ██▓▓    Intelligent CLI Assistant
    ▓▓▓▓██▓▓
    ▓▓  ▓▓▓▓    Ancient Wisdom · Modern AI
    ██▓▓▓▓██
```

**Modern Theme**:
```
    ╔══════════╗
    ║  Fuling  ║
    ║ v0.1.0   ║
    ╚══════════╝
    Intelligent CLI Assistant
```

## 🔌 AI Provider Support

Fuling supports multiple AI backends:

### Currently Supported:
- **Moonshot (Kimi)** - Recommended, Chinese optimized
- **OpenAI** - ChatGPT compatible
- **Local Mode** - Offline basic functionality

### Configuration Example:
```yaml
# ~/.config/fuling/config.yaml
model:
  provider: "moonshot"  # moonshot | openai | local
  name: "kimi-k2-turbo-preview"
  api_key: "${MOONSHOT_API_KEY}"
  temperature: 0.3
  max_tokens: 1000
```

## 📁 Project Structure

```
fuling/
├── fuling_cli.py          # Main CLI entry point
├── fuling_core.py         # Core configuration management
├── fuling_ai.py           # AI integration module
├── fuling_theme.py        # Theme system
├── config/               # Configuration files
│   └── themes/          # Theme definitions
├── docs/                 # Documentation
│   ├── README_CN.md     # Chinese documentation
│   ├── README.md        # English documentation
│   ├── QUICK_START.md   # Quick start guide
│   └── API_REFERENCE.md # API reference
├── examples/             # Usage examples
└── tests/               # Test files
```

## 🛠️ Development Guide

### Environment Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/fuling.git
cd fuling

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Development installation
pip install -e .
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_cli.py

# With coverage report
pytest --cov=fuling tests/
```

### Code Standards
```bash
# Code formatting
black fuling_cli.py fuling_core.py fuling_ai.py

# Code linting
flake8 fuling_cli.py fuling_core.py fuling_ai.py

# Type checking (optional)
mypy fuling_cli.py fuling_core.py fuling_ai.py
```

## 📚 Documentation Index

### User Documentation
- [Quick Start](docs/QUICK_START.md) - Get started in 5 minutes
- [Command Reference](docs/COMMAND_REFERENCE.md) - All commands explained
- [Configuration Guide](docs/CONFIGURATION.md) - Detailed configuration
- [Theme Customization](docs/THEMES.md) - Theme system usage
- [AI Providers](docs/AI_PROVIDERS.md) - AI backend configuration

### Developer Documentation
- [Architecture](docs/ARCHITECTURE.md) - System architecture
- [API Reference](docs/API_REFERENCE.md) - Module APIs
- [Plugin Development](docs/PLUGIN_DEVELOPMENT.md) - Developing plugins
- [Contributing Guide](docs/CONTRIBUTING.md) - How to contribute
- [Release Process](docs/RELEASE_PROCESS.md) - Version releases

### Examples
- [Basic Usage](examples/basic_usage.py)
- [Code Generation](examples/code_generation.py)
- [Automation Scripts](examples/automation.py)
- [Plugin Example](examples/plugin_example.py)

## 🚀 Roadmap

### v0.1.0 (Current)
- ✅ Basic CLI framework
- ✅ Command explanation
- ✅ Local knowledge base
- ✅ Theme system foundation
- ✅ Multi-AI provider architecture

### v0.2.0 (In Development)
- 🔄 Real AI integration
- 🔄 Code generation optimization
- 🔄 Plugin system framework
- 🔄 Performance monitoring
- 🔄 Complete documentation

### v0.3.0 (Planned)
- 📅 Advanced code refactoring
- 📅 Team collaboration features
- 📅 Visual interface
- 📅 Plugin marketplace
- 📅 Cloud sync

### v1.0.0 (Target)
- 🎯 Production ready
- 🎯 Complete test coverage
- 🎯 Community ecosystem
- 🎯 Enterprise features
- 🎯 Multi-language support

## 🤝 Contributing

We welcome all forms of contributions!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Standards
- Follow PEP 8 code style
- Add appropriate type annotations
- Write unit tests
- Update relevant documentation
- Maintain backward compatibility

### Reporting Issues
Please use [GitHub Issues](https://github.com/yourusername/fuling/issues) to report bugs or suggest features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Thanks to the following projects and technologies for inspiration:
- [OpenClaw](https://github.com/openclaw/openclaw) - Open source AI assistant framework
- [Moonshot AI](https://www.moonshot.cn/) - Kimi intelligent assistant
- [Click](https://click.palletsprojects.com/) - Python CLI framework
- [Rich](https://github.com/Textualize/rich) - Terminal beautification library

## 📞 Contact

- **Maintainer**: deepseek-chat-v3
- **Email**: kawinkhae.101@gmail.com
- **GitHub**: [mai-xiyu/Fu-Ling-CLI](https://github.com/mai-xiyu/Fu-Ling-CLI)
- **Issue Tracker**: [GitHub Issues](https://github.com/mai-xiyu/Fu-Ling-CLI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mai-xiyu/Fu-Ling-CLI/discussions)

---

<div align="center">

**Fuling - Making CLI Smarter, Development More Efficient**

![Fuling](docs/images/fuling_banner.png)

</div>