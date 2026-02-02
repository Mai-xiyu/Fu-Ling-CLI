#!/usr/bin/env python3
"""
Demo script for AI-CLI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def demo():
    console.print(Panel(
        "[bold cyan]AI-CLI Demo[/bold cyan]\n"
        "An intelligent CLI assistant with AI capabilities",
        border_style="cyan"
    ))
    
    # Show what we've built
    console.print("\n[bold]What we've built:[/bold]")
    
    features = [
        "✅ [green]CLI Framework[/green]: Full Click-based command line interface",
        "✅ [green]Configuration System[/green]: YAML-based config with defaults",
        "✅ [green]Context Awareness[/green]: Git status, directory contents, system info",
        "✅ [green]AI Integration[/green]: Support for Ollama, OpenAI, and local models",
        "✅ [green]Core Commands[/green]: find, explain, suggest, history, learn",
        "✅ [green]Safety Features[/green]: Command analysis and warnings",
        "✅ [green]Rich Output[/green]: Beautiful terminal formatting",
        "✅ [green]Extensible Architecture[/green]: Easy to add new commands",
    ]
    
    for feature in features:
        console.print(f"  {feature}")
    
    # Show project structure
    console.print("\n[bold]Project Structure:[/bold]")
    structure = """
ai-cli/
├── ai_cli/
│   ├── cli.py              # Main CLI entry point
│   ├── core/
│   │   ├── config.py       # Configuration management
│   │   ├── context.py      # Context awareness
│   │   └── ai.py           # AI model integration
│   └── commands/
│       ├── find.py         # Find files with AI
│       └── explain.py      # Command explanation
├── setup.py                # Package installation
├── README.md              # Comprehensive documentation
└── examples/              # Usage examples
    """
    console.print(structure)
    
    # Show usage examples
    console.print("\n[bold]Usage Examples:[/bold]")
    
    examples = [
        ("Find files", "ai find 'python files modified today'"),
        ("Explain command", "ai explain 'find . -name \"*.py\" -exec grep -l import {} \\;'"),
        ("Get suggestions", "ai suggest 'I need to clean up temporary files'"),
        ("Search history", "ai history 'git commands'"),
        ("Create alias", "ai alias cleanup 'find . -name \"*.pyc\" -delete'"),
    ]
    
    for desc, cmd in examples:
        console.print(f"  [cyan]{desc}:[/cyan]")
        console.print(f"    [yellow]$ {cmd}[/yellow]")
    
    # Show next steps
    console.print("\n[bold]Next Steps:[/bold]")
    next_steps = [
        "1. Install dependencies: `pip install click rich pyyaml`",
        "2. Try it out: `python -m ai_cli.cli --help`",
        "3. Initialize config: `python -m ai_cli.cli init`",
        "4. Install Ollama for AI features: https://ollama.com",
        "5. Star the repo on GitHub! ⭐",
    ]
    
    for step in next_steps:
        console.print(f"  {step}")
    
    console.print("\n[bold]GitHub Repository:[/bold]")
    console.print("  https://github.com/xiyu-bot-assistant/ai-cli")
    
    console.print("\n[bold]Goal:[/bold] Create a useful tool that gains traction,")
    console.print("attracts contributors, and potentially gets acquired!")
    console.print("\n[italic]'Making terminals smarter, one command at a time.'[/italic]")

if __name__ == "__main__":
    demo()