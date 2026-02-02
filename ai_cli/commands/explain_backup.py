"""
Explain shell commands
"""

import re
from typing import Dict, Any
from ai_cli.core.ai import generate_explanation
from ai_cli.core.config import get_feature_config

# Common command explanations (fallback)
COMMAND_EXPLANATIONS = {
    "ls": {
        "description": "List directory contents",
        "common_options": {
            "-l": "Long format listing",
            "-a": "Show hidden files",
            "-h": "Human readable sizes",
            "-t": "Sort by modification time",
        },
        "examples": [
            "ls -la: List all files with details",
            "ls *.py: List Python files",
        ]
    },
    "cd": {
        "description": "Change directory",
        "common_usage": [
            "cd /path/to/directory",
            "cd .. (go up one level)",
            "cd ~ (go to home directory)",
            "cd - (go to previous directory)",
        ]
    },
    "find": {
        "description": "Search for files in directory hierarchy",
        "common_patterns": [
            "find . -name '*.py': Find Python files",
            "find . -type f -mtime -7: Find files modified in last 7 days",
            "find . -size +1M: Find files larger than 1MB",
        ]
    },
    "grep": {
        "description": "Search text using patterns",
        "common_options": {
            "-r": "Recursive search",
            "-i": "Case insensitive",
            "-n": "Show line numbers",
            "-v": "Invert match",
        }
    },
    "ps": {
        "description": "Display information about running processes",
        "common_usage": [
            "ps aux: Show all processes",
            "ps -ef: Show full format listing",
        ]
    },
    "kill": {
        "description": "Send signal to processes",
        "warning": "Use with caution! Can terminate processes.",
        "common_signals": {
            "9": "SIGKILL (force termination)",
            "15": "SIGTERM (graceful termination)",
        }
    }
}

def explain_command_simple(command: str) -> str:
    """Simple explanation without AI"""
    # Extract base command
    parts = command.strip().split()
    if not parts:
        return "Empty command"
    
    base_cmd = parts[0]
    
    if base_cmd in COMMAND_EXPLANATIONS:
        info = COMMAND_EXPLANATIONS[base_cmd]
        explanation = f"# {base_cmd}: {info['description']}\n\n"
        
        if "common_options" in info:
            explanation += "## Common Options:\n"
            for opt, desc in info["common_options"].items():
                explanation += f"- `{opt}`: {desc}\n"
            explanation += "\n"
        
        if "common_patterns" in info:
            explanation += "## Common Patterns:\n"
            for pattern in info["common_patterns"]:
                explanation += f"- `{pattern}`\n"
            explanation += "\n"
        
        if "common_usage" in info:
            explanation += "## Common Usage:\n"
            for usage in info["common_usage"]:
                explanation += f"- `{usage}`\n"
            explanation += "\n"
        
        if "warning" in info:
            explanation += f"⚠️ **Warning**: {info['warning']}\n\n"
        
        explanation += f"## Your Command:\n`{command}`\n"
        return explanation
    
    # Try to guess based on command pattern
    if command.startswith("sudo"):
        return f"# sudo: Execute command with superuser privileges\n\n`{command}`\n\n⚠️ **Warning**: This command runs with administrative privileges. Make sure you trust it!"
    
    elif "|" in command:
        return f"# Pipeline Command\n\n`{command}`\n\nThis uses pipes (`|`) to pass output from one command to another."
    
    elif ">" in command or ">>" in command:
        return f"# Output Redirection\n\n`{command}`\n\nThis redirects output to a file (`>` overwrites, `>>` appends)."
    
    elif "&&" in command:
        return f"# Command Chaining\n\n`{command}`\n\nRuns commands sequentially (`&&` means run next command only if previous succeeds)."
    
    else:
        return f"# Command: `{command}`\n\nI don't have a detailed explanation for this command. Consider using AI explanation with `ai explain --ai`."

def explain_command(command: str, use_ai: bool = None) -> str:
    """
    Explain what a shell command does
    
    Args:
        command: The shell command to explain
        use_ai: Whether to use AI (None = auto based on config)
    
    Returns:
        Explanation of the command
    """
    if not command or not command.strip():
        return "Please provide a command to explain."
    
    command = command.strip()
    
    # Auto-decide whether to use AI
    if use_ai is None:
        features = get_feature_config()
        use_ai = features.get("explain_commands", True)
    
    if use_ai:
        try:
            return generate_explanation(command)
        except Exception as e:
            print(f"AI explanation failed: {e}")
            # Fall back to simple explanation
            return explain_command_simple(command)
    else:
        return explain_command_simple(command)

def analyze_command_safety(command: str) -> Dict[str, Any]:
    """Analyze command for potential safety issues"""
    safety_issues = []
    warnings = []
    
    command_lower = command.lower()
    
    # Dangerous patterns
    dangerous_patterns = [
        (r"rm\s+-rf\s+/", "DANGEROUS: Deleting root directory"),
        (r"rm\s+-rf\s+~", "DANGEROUS: Deleting home directory"),
        (r":\(\)\{:\|:&\};:", "Fork bomb"),
        (r"mkfs\.|dd\s+if=/dev/", "Formatting disk"),
        (r"chmod\s+[0-7]{3,4}\s+/", "Changing permissions on system directories"),
    ]
    
    for pattern, warning in dangerous_patterns:
        if re.search(pattern, command):
            safety_issues.append(warning)
    
    # Warning patterns
    warning_patterns = [
        (r"sudo\s+", "Running with superuser privileges"),
        (r"rm\s+-rf", "Recursive force delete"),
        (r">\s+/dev/sd", "Writing to disk device"),
        (r"curl\s+.*\s+\|\s+bash", "Piping curl to bash"),
    ]
    
    for pattern, warning in warning_patterns:
        if re.search(pattern, command):
            warnings.append(warning)
    
    # Check for data loss risk
    if "rm " in command_lower and not ("-i" in command_lower or "--interactive" in command_lower):
        warnings.append("Deleting files without interactive confirmation")
    
    return {
        "safe": len(safety_issues) == 0,
        "safety_issues": safety_issues,
        "warnings": warnings,
        "recommendation": "Consider adding -i flag for interactive mode" if "rm " in command_lower else None,
    }

def format_safety_analysis(analysis: Dict[str, Any]) -> str:
    """Format safety analysis for display"""
    if analysis["safe"] and not analysis["warnings"]:
        return "✅ Command appears safe"
    
    result = ""
    
    if not analysis["safe"]:
        result += "🚨 **SAFETY ISSUES DETECTED**:\n"
        for issue in analysis["safety_issues"]:
            result += f"- {issue}\n"
        result += "\n"
    
    if analysis["warnings"]:
        result += "⚠️ **Warnings**:\n"
        for warning in analysis["warnings"]:
            result += f"- {warning}\n"
        result += "\n"
    
    if analysis["recommendation"]:
        result += f"💡 **Recommendation**: {analysis['recommendation']}\n"
    
    return result.strip()