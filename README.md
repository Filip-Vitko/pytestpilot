# pytestpilot

An AI-powered agent that automatically generates pytest tests for Python source code and iteratively fixes bugs in that code until all tests pass: using a local LLM via [Ollama](https://ollama.com/).

## How it works

1. **Generate**: the agent reads your Python source file and asks the LLM to write comprehensive pytest tests for it.
2. **Run**: the generated tests are executed with `pytest`.
3. **Fix**: if any tests fail, the agent sends the source code, the tests, and the error output back to the LLM and asks it to apply the smallest possible fix.
4. **Repeat**: steps 2–3 repeat up to `--max-retries` times.
5. **Save**: once all tests pass, the fixed source file is written to the `output/` directory. The original file in `tests/fixtures/` (or wherever you point it) is never modified.

```
source.py  ──►  LLM generates tests  ──►  pytest
                                              │
                                    ┌─── fail ┘
                                    │
                                    ▼
                             LLM fixes source
                                    │
                                    └─── retry ──► pass ──► output/source.py
```

## Project structure

```
pytestpilot/
├── src/
│   ├── main.py          # CLI entry point
│   ├── agents.py        # Agent loop (generate → run → fix)
│   ├── llm_client.py    # Ollama API calls + markdown fence stripping
│   ├── runner.py        # pytest subprocess runner
│   ├── prompts.py       # System and user prompt templates
│   └── config.py        # Configuration via environment variables
├── tests/
│   ├── fixtures/        # Example Python files with intentional bugs
│   ├── test_runner.py
│   ├── test_agents.py
│   └── test_llm_client.py
├── tmp/                  # Combined source+test scratch files (auto-created, gitignored)
├── output/               # Fixed source files (auto-created, gitignored)
└── requirements.txt
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) running locally (default: `http://localhost:11434`)
- A pulled model: default is `qwen2.5-coder:14b`

```bash
ollama pull qwen2.5-coder:14b
```

## Installation

```bash
git clone https://github.com/your-username/pytestpilot.git
cd pytestpilot

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
python -m src.main <source_file> [--max-retries N]
```

### Examples

Run against one of the included buggy fixtures:

```bash
python -m src.main tests/fixtures/find_max.py
python -m src.main tests/fixtures/add_item.py --max-retries 5
```

On success the fixed file is written to `output/` and the exit code is `0`.
On failure (max retries exhausted) the pytest output is printed and the exit code is `1`.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `MODEL_NAME` | `qwen2.5-coder:14b` | Ollama model to use |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `WORKDIR` | `tmp` | Directory for temporary combined source+test files |

```bash
MODEL_NAME=codellama:13b python -m src.main tests/fixtures/safe_divide.py
```

> `MODEL_PROVIDER` and `API_KEY` also exist in `config.py` for future support of cloud providers (e.g. Anthropic, OpenAI) but are not yet wired up: Ollama is currently the only working provider.

## Running the test suite

```bash
pytest tests/
```

The test suite mocks both the LLM calls and pytest subprocess calls, so it runs in milliseconds with no network access and no real Ollama instance required.

## Known limitations

- **Test quality depends heavily on the local model's reasoning ability.** Smaller models (tested with `qwen2.5-coder:14b`) sometimes generate tests that are internally inconsistent, or assume behavior not implied by the source code: for example, assuming punctuation or whitespace should be stripped in a palindrome check when the original function never says so.
- **The agent both writes the tests and fixes the code to pass them.** This means a sufficiently determined (or confused) model could in principle make tests pass without the underlying logic being meaningfully correct: similar to a student grading their own exam. The fix prompt asks for the smallest possible change to mitigate this, but it isn't a hard guarantee.
- **No support for source files with external dependencies.** Generated tests are combined with the source code into a single scratch file in `tmp/`, so imports are not resolved against the original module's real path or package structure. Works well for standalone functions; not yet suitable for testing code that imports from elsewhere in a larger codebase.
- **No retry budget on LLM failures.** If Ollama is unreachable, `generate_test_code`/`fix_source_code` return an empty string rather than raising, which the agent currently treats as just another failed attempt rather than a distinct "LLM unavailable" error.

## Roadmap

- [ ] Docker + `docker-compose` setup (agent + Ollama as services)
- [ ] CI pipeline (GitHub Actions: lint + test on push)
- [ ] Support for cloud LLM providers (Anthropic, OpenAI) via `MODEL_PROVIDER`
- [ ] Proper import resolution for source files with external dependencies
