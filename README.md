# CodeLens AI

CodeLens AI is a Python-based code analysis tool that scans a Python project, detects code quality issues, generates pytest test suggestions, creates actual pytest test files, runs the generated tests, and produces a Markdown report.

## Features

- Scans Python files in a project folder
- Extracts imports, functions, classes, arguments, line numbers, and docstrings
- Detects missing docstrings
- Detects possible division-by-zero risks
- Detects functions with too many arguments
- Detects long functions
- Generates pytest test suggestions
- Creates actual pytest test files
- Runs generated tests automatically
- Generates a Markdown report

## Tech Stack

- Python
- AST module
- Pytest
- Subprocess
- Markdown report generation

## Project Structure

```text
codelens-ai/
├── codelens/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── reporter.py
│   ├── scanner.py
│   ├── test_generator.py
│   ├── test_runner.py
│   └── test_writer.py
│
├── sample_projects/
│   └── calculator_app/
│       └── calculator.py
│
├── generated_tests/
├── reports/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md