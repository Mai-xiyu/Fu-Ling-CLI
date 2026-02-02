#!/usr/bin/env python3
"""
Main CLI entry point for AI-CLI
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
import sys
import os

from ai_cli.utils.errors import (
    handle_error, safe_execute, format_success,
    format_warning, format_error, format_info
)

console = Console()

def print_banner():
    """Print AI-CLI banner"""
    banner = """
    █████╗ ██╗      ██████╗██╗     ██╗
   ██╔══██╗██║     ██╔════╝██║     ██║
   ███████║██║     ██║     ██║     ██║
   ██╔══██║██║     ██║     ██║     ██║
   ██║  ██║███████╗╚██████╗███████╗██║
   ╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝
   
   Intelligent Command Line Assistant
   """
    
    console.print(Panel.fit(
        banner,
        title="[bold cyan]AI-CLI[/]",
        border_style="cyan",
        padding=(1, 2)
    ))

@click.group()
@click.version_option(
    package_name="ai-cli",
    message="%(prog)s %(version)s"
)
@click.option(
    '--debug',
    is_flag=True,
    help="Enable debug mode with tracebacks"
)
@click.pass_context
def cli(ctx, debug):
    """AI-CLI - Intelligent Command Line Assistant
    
    Make your terminal smarter, faster, and more intuitive.
    
    Examples:
      ai init                    # Initialize configuration
      ai find "python files"     # Find files with natural language
      ai explain "ls -la"        # Explain what a command does
      ai suggest                 # Get command suggestions
      ai config                  # Show current configuration
    """
    # Store debug flag in context
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    
    # Print banner on first run
    config_dir = os.path.expanduser("~/.config/ai-cli")
    config_file = os.path.join(config_dir, "config.yaml")
    
    if not os.path.exists(config_file):
        print_banner()
        console.print("[dim]Run 'ai init' to get started[/]")
    
    # 动态注册插件命令
    try:
        from ai_cli.core.dynamic_commands import register_plugin_commands
        register_plugin_commands(cli)
    except Exception as e:
        if debug:
            console.print(f"[dim]Dynamic command registration failed: {e}[/]")

@cli.command()
@click.option(
    '--model',
    default='phi3:mini',
    help='Default AI model to use'
)
@click.option(
    '--provider',
    type=click.Choice(['ollama', 'openai', 'local']),
    default='ollama',
    help='AI provider to use'
)
@click.pass_context
def init(ctx, model, provider):
    """Initialize AI-CLI configuration
    
    Creates configuration directory and sets up default settings.
    """
    from ai_cli.core.config import init_config, update_config
    
    console.print("[bold]Initializing AI-CLI...[/]")
    
    try:
        # Initialize with custom options
        config = init_config()
        
        # Update with provided options
        updates = {
            'model': {
                'name': model,
                'provider': provider,
                'temperature': 0.3
            }
        }
        
        update_config(updates)
        
        # Show success message
        console.print(Panel.fit(
            f"[bold green]✓ AI-CLI initialized successfully![/]\n\n"
            f"Configuration saved to: [dim]~/.config/ai-cli/config.yaml[/]\n"
            f"Default model: [cyan]{model}[/]\n"
            f"Provider: [cyan]{provider}[/]\n\n"
            f"[dim]Try these commands:[/]\n"
            f"  ai find 'python files'     # Find files\n"
            f"  ai explain 'ls -la'        # Explain commands\n"
            f"  ai suggest                 # Get suggestions",
            title="Ready to Go!",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[bold red]✗ Initialization failed:[/] {e}")
        if ctx.obj.get('DEBUG'):
            import traceback
            traceback.print_exc()
        sys.exit(1)

@cli.command()
@click.argument('query')
def find(query):
    """Find files using natural language"""
    from ai_cli.commands.find import find_files
    results = find_files(query)
    
    if results:
        console.print(f"\n[bold]Found {len(results)} files:[/bold]")
        for result in results:
            console.print(f"  • {result}")
    else:
        console.print("[yellow]No files found matching your query.[/yellow]")

@cli.command()
@click.argument('query')
def grep(query):
    """Search file contents using natural language"""
    from ai_cli.commands.grep import search_contents
    results = search_contents(query)
    
    if results:
        console.print(f"\n[bold]Found {len(results)} matches:[/bold]")
        for file_path, matches in results.items():
            console.print(f"\n[cyan]{file_path}:[/cyan]")
            for match in matches[:3]:  # Show first 3 matches per file
                console.print(f"  • {match}")
    else:
        console.print("[yellow]No matches found.[/yellow]")

@cli.command()
@click.argument('command')
def explain(command):
    """Explain what a command does"""
    from ai_cli.commands.explain import explain_command
    explanation = explain_command(command)
    
    console.print(Panel(
        Markdown(explanation),
        title="[bold]Command Explanation[/bold]",
        border_style="blue"
    ))

@cli.command()
@click.argument('query', required=False)
def suggest(query=None):
    """Get command suggestions"""
    from ai_cli.commands.suggest import suggest_commands
    
    if query:
        suggestions = suggest_commands(query)
    else:
        # Get context-aware suggestions
        from ai_cli.core.context import get_context
        context = get_context()
        suggestions = suggest_commands(context=context)
    
    if suggestions:
        console.print("\n[bold]Suggested commands:[/bold]")
        for i, (cmd, desc) in enumerate(suggestions, 1):
            console.print(f"\n{i}. [green]{cmd}[/green]")
            console.print(f"   {desc}")
    else:
        console.print("[yellow]No suggestions available.[/yellow]")

@cli.command()
@click.argument('query', required=False)
def history(query=None):
    """Search command history intelligently"""
    from ai_cli.commands.history import search_history
    
    results = search_history(query)
    
    if results:
        console.print(f"\n[bold]Found {len(results)} commands:[/bold]")
        for cmd, timestamp in results:
            console.print(f"  • [cyan]{timestamp}[/cyan] {cmd}")
    else:
        console.print("[yellow]No matching commands found in history.[/yellow]")

@cli.command()
def learn():
    """Learn from your usage patterns"""
    from ai_cli.core.learning import learn_patterns
    console.print("[italic]Analyzing your usage patterns...[/italic]")
    learn_patterns()
    console.print("[green]✓[/green] Learning complete!")

@cli.command()
@click.pass_context
def status(ctx):
    """Check AI-CLI system status
    
    Verify that all components are working correctly.
    """
    from ai_cli.core.ai import test_model_connection
    from ai_cli.core.config import get_config
    from ai_cli.core.plugins import get_plugin_manager
    import os
    from pathlib import Path
    
    console.print("[bold]AI-CLI System Status[/]")
    console.print("=" * 40)
    
    checks = []
    
    # Check 1: Configuration
    try:
        config = get_config()
        checks.append(("✅", "Configuration loaded"))
    except Exception as e:
        checks.append(("❌", f"Configuration failed: {e}"))
    
    # Check 2: Config directory
    config_dir = Path.home() / ".config" / "ai-cli"
    if config_dir.exists():
        checks.append(("✅", f"Config directory: {config_dir}"))
    else:
        checks.append(("❌", "Config directory missing"))
    
    # Check 3: AI model connection
    try:
        if test_model_connection():
            checks.append(("✅", "AI model connection OK"))
        else:
            checks.append(("⚠", "AI model not connected (run 'ai init')"))
    except Exception as e:
        checks.append(("❌", f"AI test failed: {e}"))
    
    # Check 4: Python dependencies
    try:
        import click
        import rich
        import yaml
        checks.append(("✅", "Python dependencies OK"))
    except ImportError as e:
        checks.append(("❌", f"Missing dependency: {e}"))
    
    # Check 5: Command availability
    try:
        from ai_cli.commands.explain import explain_command
        checks.append(("✅", "Commands loaded"))
    except Exception as e:
        checks.append(("❌", f"Command load failed: {e}"))
    
    # Check 6: Plugins
    try:
        plugin_manager = get_plugin_manager()
        plugin_count = len(plugin_manager.get_all_plugins())
        checks.append(("✅", f"Plugins loaded: {plugin_count}"))
    except Exception as e:
        checks.append(("⚠", f"Plugins: {e}"))
    
    # Display results
    for icon, message in checks:
        console.print(f"{icon} {message}")
    
    console.print("\n[bold]Quick Start:[/]")
    console.print("  1. Run 'ai init' to configure")
    console.print("  2. Try 'ai find \"python files\"'")
    console.print("  3. Use 'ai explain \"ls -la\"' for help")
    console.print("  4. Run 'ai plugin list' to see plugins")
    
    # Overall status
    all_ok = all(icon == "✅" for icon, _ in checks)
    if all_ok:
        console.print("\n[bold green]✓ All systems operational![/]")
    else:
        console.print("\n[bold yellow]⚠ Some issues detected[/]")
        console.print("  Run with --debug for details or 'ai init' to reconfigure")

@cli.command()
@click.argument('alias')
@click.argument('command')
def alias(alias, command):
    """Create a custom command alias"""
    from ai_cli.core.config import add_alias
    add_alias(alias, command)
    console.print(f"[green]✓[/green] Alias '{alias}' created for: {command}")

@cli.command()
@click.option(
    '--setup',
    is_flag=True,
    help='Run interactive setup wizard'
)
def interactive(setup):
    """Start interactive AI-CLI session
    
    Enter a conversational interface with AI-CLI.
    Type commands naturally and get intelligent responses.
    """
    if setup:
        from ai_cli.interactive import interactive_setup
        interactive_setup()
    else:
        from ai_cli.interactive import interactive_mode
        interactive_mode()

@cli.group()
def plugin():
    """Plugin management commands"""
    pass

@plugin.command(name='list')
def plugin_list():
    """List all loaded plugins"""
    from ai_cli.core.plugins import list_plugins_command
    list_plugins_command()

@plugin.command()
@click.argument('plugin_name')
def info(plugin_name):
    """Show plugin information"""
    from ai_cli.core.plugins import plugin_info_command
    plugin_info_command(plugin_name)

@cli.command()
def commands():
    """List all available commands"""
    from ai_cli.core.dynamic_commands import list_all_commands
    list_all_commands()

@cli.group()
def perf():
    """Performance monitoring commands"""
    pass

@perf.command(name='report')
def perf_report():
    """Show performance report"""
    from ai_cli.core.performance import show_performance_report
    show_performance_report()

@perf.command(name='resources')
def perf_resources():
    """Show system resources"""
    from ai_cli.core.performance import show_system_resources
    show_system_resources()

@perf.command(name='optimize')
def perf_optimize():
    """Optimize startup performance"""
    from ai_cli.core.performance import optimize_startup
    from rich.table import Table
    
    console.print("[bold]Optimizing startup performance...[/]")
    
    metrics = optimize_startup()
    
    table = Table(title="Startup Performance")
    table.add_column("Module", style="cyan")
    table.add_column("Import Time", style="green")
    table.add_column("Status", style="bold")
    
    import_times = metrics.get('import_times', {})
    total_time = 0
    
    for module, import_time in import_times.items():
        if import_time >= 0:
            status = "✅" if import_time < 0.01 else "⚠" if import_time < 0.1 else "❌"
            table.add_row(module, f"{import_time:.4f}s", status)
            total_time += import_time
        else:
            table.add_row(module, "N/A", "❌")
    
    console.print(table)
    console.print(f"\n[bold]Total startup time:[/] {total_time:.4f}s")
    
    if total_time > 0.5:
        console.print("[yellow]⚠ Startup time is high. Consider lazy loading.[/]")
    else:
        console.print("[green]✓ Startup performance is good![/]")

@cli.command()
@click.option(
    '--show-paths',
    is_flag=True,
    help='Show configuration file paths'
)
@click.pass_context
def config(ctx, show_paths):
    """Show current configuration
    
    Display all AI-CLI configuration settings in a readable format.
    """
    from ai_cli.core.config import get_config, CONFIG_FILE, CONFIG_DIR
    from pathlib import Path
    
    try:
        config = get_config()
        
        # Create a table for better display
        table = Table(
            title="[bold green]AI-CLI Configuration[/]",
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        # Model settings
        model_config = config.get('model', {})
        table.add_row("Model Name", model_config.get('name', 'N/A'))
        table.add_row("Provider", model_config.get('provider', 'N/A'))
        table.add_row("Temperature", str(model_config.get('temperature', 'N/A')))
        table.add_row("", "")  # Empty row for spacing
        
        # Feature settings
        features = config.get('features', {})
        for feature, enabled in features.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            table.add_row(f"Feature: {feature}", status)
        
        # Aliases
        aliases = config.get('aliases', {})
        if aliases:
            table.add_row("", "")  # Empty row
            table.add_row("[bold]Aliases[/]", "")
            for alias, command in aliases.items():
                table.add_row(f"  {alias}", f"[dim]{command}[/]")
        
        console.print(table)
        
        # Show paths if requested
        if show_paths:
            console.print("\n[bold]Configuration Paths:[/]")
            console.print(f"  Config file: [dim]{CONFIG_FILE}[/]")
            console.print(f"  Config dir:  [dim]{CONFIG_DIR}[/]")
            
            # Check if files exist
            if CONFIG_FILE.exists():
                console.print(f"  [green]✓ Config file exists[/]")
            else:
                console.print(f"  [yellow]⚠ Config file missing[/]")
                
    except Exception as e:
        console.print(f"[bold red]✗ Failed to load configuration:[/] {e}")
        if ctx.obj.get('DEBUG'):
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()