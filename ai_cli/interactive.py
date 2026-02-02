"""
Interactive mode for AI-CLI
"""

import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
import questionary

from ai_cli.core.config import get_config, update_config
from ai_cli.core.ai import test_model_connection, get_model
from ai_cli.commands.explain import explain_command
from ai_cli.commands.suggest import suggest_commands
from ai_cli.core.context import get_context

console = Console()

def interactive_setup():
    """Interactive setup wizard for AI-CLI"""
    
    console.print(Panel.fit(
        "[bold cyan]AI-CLI Interactive Setup[/]\n\n"
        "Let's configure your AI assistant step by step.",
        border_style="cyan"
    ))
    
    # Step 1: Choose AI provider
    provider = questionary.select(
        "Choose your AI provider:",
        choices=[
            questionary.Choice("Ollama (local, recommended)", value="ollama"),
            questionary.Choice("OpenAI (cloud, requires API key)", value="openai"),
            questionary.Choice("Local fallback (no AI)", value="local"),
        ],
        default="ollama"
    ).ask()
    
    config_updates = {'model': {'provider': provider}}
    
    # Step 2: Model selection based on provider
    if provider == "ollama":
        model = questionary.text(
            "Ollama model name:",
            default="phi3:mini",
            instruction="(e.g., llama3.2:3b, qwen2.5:0.5b, phi3:mini)"
        ).ask()
        config_updates['model']['name'] = model
        
        # Test Ollama connection
        console.print("\n[dim]Testing Ollama connection...[/]")
        try:
            import ollama
            models = ollama.list()
            if any(m['name'] == model for m in models.get('models', [])):
                console.print(f"[green]✓ Model '{model}' found[/]")
            else:
                console.print(f"[yellow]⚠ Model '{model}' not found locally[/]")
                console.print(f"[dim]Run: ollama pull {model}[/]")
        except ImportError:
            console.print("[yellow]⚠ Ollama not installed[/]")
            console.print("[dim]Install with: pip install ollama[/]")
        except Exception as e:
            console.print(f"[yellow]⚠ Connection failed: {e}[/]")
    
    elif provider == "openai":
        model = questionary.select(
            "OpenAI model:",
            choices=[
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
                "o1-preview",
                "o1-mini",
            ],
            default="gpt-4o"
        ).ask()
        config_updates['model']['name'] = model
        
        api_key = questionary.password("OpenAI API key:").ask()
        if api_key:
            config_updates['model']['api_key'] = api_key
        else:
            console.print("[yellow]⚠ No API key provided[/]")
    
    # Step 3: Configure features
    console.print("\n[bold]Feature Configuration[/]")
    
    features = {
        'auto_suggest': "Show command suggestions automatically",
        'explain_commands': "Explain commands before running",
        'safety_check': "Check commands for safety issues",
        'learn_patterns': "Learn from your usage patterns",
    }
    
    for feature, description in features.items():
        enabled = Confirm.ask(
            f"[cyan]{description}[/]",
            default=True
        )
        if 'features' not in config_updates:
            config_updates['features'] = {}
        config_updates['features'][feature] = enabled
    
    # Step 4: Temperature
    temperature = IntPrompt.ask(
        "[cyan]AI creativity (0-100)[/]",
        default=30,
        show_default=True
    )
    config_updates['model']['temperature'] = temperature / 100.0
    
    # Apply configuration
    try:
        update_config(config_updates)
        
        console.print(Panel.fit(
            "[bold green]✓ Configuration saved![/]\n\n"
            f"Provider: [cyan]{provider}[/]\n"
            f"Model: [cyan]{config_updates['model'].get('name', 'N/A')}[/]\n"
            f"Temperature: [cyan]{temperature/100:.2f}[/]\n\n"
            "[dim]Try these commands:[/]\n"
            "  ai find 'recent documents'\n"
            "  ai explain 'complex command'\n"
            "  ai suggest",
            title="Setup Complete",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[bold red]✗ Configuration failed:[/] {e}")
        return False
    
    return True

def interactive_mode():
    """Start interactive AI-CLI session"""
    
    console.print(Panel.fit(
        "[bold cyan]AI-CLI Interactive Mode[/]\n\n"
        "Type commands or ask questions. Type 'quit' to exit.",
        border_style="cyan"
    ))
    
    context = get_context()
    console.print(f"[dim]Current directory: {context['directory']}[/]")
    
    if context['git']['is_repo']:
        console.print(f"[dim]Git repo: {context['git']['branch']}[/]")
    
    history = []
    
    while True:
        try:
            # Get user input
            query = Prompt.ask("\n[bold cyan]›[/]")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("[dim]Goodbye![/]")
                break
            
            if not query.strip():
                continue
            
            # Add to history
            history.append(query)
            
            # Process command
            if query.startswith('find '):
                from ai_cli.commands.find import find_files
                results = find_files(query[5:])
                if results:
                    console.print(f"\n[bold]Found {len(results)} files:[/]")
                    for result in results[:10]:  # Show first 10
                        console.print(f"  • {result}")
                    if len(results) > 10:
                        console.print(f"  ... and {len(results) - 10} more")
                else:
                    console.print("[yellow]No files found[/]")
            
            elif query.startswith('explain '):
                explanation = explain_command(query[8:])
                console.print(Panel(
                    explanation,
                    title="[bold]Explanation[/]",
                    border_style="blue"
                ))
            
            elif query == 'suggest':
                suggestions = suggest_commands(context=context)
                if suggestions:
                    console.print("\n[bold]Suggestions:[/]")
                    for i, (cmd, desc) in enumerate(suggestions, 1):
                        console.print(f"\n{i}. [green]{cmd}[/]")
                        console.print(f"   {desc}")
                else:
                    console.print("[yellow]No suggestions available[/]")
            
            elif query == 'context':
                # Show current context
                table = Table(title="Current Context")
                table.add_column("Key", style="cyan")
                table.add_column("Value", style="green")
                
                table.add_row("Directory", context['directory'])
                table.add_row("Files", str(len(context['contents'])))
                table.add_row("Git repo", "Yes" if context['git']['is_repo'] else "No")
                if context['git']['is_repo']:
                    table.add_row("Git branch", context['git']['branch'])
                
                console.print(table)
            
            elif query == 'help':
                console.print("\n[bold]Available commands:[/]")
                console.print("  find [query]      - Find files with natural language")
                console.print("  explain [command] - Explain what a command does")
                console.print("  suggest           - Get command suggestions")
                console.print("  context           - Show current context")
                console.print("  config            - Show configuration")
                console.print("  quit              - Exit interactive mode")
            
            elif query == 'config':
                from ai_cli.core.config import get_config
                config = get_config()
                console.print(f"\n[bold]Current model:[/] {config.get('model', {}).get('name', 'N/A')}")
            
            else:
                # Try to interpret as natural language
                console.print("[dim]Processing your query...[/]")
                
                # First, try to suggest a command
                suggestions = suggest_commands(query, context)
                if suggestions:
                    console.print("\n[bold]Try one of these:[/]")
                    for cmd, desc in suggestions[:3]:
                        console.print(f"  [green]{cmd}[/] - {desc}")
                else:
                    console.print("[yellow]I'm not sure what you want to do[/]")
                    console.print("[dim]Try: find, explain, or suggest[/]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            if len(history) > 0:
                console.print(f"[dim]Last command: {history[-1]}[/]")

def main():
    """Main entry point for interactive mode"""
    try:
        interactive_mode()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Fatal error:[/] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()