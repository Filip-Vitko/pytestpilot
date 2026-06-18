from gettext import install
from unittest import result
import pytest
from src.runner import run_tests, RunResult

# --- Group 1: result object shape ---

def test_result_is_runresult(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_pass(): assert True")
    result = run_tests(str(f))
    assert isinstance(result, RunResult)

def test_result_has_passed_field_bool(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_pass(): assert True")
    result = run_tests(str(f))
    assert isinstance(result.passed, bool)

def test_result_has_output_field(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_pass(): assert True")
    result = run_tests(str(f))
    assert isinstance(result.output, str)

# --- Group 2: passing tests ---

def test_passing_file_returns_true(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_pass(): assert True")
    assert run_tests(str(f)).passed is True

def test_output_contains_passed(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_pass(): assert True")
    result = run_tests(str(f))
    assert "passed" in result.output

# --- Group 3: failing tests ---

def test_failing_file_returns_false(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_fail(): assert False")
    assert run_tests(str(f)).passed is False

def test_output_contains_failure_info(tmp_path):
    f = tmp_path / "test_sample.py"
    f.write_text("def test_fail(): assert False")
    result = run_tests(str(f))
    assert "AssertionError" in result.output or "failed" in result.output

# --- Group 4: edge cases