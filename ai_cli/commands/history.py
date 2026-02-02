"""
Intelligent command history search
"""

import os
from typing import List, Tuple, Optional
from datetime import datetime

def search_history(query: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Search shell command history intelligently
    
    Args:
        query: Optional search query
    
    Returns:
        List of (command, timestamp) tuples
    """
    history = load_history()
    
    if query:
        # Filter by query
        query_lower = query.lower()
        history = [(cmd, ts) for cmd, ts in history if query_lower in cmd.lower()]
    
    return history[:20]  # Return top 20 results

def load_history() -> List[Tuple[str, str]]:
    """Load command history from shell history files"""
    history = []
    
    # Try different shell history files
    history_files = [
        (os.path.expanduser("~/.bash_history"), parse_bash_history),
        (os.path.expanduser("~/.zsh_history"), parse_zsh_history),
        (os.path.expanduser("~/.history"), parse_generic_history),
    ]
    
    for hist_file, parser in history_files:
        if os.path.exists(hist_file):
            try:
                with open(hist_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    parsed = parser(lines[-100:])  # Last 100 lines
                    history.extend(parsed)
            except:
                continue
    
    # Sort by timestamp (newest first)
    history.sort(key=lambda x: x[1], reverse=True)
    
    return history

def parse_bash_history(lines: List[str]) -> List[Tuple[str, str]]:
    """Parse bash history format"""
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    for line in lines:
        line = line.strip()
        if line:
            results.append((line, timestamp))
    
    return results

def parse_zsh_history(lines: List[str]) -> List[Tuple[str, str]]:
    """Parse zsh history format"""
    results = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # ZSH history format: ': 1234567890:0;command'
        if line.startswith(': '):
            parts = line.split(';', 1)
            if len(parts) == 2:
                timestamp_part = parts[0][2:]  # Remove ': '
                timestamp_parts = timestamp_part.split(':', 1)
                if timestamp_parts:
                    try:
                        timestamp = datetime.fromtimestamp(int(timestamp_parts[0]))
                        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M")
                        command = parts[1].strip()
                        results.append((command, timestamp_str))
                    except:
                        # Fallback to current time
                        results.append((parts[1].strip(), datetime.now().strftime("%Y-%m-%d %H:%M")))
        else:
            # Plain command
            results.append((line, datetime.now().strftime("%Y-%m-%d %H:%M")))
    
    return results

def parse_generic_history(lines: List[str]) -> List[Tuple[str, str]]:
    """Parse generic history format"""
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    for line in lines:
        line = line.strip()
        if line:
            results.append((line, timestamp))
    
    return results

def save_command_to_history(command: str):
    """Save a command to AI-CLI's own history"""
    history_file = os.path.expanduser("~/.config/ai-cli/history.json")
    
    try:
        import json
        from pathlib import Path
        
        # Ensure directory exists
        Path(history_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        # Add new command
        entry = {
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'directory': os.getcwd(),
        }
        
        history.append(entry)
        
        # Keep only last 1000 commands
        history = history[-1000:]
        
        # Save back
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception:
        pass  # Silently fail if we can't save history