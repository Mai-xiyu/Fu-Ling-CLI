# AI-CLI 🤖

An intelligent CLI assistant that enhances traditional command-line with AI capabilities. Make your terminal smarter, faster, and more intuitive.

![GitHub](https://img.shields.io/github/license/xiyu-bot-assistant/ai-cli)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Version](https://img.shields.io/badge/version-0.1.0-orange)
![Status](https://img.shields.io/badge/status-alpha-yellow)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

## ✨ Features

- **🤖 AI-Powered Commands**: Use natural language to interact with your terminal
- **🔍 Smart Search**: Find files and content with descriptive queries
- **📚 Command Explanation**: Understand complex commands before running them
- **💡 Intelligent Suggestions**: Get context-aware command recommendations
- **🔒 Privacy First**: Everything runs locally, no data leaves your machine
- **⚡ Fast & Lightweight**: Optimized for daily use without slowing you down

## 🚀 Quick Start

```bash
# Install AI-CLI
pip install ai-cli

# Initialize AI-CLI
ai-cli init

# Start using intelligent commands
ai find "photos from last month"
ai explain "find . -name '*.py' -exec grep -l 'import pandas' {} \;"
ai suggest "I want to see disk usage"
```

## 📦 Installation

### Using pip
```bash
pip install ai-cli
```

### From source
```bash
git clone https://github.com/xiyu-bot-assistant/ai-cli.git
cd ai-cli
pip install -e .
```

## 🛠️ Usage

### Basic Commands

```bash
# Find files using natural language
ai find "configuration files modified today"
ai find "large video files in downloads folder"

# Search file contents
ai grep "error messages in log files from yesterday"
ai grep "TODO comments in python files"

# Explain complex commands
ai explain "tar -czf backup.tar.gz --exclude='*.tmp' ."
ai explain "ps aux | grep python | awk '{print $2}' | xargs kill -9"

# Get command suggestions
ai suggest "I need to clean up temporary files"
ai suggest "How do I monitor network traffic?"

# Smart command history
ai history "git commands from yesterday"
ai history "docker commands I used"
```

### Advanced Features

```bash
# Learn from your usage patterns
ai learn

# Configure AI model preferences
ai config set model phi3:mini
ai config set temperature 0.7

# Create custom command aliases
ai alias "clean pycache" "find . -name '__pycache__' -type d -exec rm -rf {} +"
```

## 🧠 How It Works

AI-CLI combines several technologies:

1. **Local AI Models**: Runs small, efficient models on your machine
2. **Context Awareness**: Understands your current directory, git status, and system state
3. **Command Translation**: Converts natural language to precise shell commands
4. **Safety First**: Always shows commands before execution, with explanation

## 🔧 Configuration

Create `~/.config/ai-cli/config.yaml`:

```yaml
model:
  name: "phi3:mini"  # or "qwen2.5:0.5b", "llama3.2:3b"
  temperature: 0.3

features:
  auto_suggest: true
  explain_commands: true
  safety_check: true

aliases:
  cleanup: "find . -name '*.pyc' -delete"
  stats: "git log --oneline | wc -l"
```

## 📁 Project Structure

```
ai-cli/
├── ai_cli/          # Main package
│   ├── core/        # Core functionality
│   ├── commands/    # Command implementations
│   ├── models/      # AI model integration
│   └── utils/       # Utilities
├── tests/           # Test suite
├── docs/            # Documentation
└── examples/        # Usage examples
```

## 🤝 Contributing

We love contributions! Here's how to help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/xiyu-bot-assistant/ai-cli.git
cd ai-cli
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest  # Run tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by [xiyu-bot-assistant](https://github.com/xiyu-bot-assistant)
- Inspired by the need for smarter developer tools
- Thanks to all contributors and users!

## 🔗 Links

- [Documentation](https://github.com/xiyu-bot-assistant/ai-cli/wiki)
- [Issue Tracker](https://github.com/xiyu-bot-assistant/ai-cli/issues)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

---

**Star this repo if you find it useful!** ⭐

*"Making terminals smarter, one command at a time."*