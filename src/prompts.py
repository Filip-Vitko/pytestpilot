#TODO: builds actual text that gets sent to Ollama 
#TODO: usage in llm_client.py
#TODO: first call source code, second for retry that includes error output

def build_user_prompt(source_code: str) -> str:
    return f"""
    You are a code expert. You will be given a python source code. Write comprehensive pytest tests for the source code. Focus on finding edge cases,
    boundary conditions, corner cases and invalid inputs. Assume the source code might have bugs and your tests catch them. Return only the pytest code, nothing else.
    Source code:
    {source_code}
    """

def build_fix_prompt(source_code: str, test_code: str, error_output: str) -> str:
    return f"""
    Here is Python source code: {source_code} and pytest tests: {test_code}. The tests are filing with these errors: {error_output}
    Fix the source code to make the tests pass. Do not change the function signatures or structure. Return only the fixed source code, nothing else.
    """