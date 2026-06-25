import subprocess
import sys


def run_pytest(test_dir="generated_tests"):
    """
    Runs pytest on the generated test files.
    """

    command = [
        sys.executable,
        "-m",
        "pytest",
        test_dir,
        "-v"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return {
        "command": " ".join(command),
        "passed": result.returncode == 0,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }