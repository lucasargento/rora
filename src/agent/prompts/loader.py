import os
from typing import Dict, Any

def _prompts_dir() -> str:
    """Returns the directory where prompt files are stored."""
    return os.path.dirname(__file__)

def load_prompt(filename: str) -> str:
    """Load a prompt template from a .txt file in the prompts directory."""
    path = os.path.join(_prompts_dir(), filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_prompt(template: str, context: Dict[str, Any]) -> str:
    """Render a prompt template by replacing placeholders like [[key]] with values from context."""
    text = template
    for k, v in context.items():
        text = text.replace(f"[[{k}]]", "" if v is None else str(v))
    return text

