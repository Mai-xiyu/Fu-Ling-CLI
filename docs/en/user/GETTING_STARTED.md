# Getting Started with Fuling

## 🚀 Quick Start (5 Minutes)

### 1. Installation
```bash
# Clone and install
git clone https://github.com/mai-xiyu/Fu-Ling-CLI.git
cd Fu-Ling-CLI
pip install -e .

# Or install directly (when available on PyPI)
# pip install fuling
```

### 2. First Run
```bash
# Initialize Fuling
fl init

# Test basic functionality
fl explain "ls -la"
fl wisdom
fl power
```

### 3. Choose Your AI Provider
```bash
# Configure AI provider (interactive)
fl config

# Options:
# - Moonshot (Kimi) - Recommended for Chinese
# - OpenAI - International standard
# - Local mode - No API key needed
```

## 📋 Core Commands Cheat Sheet

### Essential Commands
```bash
# Explain shell commands
fl explain "docker run"
fl explain "git commit -m" --context "version control"

# Generate code
fl generate "python quick sort" -l python
fl generate "react button component" -l javascript -o Button.js

# Chat with AI
fl chat

# Get help and suggestions
fl wisdom
fl fortune
```

### System Management
```bash
# Check system status
fl power

# Configure settings
fl config

# Update configuration
fl init --theme modern  # Change theme
```

## 🎯 Common Use Cases

### For Developers
```bash
# Explain complex commands
fl explain "kubectl apply -f deployment.yaml"

# Generate boilerplate code
fl generate "fastapi endpoint for users" -l python -o users.py

# Get command suggestions
fl fortune
```

### For System Administrators
```bash
# Monitor system
fl power

# Learn new commands
fl explain "netstat -tulpn"
fl explain "journalctl -f"

# Get troubleshooting tips
fl wisdom
```

### For Learning
```bash
# Interactive learning
fl chat
# Ask: "What does 'grep -r pattern .' do?"
# Ask: "How to find large files?"

# Daily practice
fl fortune  # Get random command to learn
```

## 🔧 Configuration Guide

### Basic Configuration
```bash
# Initialize with specific theme
fl init --theme dark

# Configure AI provider
fl config
# Follow interactive prompts
```

### Environment Variables
```bash
# Set API keys (optional)
export MOONSHOT_API_KEY='your_key'      # For Moonshot
export OPENAI_API_KEY='your_key'        # For OpenAI

# Theme preferences (optional)
export FULING_THEME='modern'
export FULING_LANGUAGE='en'
```

### Configuration Files
- **Main config**: `~/.config/fuling/config.yaml`
- **Cache**: `~/.cache/fuling/`
- **Logs**: `~/.local/share/fuling/logs/`

## 🎨 Customization

### Themes
```bash
# Available themes
fl init --theme ancient   # Ancient style (default)
fl init --theme modern    # Modern minimal
fl init --theme dark      # Dark mode
fl init --theme light     # Light mode
```

### Language
```bash
# Set language in config.yaml
language: "en"  # or "zh" for Chinese
```

## 🚨 Troubleshooting

### Common Issues

**Issue**: `fl` command not found
```bash
# Reinstall
pip install -e .

# Check installation
which fl
```

**Issue**: API errors
```bash
# Check API key
echo $MOONSHOT_API_KEY

# Test connection
fl power

# Switch to local mode
fl config  # Choose "Local mode"
```

**Issue**: Slow responses
```bash
# Check network
fl power

# Use local mode temporarily
# Local mode works offline
```

## 📚 Next Steps

### Master Basic Features
1. ✅ Install and initialize
2. ✅ Learn core commands
3. ✅ Configure AI provider
4. ✅ Try different themes

### Explore Advanced Features
1. Use `fl generate` for code generation
2. Try `fl chat` for interactive help
3. Create custom configurations
4. Join the community

### Get Help
- Run `fl wisdom` for tips
- Run `fl --help` for command reference
- Check `docs/` for detailed documentation
- Join GitHub discussions

---

**You're ready to use Fuling! Start with `fl wisdom` for daily tips.** 🚀