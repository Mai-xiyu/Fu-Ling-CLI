"""
Context awareness for AI-CLI
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import json

def get_current_directory() -> str:
    """Get current working directory"""
    return os.getcwd()

def get_directory_contents() -> List[str]:
    """Get contents of current directory"""
    try:
        return os.listdir('.')
    except:
        return []

def get_git_status() -> Dict[str, Any]:
    """Get git repository status"""
    status = {
        "is_repo": False,
        "branch": None,
        "status": None,
        "staged": [],
        "unstaged": [],
        "untracked": [],
    }
    
    try:
        # Check if we're in a git repo
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return status
        
        status["is_repo"] = True
        
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            status["branch"] = result.stdout.strip()
        
        # Get git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line:
                    code = line[:2]
                    file = line[3:]
                    
                    if code == '??':
                        status["untracked"].append(file)
                    elif code[0] != ' ':
                        status["staged"].append(file)
                    elif code[1] != ' ':
                        status["unstaged"].append(file)
        
        return status
    except:
        return status

def get_system_info() -> Dict[str, Any]:
    """Get basic system information"""
    info = {
        "platform": os.name,
        "shell": os.environ.get("SHELL", "unknown"),
        "user": os.environ.get("USER", "unknown"),
        "home": os.environ.get("HOME", ""),
    }
    
    # Try to get more info if available
    try:
        import platform
        info["system"] = platform.system()
        info["release"] = platform.release()
        info["machine"] = platform.machine()
    except:
        pass
    
    return info

def get_recent_commands(count: int = 10) -> List[str]:
    """Get recent shell commands from history"""
    commands = []
    
    # Try different shell history files
    history_files = [
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.zsh_history"),
        os.path.expanduser("~/.history"),
    ]
    
    for hist_file in history_files:
        if os.path.exists(hist_file):
            try:
                with open(hist_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    commands.extend(line.strip() for line in lines[-count:] if line.strip())
                break
            except:
                continue
    
    return commands[-count:]

def get_file_types() -> Dict[str, int]:
    """Analyze file types in current directory"""
    file_types = {}
    
    try:
        for item in os.listdir('.'):
            if os.path.isfile(item):
                ext = os.path.splitext(item)[1]
                if ext:
                    file_types[ext] = file_types.get(ext, 0) + 1
                else:
                    file_types["no_extension"] = file_types.get("no_extension", 0) + 1
            elif os.path.isdir(item):
                file_types["directory"] = file_types.get("directory", 0) + 1
    except:
        pass
    
    return file_types

def get_context() -> Dict[str, Any]:
    """Get comprehensive context information"""
    return {
        "directory": get_current_directory(),
        "contents": get_directory_contents(),
        "git": get_git_status(),
        "system": get_system_info(),
        "recent_commands": get_recent_commands(5),
        "file_types": get_file_types(),
        "environment": {
            "path": os.environ.get("PATH", "").split(':'),
            "editor": os.environ.get("EDITOR", ""),
            "lang": os.environ.get("LANG", ""),
        }
    }

def format_context_for_prompt(context: Dict[str, Any]) -> str:
    """Format context information for AI prompt"""
    lines = []
    
    # Current directory
    lines.append(f"Current directory: {context['directory']}")
    
    # Git status
    git = context['git']
    if git['is_repo']:
        lines.append(f"Git repository: {git['branch']}")
        if git['staged']:
            lines.append(f"Staged changes: {len(git['staged'])} files")
        if git['unstaged']:
            lines.append(f"Unstaged changes: {len(git['unstaged'])} files")
        if git['untracked']:
            lines.append(f"Untracked files: {len(git['untracked'])}")
    
    # File types
    file_types = context['file_types']
    if file_types:
        lines.append("File types in directory:")
        for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            lines.append(f"  {ext}: {count}")
    
    # Recent commands
    recent = context['recent_commands']
    if recent:
        lines.append("Recent commands:")
        for cmd in recent[-3:]:
            lines.append(f"  {cmd}")
    
    return "\n".join(lines)