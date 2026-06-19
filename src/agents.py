import os
from dataclasses import dataclass
from src.config import WORKDIR
from src.runner import RunResult, run_tests
from src.llm_client import generate_test_code, fix_source_code


@dataclass
class AgentConfig:
    max_retries: int


@dataclass
class AgentResult:
    passed: bool
    output: str
    fixed_source_code: str | None = None
    test_code: str | None = None


class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        os.makedirs(WORKDIR, exist_ok=True)

    def run(self, source_file: str) -> AgentResult:
        with open(source_file) as f:
            source_code = f.read()

        test_code = generate_test_code(source_code)
        test_file = os.path.join(WORKDIR, "generated_test.py")

        for _ in range(self.config.max_retries):
            combined = source_code + "\n\n" + test_code
            with open(test_file, "w") as f:
                f.write(combined)

            run_result = run_tests(test_file)

            if run_result.passed:
                return AgentResult(
                    passed=True,
                    output=run_result.output,
                    fixed_source_code=source_code,
                    test_code=test_code,
                )

            source_code = fix_source_code(source_code, test_code, run_result.output)

        return AgentResult(passed=False, output="Max retries reached")