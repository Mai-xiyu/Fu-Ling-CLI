"""
AI model integration for AI-CLI
"""

import json
import subprocess
from typing import Dict, Any, Optional, List
from ai_cli.core.config import get_model_config

class AIModel:
    """Base class for AI models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", "phi3:mini")
        self.temperature = config.get("temperature", 0.3)
        self.provider = config.get("provider", "ollama")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response from model"""
        raise NotImplementedError
    
    def generate_command(self, prompt: str) -> str:
        """Generate a shell command from prompt"""
        system_prompt = """You are a helpful assistant that generates shell commands.
        Always respond with ONLY the command, no explanations, no markdown, no code blocks.
        The command should be safe to execute and follow best practices.
        If you cannot generate a safe command, respond with "ERROR: Cannot generate command"."""
        
        response = self.generate(prompt, system_prompt)
        
        # Clean up response
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith("```") and response.endswith("```"):
            lines = response.split('\n')
            if len(lines) >= 3:
                response = '\n'.join(lines[1:-1]).strip()
        
        return response

class OllamaModel(AIModel):
    """Ollama model integration"""
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Ollama"""
        try:
            import ollama
        except ImportError:
            return "ERROR: Ollama not installed. Run 'pip install ollama'"
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = ollama.chat(
                model=self.name,
                messages=messages,
                options={
                    "temperature": self.temperature,
                }
            )
            return response['message']['content']
        except Exception as e:
            return f"ERROR: {str(e)}"

class OpenAIModel(AIModel):
    """OpenAI-compatible model integration (OpenAI, Moonshot, etc.)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using OpenAI-compatible API"""
        try:
            from openai import OpenAI
        except ImportError:
            return "ERROR: OpenAI not installed. Run 'pip install openai'"
        
        if not self.api_key:
            return "ERROR: API key not configured"
        
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = client.chat.completions.create(
                model=self.name,
                messages=messages,
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"ERROR: {str(e)}"

class LocalModel(AIModel):
    """Local model integration (fallback)"""
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Simple local fallback - no actual AI"""
        # This is a placeholder for actual local model integration
        # In a real implementation, you would integrate with local LLM libraries
        
        # For now, return a simple response
        return f"I would generate a response for: {prompt[:50]}..."
    
    def generate_command(self, prompt: str) -> str:
        """Simple command generation fallback"""
        # Basic pattern matching for common queries
        prompt_lower = prompt.lower()
        
        if "find" in prompt_lower and "file" in prompt_lower:
            if "python" in prompt_lower:
                return "find . -name '*.py' -type f"
            elif "today" in prompt_lower:
                return "find . -type f -mtime 0"
            else:
                return "find . -type f"
        
        elif "disk" in prompt_lower and "usage" in prompt_lower:
            return "df -h"
        
        elif "memory" in prompt_lower:
            return "free -h"
        
        elif "process" in prompt_lower:
            return "ps aux | head -20"
        
        else:
            return "echo 'Command not implemented in fallback mode'"

def get_model() -> AIModel:
    """Get configured AI model instance"""
    config = get_model_config()
    provider = config.get("provider", "ollama")
    
    try:
        if provider == "ollama":
            return OllamaModel(config)
        elif provider in ["openai", "moonshot"]:
            return OpenAIModel(config)
        else:
            return LocalModel(config)
    except Exception:
        # Fallback to local model if configured model fails
        return LocalModel(config)

def generate_command(prompt: str) -> str:
    """Generate a shell command using AI"""
    model = get_model()
    return model.generate_command(prompt)

def generate_explanation(command: str) -> str:
    """Generate explanation for a command"""
    model = get_model()
    
    prompt = f"""Explain what this shell command does: {command}
    
    Provide a clear, concise explanation that includes:
    1. What the command does
    2. Key options/flags and their meanings
    3. Example output
    4. Common use cases
    5. Safety considerations if any
    
    Format the response in markdown."""
    
    return model.generate(prompt)

def generate_suggestions(context: Dict[str, Any], query: Optional[str] = None) -> List[Dict[str, str]]:
    """Generate command suggestions based on context"""
    model = get_model()
    
    if query:
        prompt = f"""Based on this query: "{query}"
        
        And the current context:
        {json.dumps(context, indent=2)}
        
        Suggest 3-5 useful shell commands that might help.
        For each command, provide:
        1. The command itself
        2. A brief description of what it does
        
        Format as JSON list: [{{"command": "...", "description": "..."}}]"""
    else:
        prompt = f"""Based on the current context:
        {json.dumps(context, indent=2)}
        
        Suggest 3-5 useful shell commands that the user might want to run.
        For each command, provide:
        1. The command itself
        2. A brief description of what it does
        
        Format as JSON list: [{{"command": "...", "description": "..."}}]"""
    
    response = model.generate(prompt)
    
    try:
        # Try to parse JSON response
        suggestions = json.loads(response)
        if isinstance(suggestions, list):
            return suggestions
    except:
        pass
    
    # Fallback suggestions
    return [
        {"command": "ls -la", "description": "List all files with details"},
        {"command": "pwd", "description": "Show current directory"},
        {"command": "git status", "description": "Check git repository status"},
    ]

def test_model_connection() -> bool:
    """Test if AI model is accessible"""
    model = get_model()
    
    if isinstance(model, LocalModel):
        return True  # Local model always "works"
    
    try:
        test_prompt = "Say 'hello' if you can hear me."
        response = model.generate(test_prompt)
        return "hello" in response.lower() or len(response.strip()) > 0
    except:
        return False