# CodeLens AI

![CodeLens AI Analysis](https://github.com/khushichhabra7921/CodeLensAI/actions/workflows/codelens.yml/badge.svg)

CodeLens AI is an AI-powered Python code analysis tool that scans a Python project, detects code quality issues, generates pytest test suggestions, creates actual pytest test files, runs those tests automatically, and produces a Markdown report with an AI-generated codebase explanation.

## Features

* Scans Python files in a project folder
* Extracts imports, functions, classes, arguments, line numbers, and docstrings
* Detects missing docstrings
* Detects possible division-by-zero risks
* Detects functions with too many arguments
* Detects long functions
* Generates pytest test suggestions
* Creates actual pytest test files
* Runs generated tests automatically
* Generates a Markdown report
* Uses Groq LLM to generate an AI explanation of the codebase
* Runs automatically on GitHub Actions for every push and pull request

## Tech Stack

* Python
* AST module
* Pytest
* Groq LLM
* python-dotenv
* GitHub Actions
* Markdown report generation

## Project Structure

```text
codelens-ai/
│
├── .github/
│   └── workflows/
│       └── codelens.yml
│
├── codelens/
│   ├── __init__.py
│   ├── ai_explainer.py
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
│   └── test_calculator_generated.py
│
├── reports/
│   └── codelens_report.md
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## How It Works

```text
User gives a Python project folder
        ↓
CodeLens scans all Python files
        ↓
It extracts functions, classes, imports, arguments, line numbers, and docstrings
        ↓
It detects code quality issues
        ↓
It generates pytest test suggestions
        ↓
It creates actual pytest test files
        ↓
It runs the generated tests
        ↓
It generates an AI explanation of the codebase
        ↓
It creates a Markdown report
```

## Installation

Clone the repository:

```bash
git clone https://github.com/khushichhabra7921/CodeLensAI.git
cd CodeLensAI
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the root folder:

```text
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

The `.env` file is ignored by Git and should not be pushed to GitHub.

For GitHub Actions, add your Groq API key as a repository secret:

```text
GROQ_API_KEY
```

## Usage

Analyze the sample project:

```bash
python main.py analyze sample_projects/calculator_app
```

View CLI help:

```bash
python main.py --help
```

View help for the analyze command:

```bash
python main.py analyze --help
```

Run generated tests manually:

```bash
python -m pytest generated_tests -v
```

## Example Output

```text
CodeLens AI Report
========================================
Files scanned: 1
Imports found: 1
Functions found: 5
Classes found: 1
Issues found: 7
Test suggestions generated: 5
Pytest files generated: 1
Generated tests passed: True
AI explanation generated: True
```

## Sample Issues Detected

```text
[Possible Runtime Error]
Severity: High
Message: Function 'divide' uses division. This may crash if the denominator is zero.
Suggestion: Add a check before division, for example: if b == 0, raise ValueError.
```

```text
[Too Many Arguments]
Severity: Medium
Message: Function 'calculate_final_score' has 5 arguments.
Suggestion: Consider grouping related values into a dictionary, class, or data object.
```

```text
[Long Function]
Severity: Medium
Message: Function 'calculate_final_score' is 15 lines long.
Suggestion: Consider splitting this function into smaller helper functions.
```

## Report

After running CodeLens AI, a Markdown report is generated at:

```text
reports/codelens_report.md
```

The report includes:

* Project summary
* Detailed file analysis
* AI codebase explanation
* Code quality issues
* Test suggestions
* Generated pytest files
* Pytest run result

## GitHub Actions

This project includes a GitHub Actions workflow:

```text
.github/workflows/codelens.yml
```

The workflow automatically runs on:

* Push to `main`
* Pull request to `main`
* Manual workflow trigger

It performs the following steps:

```text
Checkout repository
        ↓
Set up Python
        ↓
Install dependencies
        ↓
Run CodeLens AI
        ↓
Run generated pytest tests
        ↓
Upload Markdown report as artifact
```

## Current Status

Completed:

* Static Python code scanner
* Rule-based code quality analyzer
* Markdown report generator
* Test suggestion generator
* Pytest file generator
* Automatic pytest runner
* AI-powered codebase explanation using Groq
* CLI command support
* GitHub Actions workflow

## Future Improvements

Planned improvements:

* Support for analyzing larger real-world repositories
* Better AI-generated test cases
* Pull request comment generation
* Code complexity scoring
* Security issue detection
* Support for multiple programming languages
* Web dashboard for reports
