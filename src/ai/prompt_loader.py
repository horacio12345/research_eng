"""
Prompt loading and management utilities.
"""

from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate


def load_prompt(name: str) -> ChatPromptTemplate:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        name: Name of the prompt file (without .txt extension)
        
    Returns:
        ChatPromptTemplate ready for use with format_messages()
    """
    prompt_path = Path(__file__).parent / "prompts" / f"{name}.txt"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    template = prompt_path.read_text(encoding='utf-8')
    return ChatPromptTemplate.from_template(template)
