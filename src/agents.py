from dataclasses import dataclass
from src.runner import RunResult, run_tests
from src.llm_client import generate_test_code

@dataclass
class AgentConfig:
    max_retries: int

@dataclass
class AgentResult:
    passed: bool
    output: str

class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config

    def run(self, source_file: str) -> AgentResult:
        error_output = None

        for _ in range(self.config.max_retries):
            test_code = generate_test_code(source_file, error_output)
            
            # write generated code to a temp file
            test_file = "tests/generated_test.py"
            with open(test_file, "w") as f:
                f.write(test_code)

            run_result = run_tests(test_file)

            if run_result.passed:
                return AgentResult(passed=True, output=run_result.output)
            
            error_output = run_result.output  # pass this to next LLM call

        return AgentResult(passed=False, output="Max retries reached")
