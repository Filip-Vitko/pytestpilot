SYSTEM_PROMPT = """You are a code expert. You will be given Python source code.
Write comprehensive pytest tests for it. Make sure each test is independent and does not
rely on the results of other tests.

Base your tests ONLY on what the function name, docstring, and parameter names imply.
Do not assume behavior that isn't stated or strongly implied. For example, do not assume
a function should strip punctuation, trim whitespace, or handle unicode unless the
docstring or function name says so.

Focus on edge cases, boundary conditions, data types, and invalid inputs that are
reasonable given the function's stated purpose.
Assume the code might have bugs and your tests should catch them.
Return only the pytest code, nothing else. No markdown, no explanations, no code fences."""


def build_user_prompt(source_code: str) -> str:
    return f"Source code:\n{source_code}"


def build_fix_prompt(source_code: str, test_code: str, error_output: str) -> str:
    return f"""Source code:\n{source_code}

            Tests:\n{test_code}

            Errors:\n{error_output}

            Fix the source code to make the failing tests pass, using the SMALLEST possible change.
            Do not change function signatures, parameter names, or the function's structure.
            Do not add new functionality, new edge case handling, or new behavior beyond what the
            failing tests specifically require.
            If a test expects a specific value or behavior, change only the logic needed to produce
            that exact result — do not generalize, do not add extra validation, do not refactor.
            Return only the fixed source code, nothing else. No markdown, no explanations, no code fences."""