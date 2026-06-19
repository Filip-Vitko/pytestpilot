import argparse
import sys
from src.agents import Agent, AgentConfig


def main():
    parser = argparse.ArgumentParser(
        description="Generate pytest tests and auto-fix source code until they pass."
    )
    parser.add_argument("source_file", help="Path to the Python file to test")
    parser.add_argument(
        "--max-retries", type=int, default=3, help="Max fix attempts (default: 3)"
    )
    args = parser.parse_args()

    config = AgentConfig(max_retries=args.max_retries)
    agent = Agent(config)

    print(f"Running agent on {args.source_file}...")
    result = agent.run(args.source_file)

    if result.passed:
        print("[SUCCESS] Tests passed!")
        print(f"\n--- Generated tests ---\n{result.test_code}")
        print(f"\n--- Fixed source ---\n{result.fixed_source_code}")

        with open(args.source_file, "w") as f:
            f.write(result.fixed_source_code)

        sys.exit(0)
    else:
        print("[ERROR] Agent gave up after max retries.")
        print(result.output)
        sys.exit(1)


if __name__ == "__main__":
    main()