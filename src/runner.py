import os
import subprocess
from dataclasses import dataclass

@dataclass
class RunResult:
    """
    0 - all tests passed
    1 - tests ran but some failed
    2 - pytest was interrupted
    3 - internal pytest error
    4 - command line usage error
    5 - no tests were collected (empty file)
    """
    passed: bool
    output: str
    exit_code: int

    @classmethod
    def from_process(cls, exit_code: int, output: str) -> "RunResult":
        return cls(
            passed=exit_code == 0,
            output=output,
            exit_code=exit_code
        )

def run_tests(file_path: str) -> RunResult:
    if not os.path.exists(file_path):
        return RunResult.from_process(1, "File not found")
    try:
        result = subprocess.run(
            ["pytest", file_path],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = result.stdout + result.stderr
        return RunResult.from_process(result.returncode, output)
    except subprocess.TimeoutExpired:
        return RunResult.from_process(1, "pytest timed out after 5 seconds")