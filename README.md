# CodeLens AI

![CodeLens AI Analysis](https://github.com/khushichhabra7921/CodeLensAI/actions/workflows/codelens.yml/badge.svg)

CodeLens AI is an AI-powered Python code analysis tool that scans a Python project, detects code quality issues, detects common security risks, generates pytest test suggestions, creates actual pytest test files, runs those tests automatically, calculates a code quality and security score, and produces a Markdown report with an AI-generated explanation of the codebase.

---

## Features

- Scans Python files in a project folder
- Extracts imports, functions, classes, arguments, line numbers, and docstrings
- Detects missing docstrings
- Detects possible division-by-zero risks
- Detects functions with too many arguments
- Detects long functions
- Detects common security issues
- Detects hardcoded secrets
- Detects unsafe `eval()` usage
- Detects unsafe `exec()` usage
- Detects unsafe `os.system()` usage
- Detects `subprocess` usage with `shell=True`
- Detects unsafe `pickle.load()` and `pickle.loads()` usage
- Detects unsafe `yaml.load()` usage without SafeLoader
- Detects insecure HTTP URLs
- Calculates a code quality and security score
- Generates pytest test suggestions
- Creates actual pytest test files
- Runs generated pytest tests automatically
- Generates a Markdown report
- Uses Groq LLM to generate an AI explanation of the codebase
- Runs automatically on GitHub Actions for every push and pull request

---

## Tech Stack

- Python
- AST module
- Pytest
- Groq LLM
- python-dotenv
- GitHub Actions
- Markdown report generation

---

## Project Structure

```text
CodeLensAI/
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
│   ├── score_calculator.py
│   ├── security_analyzer.py
│   ├── test_generator.py
│   ├── test_runner.py
│   └── test_writer.py
│
├── sample_projects/
│   ├── calculator_app/
│   │   └── calculator.py
│   │
│   └── vulnerable_app/
│       └── vulnerable.py
│
├── generated_tests/
│   └── test_calculator_generated.py
│
├── reports/
│   └── codelens_report.md
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## How It Works

```text
User gives a Python project folder
        ↓
CodeLens scans all Python files
        ↓
It extracts imports, functions, classes, arguments, line numbers, and docstrings
        ↓
It detects code quality issues
        ↓
It detects security issues
        ↓
It calculates a code quality and security score
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

---

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

---

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

---

## Usage

Analyze the calculator sample project:

```bash
python main.py analyze sample_projects/calculator_app
```

Analyze the vulnerable sample project:

```bash
python main.py analyze sample_projects/vulnerable_app
```

You can also run the tool without the `analyze` keyword:

```bash
python main.py sample_projects/calculator_app
```

Run generated tests manually:

```bash
python -m pytest generated_tests -v
```

---

## Example Terminal Output

```text
CodeLens AI Report
========================================
Files scanned: 1
Imports found: 4
Functions found: 7
Classes found: 0
Total issues found: 17
Code quality issues found: 7
Security issues found: 10
Test suggestions generated: 7
Pytest files generated: 1
Generated tests passed: True
AI explanation generated: True

Code Quality and Security Score
----------------------------------------
Score: 0/100
Grade: F
Status: Critical
Critical severity issues: 2
High severity issues: 7
Medium severity issues: 0
Low severity issues: 8
```

---

## Code Quality Issues Detected

### Missing Docstring

```text
[Missing Docstring]
Severity: Low
Message: Function does not have a docstring.
Suggestion: Add a short docstring explaining what the function does.
```

### Possible Runtime Error

```text
[Possible Runtime Error]
Severity: High
Message: Function uses division. This may crash if the denominator is zero.
Suggestion: Add a check before division, for example: if b == 0, raise ValueError.
```

### Too Many Arguments

```text
[Too Many Arguments]
Severity: Medium
Message: Function has too many arguments.
Suggestion: Consider grouping related values into a dictionary, class, or data object.
```

### Long Function

```text
[Long Function]
Severity: Medium
Message: Function is too long.
Suggestion: Consider splitting this function into smaller helper functions.
```

---

## Security Issues Detected

### Unsafe eval Usage

```text
[Unsafe eval Usage]
Severity: Critical
Message: The code uses eval(), which can execute arbitrary Python code.
Suggestion: Avoid eval(). Use safer parsing methods such as ast.literal_eval() when possible.
```

### Unsafe exec Usage

```text
[Unsafe exec Usage]
Severity: Critical
Message: The code uses exec(), which can execute arbitrary Python code.
Suggestion: Avoid exec(). Refactor the logic so dynamic code execution is not required.
```

### Unsafe os.system Usage

```text
[Unsafe os.system Usage]
Severity: High
Message: The code uses os.system(), which may allow command injection if user input is included.
Suggestion: Use subprocess.run() with a list of arguments and avoid shell=True.
```

### Subprocess shell=True

```text
[Subprocess shell=True]
Severity: High
Message: The code uses subprocess with shell=True, which can be dangerous with user input.
Suggestion: Use shell=False and pass commands as a list of arguments.
```

### Unsafe Pickle Usage

```text
[Unsafe Pickle Usage]
Severity: High
Message: The code uses pickle to load data. Pickle can execute code when loading untrusted data.
Suggestion: Avoid loading pickle data from untrusted sources. Use JSON for safer data exchange.
```

### Unsafe YAML Load

```text
[Unsafe YAML Load]
Severity: High
Message: The code uses yaml.load() without SafeLoader.
Suggestion: Use yaml.safe_load() or yaml.load(..., Loader=yaml.SafeLoader).
```

### Hardcoded Secret

```text
[Hardcoded Secret]
Severity: High
Message: A variable appears to contain a hardcoded secret.
Suggestion: Move secrets to environment variables or a secure secrets manager.
```

### Insecure HTTP URL

```text
[Insecure HTTP URL]
Severity: Low
Message: The code contains an insecure HTTP URL.
Suggestion: Use HTTPS URLs whenever possible.
```

---

## Code Quality and Security Score

CodeLens AI calculates a score from 0 to 100.

The score starts at 100 and decreases based on issue severity:

```text
Critical issue: -20 points
High issue:     -15 points
Medium issue:   -8 points
Low issue:      -4 points
```

Grade mapping:

```text
90 - 100: A, Excellent
75 - 89:  B, Good
60 - 74:  C, Needs Improvement
40 - 59:  D, Poor
0  - 39:  F, Critical
```

---

## Report

After running CodeLens AI, a Markdown report is generated at:

```text
reports/codelens_report.md
```

The report includes:

- Project summary
- Code quality and security score
- Detailed file analysis
- AI codebase explanation
- Code quality issues
- Security issues
- Test suggestions
- Generated pytest files
- Pytest run result

---

## Sample Projects

### Calculator App

The calculator app is a simple project used to test basic code quality analysis.

Run:

```bash
python main.py analyze sample_projects/calculator_app
```

### Vulnerable App

The vulnerable app intentionally contains unsafe code patterns so that CodeLens AI can demonstrate security detection.

Run:

```bash
python main.py analyze sample_projects/vulnerable_app
```

This sample may detect:

- Hardcoded API keys
- Hardcoded passwords
- Insecure HTTP URLs
- `eval()`
- `exec()`
- `os.system()`
- `subprocess.run(..., shell=True)`
- `pickle.load()`
- `yaml.load()` without SafeLoader

---

## GitHub Actions

This project includes a GitHub Actions workflow:

```text
.github/workflows/codelens.yml
```

The workflow automatically runs on:

- Push to `main`
- Pull request to `main`
- Manual workflow trigger

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

---

## Current Status

Completed:

- Static Python code scanner
- Rule-based code quality analyzer
- Rule-based security analyzer
- Code quality and security score calculator
- Markdown report generator
- Test suggestion generator
- Pytest file generator
- Automatic pytest runner
- AI-powered codebase explanation using Groq
- Sample calculator project
- Sample vulnerable project
- GitHub Actions workflow

---

## Future Improvements

Planned improvements:

- Better AI-generated test cases
- Pull request comment generation
- Support for analyzing larger real-world repositories
- Support for multiple programming languages
- Web dashboard for reports
- JSON report export
- HTML report export

---

## Author

Built as a Python automation and AI code analysis project.