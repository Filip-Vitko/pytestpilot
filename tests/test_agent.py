from src.agents import Agent, AgentConfig
from src.runner import RunResult

# --- Happy Path ---

def test_happy_path(mocker):
    mock_runner = mocker.patch("src.agents.run_tests", return_value=RunResult(
        passed=True,
        output="1 passed",
        exit_code=0,
    ))

    mocker.patch("src.agents.generate_test_code", return_value="def test_foo(): assert True")

    agent = Agent(AgentConfig(max_retries=3))
    result = agent.run("fake_source_code.py")

    assert result.passed is True
    assert mock_runner.call_count == 1

# --- Retry logic ---

def test_retry_logic(mocker):
    mock_runner = mocker.patch("src.agents.run_tests", side_effect=[
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1),
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1),
        RunResult(passed=True, output="1 passed", exit_code=0),
    ])

    mocker.patch("src.agents.generate_test_code", return_value="def test_foo(): assert True")

    agent = Agent(AgentConfig(max_retries=3))
    result = agent.run("fake_source_code.py")

    assert result.passed is True
    assert mock_runner.call_count == 3

# --- Give up logic ---

def test_give_up_logic(mocker):
    mock_runner = mocker.patch("src.agents.run_tests", side_effect=[
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1),
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1),
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1),
        RunResult(passed=False, output="AssertionError: False is not true", exit_code=1), # if off by one error, it will give up
    ])

    mocker.patch("src.agents.generate_test_code", return_value="def test_foo(): assert True")

    agent = Agent(AgentConfig(max_retries=3))
    result = agent.run("fake_source_code.py")

    assert result.passed is False
    assert mock_runner.call_count == 3

# --- Retry uses error output to improve code ---

def test_retry_sends_error_output_to_llm(mocker):
    mocker.patch("src.agents.run_tests", side_effect=[
        RunResult(passed=False, output="AssertionError: 1 != 2", exit_code=1),
        RunResult(passed=True, output="1 passed", exit_code=0),
    ])

    mock_llm = mocker.patch("src.agents.generate_test_code", return_value="def test_foo(): assert True")

    agent = Agent(AgentConfig(max_retries=3))
    result = agent.run("fake_source_code.py")

    second_call_args = mock_llm.call_args_list[1]
    assert "AssertionError: 1 != 2" in str(second_call_args)