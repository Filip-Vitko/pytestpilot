import re
import requests
from src.config import OLLAMA_URL, MODEL_NAME
from src.prompts import SYSTEM_PROMPT, build_user_prompt, build_fix_prompt

def _strip_markdown_fences(text: str) -> str:
    """Remove ```python ... ``` or ``` ... ``` wrapping if present."""
    text = text.strip()
    pattern = r"```(?:python)?\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def _call_ollama(system_prompt: str, user_prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
            },
        )
        content = response.json().get("message", {}).get("content", "")
        return _strip_markdown_fences(content)
    except requests.exceptions.ConnectionError:
        return ""

def generate_test_code(source_code: str) -> str:
    user_prompt = build_user_prompt(source_code)
    return _call_ollama(SYSTEM_PROMPT, user_prompt)


def fix_source_code(source_code: str, test_code: str, error_output: str) -> str:
    user_prompt = build_fix_prompt(source_code, test_code, error_output)
    return _call_ollama(SYSTEM_PROMPT, user_prompt)