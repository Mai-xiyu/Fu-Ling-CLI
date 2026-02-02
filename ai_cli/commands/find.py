"""
Find files using natural language
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import fnmatch

from ai_cli.core.ai import generate_command
from ai_cli.core.context import get_context

def parse_natural_language_query(query: str) -> Dict[str, Any]:
    """Parse natural language query into search parameters"""
    params = {
        "name_patterns": [],
        "content_patterns": [],
        "size_constraints": [],
        "time_constraints": [],
        "type_constraints": [],
        "location_constraints": [],
    }
    
    # Simple keyword matching (in a real implementation, use AI)
    query_lower = query.lower()
    
    # File types
    if "python" in query_lower or ".py" in query:
        params["type_constraints"].append(("extension", ".py"))
    if "javascript" in query_lower or ".js" in query:
        params["type_constraints"].append(("extension", ".js"))
    if "json" in query_lower or ".json" in query:
        params["type_constraints"].append(("extension", ".json"))
    if "markdown" in query_lower or ".md" in query:
        params["type_constraints"].append(("extension", ".md"))
    if "text" in query_lower or ".txt" in query:
        params["type_constraints"].append(("extension", ".txt"))
    
    # Time constraints
    if "today" in query_lower:
        params["time_constraints"].append(("modified", "today"))
    if "yesterday" in query_lower:
        params["time_constraints"].append(("modified", "yesterday"))
    if "week" in query_lower:
        params["time_constraints"].append(("modified", "week"))
    if "month" in query_lower:
        params["time_constraints"].append(("modified", "month"))
    
    # Size constraints
    if "large" in query_lower or "big" in query_lower:
        params["size_constraints"].append(("min", "10MB"))
    if "small" in query_lower or "tiny" in query_lower:
        params["size_constraints"].append(("max", "1MB"))
    
    # Location
    if "download" in query_lower:
        params["location_constraints"].append(("path_contains", "download"))
    if "home" in query_lower:
        params["location_constraints"].append(("in_home", True))
    
    return params

def find_files_ai(query: str) -> List[str]:
    """Use AI to generate and execute find command"""
    context = get_context()
    
    prompt = f"""
    I want to find files. My query is: "{query}"
    
    Current context:
    - Directory: {context['directory']}
    - Contains: {', '.join(context['contents'][:10])}{'...' if len(context['contents']) > 10 else ''}
    
    Please generate a find command that:
    1. Searches from current directory or appropriate location
    2. Uses appropriate filters based on the query
    3. Is safe to execute
    4. Returns only the find command, no explanation
    
    The command should use standard Unix find syntax.
    """
    
    try:
        command = generate_command(prompt)
        
        # Basic safety check
        if not command.startswith("find "):
            raise ValueError("Generated command doesn't start with 'find'")
        
        # Execute the command
        import subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=context['directory']
        )
        
        if result.returncode == 0:
            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            return files
        else:
            print(f"Command failed: {result.stderr}")
            return []
            
    except Exception as e:
        print(f"Error using AI find: {e}")
        return find_files_simple(query)

def find_files_simple(query: str) -> List[str]:
    """Simple fallback find implementation"""
    files = []
    query_lower = query.lower()
    
    # Walk through current directory
    for root, dirs, filenames in os.walk('.'):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            
            # Simple matching
            if (query_lower in filename.lower() or 
                query_lower in filepath.lower()):
                files.append(filepath)
    
    return files[:50]  # Limit results

def find_files(query: str, use_ai: bool = True) -> List[str]:
    """
    Find files matching natural language query
    
    Args:
        query: Natural language description of files to find
        use_ai: Whether to use AI for query interpretation
    
    Returns:
        List of file paths matching the query
    """
    if not query:
        return []
    
    if use_ai:
        return find_files_ai(query)
    else:
        return find_files_simple(query)

def format_find_results(files: List[str], query: str = "") -> str:
    """Format find results for display"""
    if not files:
        return f"No files found matching '{query}'"
    
    result = f"Found {len(files)} files"
    if query:
        result += f" matching '{query}'"
    result += ":\n\n"
    
    for i, filepath in enumerate(files[:20], 1):  # Show first 20
        # Get file info
        try:
            stat = os.stat(filepath)
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            size_str = f"{size:,} bytes"
            if size > 1024*1024:
                size_str = f"{size/(1024*1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size/1024:.1f} KB"
            
            time_str = mtime.strftime("%Y-%m-%d %H:%M")
            result += f"{i:3d}. {filepath}\n"
            result += f"     Size: {size_str}, Modified: {time_str}\n"
        except:
            result += f"{i:3d}. {filepath}\n"
    
    if len(files) > 20:
        result += f"\n... and {len(files) - 20} more files\n"
    
    return result