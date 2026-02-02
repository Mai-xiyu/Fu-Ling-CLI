"""
Command suggestions for AI-CLI
"""

from typing import List, Tuple, Optional, Dict, Any
from ai_cli.core.ai import generate_suggestions
from ai_cli.core.context import get_context

def suggest_commands(query: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> List[Tuple[str, str]]:
    """
    Generate command suggestions based on query or context
    
    Args:
        query: Optional natural language query
        context: Optional context dictionary
    
    Returns:
        List of (command, description) tuples
    """
    if context is None:
        context = get_context()
    
    try:
        suggestions = generate_suggestions(context, query)
        
        # Format suggestions
        result = []
        for suggestion in suggestions:
            if isinstance(suggestion, dict):
                cmd = suggestion.get('command', '')
                desc = suggestion.get('description', '')
                if cmd:
                    result.append((cmd, desc))
            elif isinstance(suggestion, str):
                result.append((suggestion, 'Suggested command'))
        
        return result[:5]  # Return top 5 suggestions
    
    except Exception:
        # Fallback suggestions based on context
        return get_fallback_suggestions(context, query)

def get_fallback_suggestions(context: Dict[str, Any], query: Optional[str] = None) -> List[Tuple[str, str]]:
    """Fallback suggestions when AI is not available"""
    
    suggestions = []
    
    # Git-related suggestions
    if context['git']['is_repo']:
        suggestions.extend([
            ("git status", "Check git repository status"),
            ("git log --oneline -10", "Show recent commits"),
            ("git diff", "Show unstaged changes"),
        ])
        
        if context['git']['staged']:
            suggestions.append(("git commit -m 'message'", "Commit staged changes"))
        
        if context['git']['unstaged']:
            suggestions.append(("git add .", "Stage all changes"))
    
    # File-related suggestions
    file_types = context['file_types']
    if '.py' in file_types:
        suggestions.extend([
            ("python3 -m pytest", "Run Python tests"),
            ("python3 -m black .", "Format Python code"),
            ("python3 -m flake8", "Check Python style"),
        ])
    
    if '.js' in file_types or '.ts' in file_types:
        suggestions.append(("npm test", "Run JavaScript tests"))
    
    # System suggestions
    suggestions.extend([
        ("ls -la", "List files with details"),
        ("df -h", "Show disk usage"),
        ("free -h", "Show memory usage"),
        ("ps aux | head -20", "Show running processes"),
    ])
    
    # Query-specific fallbacks
    if query:
        query_lower = query.lower()
        
        if 'find' in query_lower or 'search' in query_lower:
            if 'python' in query_lower:
                suggestions.insert(0, ("find . -name '*.py'", "Find Python files"))
            elif 'today' in query_lower:
                suggestions.insert(0, ("find . -type f -mtime 0", "Find files modified today"))
            else:
                suggestions.insert(0, ("find . -type f", "Find all files"))
        
        elif 'clean' in query_lower or 'delete' in query_lower:
            suggestions.insert(0, ("find . -name '*.pyc' -delete", "Delete Python cache files"))
            suggestions.insert(0, ("find . -name '__pycache__' -type d -exec rm -rf {} +", "Delete __pycache__ directories"))
        
        elif 'disk' in query_lower or 'space' in query_lower:
            suggestions.insert(0, ("du -sh * | sort -hr", "Show directory sizes"))
            suggestions.insert(0, ("ncdu", "Interactive disk usage (install with apt)"))
    
    # Add context-specific suggestions
    if len(context['contents']) > 50:
        suggestions.insert(0, ("ls | wc -l", f"Count files ({len(context['contents'])} total)"))
    
    # Ensure we have at least some suggestions
    if not suggestions:
        suggestions = [
            ("pwd", "Show current directory"),
            ("ls", "List files"),
            ("date", "Show current date and time"),
        ]
    
    return suggestions[:5]