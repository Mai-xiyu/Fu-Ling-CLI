"""
Learning from user patterns for AI-CLI
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict

def learn_patterns():
    """Analyze user patterns and learn from them"""
    
    # This is a placeholder for actual learning logic
    # In a real implementation, this would:
    # 1. Analyze command history
    # 2. Identify patterns and preferences
    # 3. Update configuration based on learned patterns
    
    learning_file = Path.home() / ".config" / "ai-cli" / "learning.json"
    
    try:
        # Load existing learning data
        if learning_file.exists():
            with open(learning_file, 'r') as f:
                data = json.load(f)
        else:
            data = {
                'patterns': {},
                'preferences': {},
                'last_learned': None,
                'command_counts': defaultdict(int),
            }
        
        # Update learning data
        data['last_learned'] = datetime.now().isoformat()
        
        # Analyze command history if available
        history_file = Path.home() / ".config" / "ai-cli" / "history.json"
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            # Count command frequencies
            for entry in history[-100:]:  # Last 100 commands
                cmd = entry.get('command', '')
                if cmd:
                    # Extract base command (first word)
                    base_cmd = cmd.split()[0] if ' ' in cmd else cmd
                    data['command_counts'][base_cmd] += 1
        
        # Save updated data
        with open(learning_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return True
        
    except Exception as e:
        print(f"Learning failed: {e}")
        return False

def get_learned_patterns() -> Dict[str, Any]:
    """Get learned patterns and preferences"""
    
    learning_file = Path.home() / ".config" / "ai-cli" / "learning.json"
    
    if not learning_file.exists():
        return {}
    
    try:
        with open(learning_file, 'r') as f:
            return json.load(f)
    except:
        return {}

def get_frequent_commands(limit: int = 10) -> List[Dict[str, Any]]:
    """Get most frequently used commands"""
    
    patterns = get_learned_patterns()
    command_counts = patterns.get('command_counts', {})
    
    # Sort by frequency
    sorted_commands = sorted(
        command_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [
        {'command': cmd, 'count': count}
        for cmd, count in sorted_commands[:limit]
    ]

def suggest_based_on_history(current_context: Dict[str, Any]) -> List[str]:
    """Suggest commands based on learned patterns and current context"""
    
    patterns = get_learned_patterns()
    frequent_commands = get_frequent_commands(5)
    
    suggestions = []
    
    # Add frequent commands
    for item in frequent_commands:
        cmd = item['command']
        count = item['count']
        
        # Only suggest if it makes sense in current context
        if is_command_relevant(cmd, current_context):
            suggestions.append(f"{cmd} (used {count} times)")
    
    # Add context-specific suggestions
    if current_context['git']['is_repo']:
        suggestions.extend([
            "git status",
            "git log --oneline -5",
        ])
    
    # Add general suggestions
    suggestions.extend([
        "ls -la",
        "pwd",
        "date",
    ])
    
    return suggestions[:5]  # Return top 5

def is_command_relevant(command: str, context: Dict[str, Any]) -> bool:
    """Check if a command is relevant in current context"""
    
    # Git commands only relevant in git repos
    if command.startswith('git'):
        return context['git']['is_repo']
    
    # Python commands only relevant with Python files
    if command.startswith('python') or 'pip' in command:
        return '.py' in context['file_types']
    
    # Docker commands (placeholder)
    if command.startswith('docker'):
        # Check for docker-compose.yml or Dockerfile
        contents = context['contents']
        has_docker = any(
            'docker' in f.lower() or 'Dockerfile' in f
            for f in contents
        )
        return has_docker
    
    return True  # Most commands are generally relevant