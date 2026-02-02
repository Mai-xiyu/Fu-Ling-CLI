"""
Error handling utilities for AI-CLI
"""

import sys
from typing import Optional, Type
from rich.console import Console
from rich.panel import Panel
import traceback

console = Console()

class AICLIError(Exception):
    """Base exception for AI-CLI errors"""
    def __init__(self, message: str, hint: Optional[str] = None):
        self.message = message
        self.hint = hint
        super().__init__(message)

class ConfigError(AICLIError):
    """Configuration related errors"""
    pass

class AIError(AICLIError):
    """AI model related errors"""
    pass

class CommandError(AICLIError):
    """Command execution errors"""
    pass

class SafetyError(AICLIError):
    """Safety check errors"""
    pass

def handle_error(error: Exception, show_traceback: bool = False):
    """Handle and display errors gracefully"""
    
    if isinstance(error, AICLIError):
        # User-friendly error messages
        console.print(f"[bold red]Error:[/] {error.message}")
        if error.hint:
            console.print(f"[yellow]Hint:[/] {error.hint}")
    else:
        # Unexpected errors
        console.print(f"[bold red]Unexpected error:[/] {str(error)}")
        
        if show_traceback:
            console.print("\n[dim]Traceback:[/]")
            console.print(traceback.format_exc())
        else:
            console.print("[dim]Run with --debug for full traceback[/]")
    
    # Exit with appropriate code
    error_codes = {
        ConfigError: 78,      # EX_CONFIG
        AIError: 79,          # EX_SOFTWARE
        CommandError: 126,    # EX_CANTCREAT
        SafetyError: 1,       # General error
    }
    
    exit_code = error_codes.get(type(error), 1)
    sys.exit(exit_code)

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e)
        return None

def validate_command(command: str) -> bool:
    """Validate command for safety"""
    dangerous_patterns = [
        r"rm\s+-rf\s+/",      # Deleting root
        r":\(\)\{:\|:&\};:",  # Fork bomb
        r"mkfs\.",            # Format disk
        r"dd\s+if=/dev/",     # Disk operations
    ]
    
    import re
    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return False
    
    return True

def format_success(message: str) -> str:
    """Format success message"""
    return f"[bold green]✓[/] {message}"

def format_warning(message: str) -> str:
    """Format warning message"""
    return f"[bold yellow]⚠[/] {message}"

def format_error(message: str) -> str:
    """Format error message"""
    return f"[bold red]✗[/] {message}"

def format_info(message: str) -> str:
    """Format info message"""
    return f"[bold blue]ℹ[/] {message}"