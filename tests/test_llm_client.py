import requests
from src.llm_client import generate_test_code, fix_source_code, _strip_markdown_fences


# --- generate_test_code: happy path ---

def test_generate_returns_string(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def test_add(): assert add(1,2) == 3"},
        "done": True,
    }
    mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    result = generate_test_code("def add(a, b): return a + b")
    assert isinstance(result, str)


# --- generate_test_code: content check ---

def test_generate_returns_pytest_code(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def test_add(): assert add(1,2) == 3"},
        "done": True,
    }
    mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    result = generate_test_code("def add(a, b): return a + b")
    assert len(result) > 0
    assert "def test_" in result


# --- generate_test_code: calls Ollama correctly ---

def test_generate_calls_ollama_with_right_data(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def test_add(): assert add(1,2) == 3"},
        "done": True,
    }
    mock_post = mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    source_code = "def add(a, b): return a + b"
    generate_test_code(source_code)

    called_json = mock_post.call_args.kwargs["json"]
    assert called_json["model"] is not None
    assert any(source_code in msg["content"] for msg in called_json["messages"])


# --- generate_test_code: connection error ---

def test_generate_handles_ollama_down(mocker):
    mocker.patch(
        "src.llm_client.requests.post",
        side_effect=requests.exceptions.ConnectionError("Connection refused"),
    )

    result = generate_test_code("def add(a, b): return a + b")
    assert result == ""


# --- fix_source_code: happy path ---

def test_fix_returns_string(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def add(a, b):\n    return a + b"},
        "done": True,
    }
    mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    result = fix_source_code(
        source_code="def add(a, b): return a - b",
        test_code="def test_add(): assert add(1,2) == 3",
        error_output="AssertionError: -1 != 3",
    )
    assert isinstance(result, str)


# --- fix_source_code: content check ---

def test_fix_returns_source_not_tests(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def add(a, b):\n    return a + b"},
        "done": True,
    }
    mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    result = fix_source_code(
        source_code="def add(a, b): return a - b",
        test_code="def test_add(): assert add(1,2) == 3",
        error_output="AssertionError: -1 != 3",
    )
    assert len(result) > 0
    assert "def test_" not in result  # should be fixed source, not test code


# --- fix_source_code: calls Ollama correctly ---

def test_fix_calls_ollama_with_right_data(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {
        "model": "qwen2.5-coder",
        "message": {"role": "assistant", "content": "def add(a, b):\n    return a + b"},
        "done": True,
    }
    mock_post = mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    source_code = "def add(a, b): return a - b"
    test_code = "def test_add(): assert add(1,2) == 3"
    error_output = "AssertionError: -1 != 3"

    fix_source_code(source_code, test_code, error_output)

    called_json = mock_post.call_args.kwargs["json"]
    combined_content = " ".join(msg["content"] for msg in called_json["messages"])
    assert source_code in combined_content
    assert test_code in combined_content
    assert error_output in combined_content


# --- fix_source_code: connection error ---

def test_fix_handles_ollama_down(mocker):
    mocker.patch(
        "src.llm_client.requests.post",
        side_effect=requests.exceptions.ConnectionError("Connection refused"),
    )

    result = fix_source_code(
        source_code="def add(a, b): return a - b",
        test_code="def test_add(): assert add(1,2) == 3",
        error_output="AssertionError: -1 != 3",
    )
    assert result == ""


# --- shared: malformed Ollama response ---

def test_handles_malformed_response(mocker):
    fake_response = mocker.Mock()
    fake_response.json.return_value = {"done": True}  # no "message" key
    mocker.patch("src.llm_client.requests.post", return_value=fake_response)

    result = generate_test_code("def add(a, b): return a + b")
    assert result == ""

# --- shared: strip markdown fences ---

def test_strips_markdown_fences():
    raw = "```python\ndef test_foo():\n    assert True\n```"
    assert _strip_markdown_fences(raw) == "def test_foo():\n    assert True"

def test_leaves_clean_code_unchanged():
    raw = "def test_foo():\n    assert True"
    assert _strip_markdown_fences(raw) == raw