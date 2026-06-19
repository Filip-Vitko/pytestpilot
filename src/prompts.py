SYSTEM_PROMPT = """You are a code expert. You will be given Python source code. 
Write comprehensive pytest tests for it. Focus on edge cases, boundary conditions, 
and invalid inputs. Assume the code might have bugs — your tests should catch them. 
Return only the pytest code, nothing else."""

def build_user_prompt(source_code: str) -> str:
    return f"Source code:\n{source_code}"

def build_fix_prompt(source_code: str, test_code: str, error_output: str) -> str:
    return f"""Source code:\n{source_code}\n\nTests:\n{test_code}\n\nErrors:\n{error_output}
Fix the source code to make the tests pass. Do not change function signatures or structure. 
Return only the fixed source code, nothing else."""