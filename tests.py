from functions.python_execution import run_python_file
from typing import List, Tuple, Callable


def create_test_case(description: str, working_dir: str, file_path: str) -> Callable[[], Tuple[str, str]]:
    """Create a test case function."""
    def test_case() -> Tuple[str, str]:
        result = run_python_file(working_dir, file_path)
        return description, result
    return test_case


def run_test_cases(test_cases: List[Callable[[], Tuple[str, str]]]) -> None:
    """Run all test cases and print results."""
    for test_case in test_cases:
        description, result = test_case()
        print(f"Test: {description}")
        print(f"Result: {result}")
        print("-" * 50)


def create_all_tests() -> List[Callable[[], Tuple[str, str]]]:
    """Create all test cases."""
    return [
        create_test_case(
            "Running main.py from calculator dir",
            "calculator", 
            "main.py"
        ),
        create_test_case(
            "Running test.py from calculator dir",
            "calculator", 
            "tests.py"
        ),
        create_test_case(
            "Running '../main.py' from calculator dir (should fail)",
            "calculator", 
            "../main.py"
        ),
        create_test_case(
            "Running nonexistent.py from calculator dir (should fail)",
            "calculator", 
            "nonexistent.py"
        ),
    ]


def main() -> None:
    """Main test runner."""
    test_cases = create_all_tests()
    run_test_cases(test_cases)


if __name__ == "__main__":
    main()