"""
Search file contents using natural language
"""

import os
import re
from typing import Dict, List, Optional
from ai_cli.core.ai import generate_command

def search_contents(query: str) -> Dict[str, List[str]]:
    """
    Search file contents using natural language query
    
    Args:
        query: Natural language search query
    
    Returns:
        Dictionary mapping file paths to list of matching lines
    """
    # Simple implementation for now
    # In a real implementation, this would use AI to generate grep commands
    
    results = {}
    
    # Simple keyword search
    keywords = extract_keywords(query)
    
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if filename.startswith('.'):
                continue
                
            filepath = os.path.join(root, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    matches = []
                    for i, line in enumerate(lines, 1):
                        if any(keyword.lower() in line.lower() for keyword in keywords):
                            matches.append(f"Line {i}: {line.strip()}")
                    
                    if matches:
                        results[filepath] = matches[:10]  # Limit to 10 matches per file
                        
            except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                continue
    
    return results

def extract_keywords(query: str) -> List[str]:
    """Extract search keywords from natural language query"""
    # Remove common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    words = re.findall(r'\b\w+\b', query.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # If no keywords found, use the whole query (excluding very short words)
    if not keywords:
        keywords = [word for word in words if len(word) > 2]
    
    return keywords[:5]  # Limit to 5 keywords

def format_grep_results(results: Dict[str, List[str]], query: str = "") -> str:
    """Format grep results for display"""
    if not results:
        return f"No matches found for '{query}'"
    
    output = f"Found matches in {len(results)} files"
    if query:
        output += f" for '{query}'"
    output += ":\n\n"
    
    for filepath, matches in results.items():
        output += f"[bold]{filepath}[/]:\n"
        for match in matches:
            output += f"  • {match}\n"
        output += "\n"
    
    return output