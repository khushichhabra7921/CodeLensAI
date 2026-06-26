# CodeLens AI

![CodeLens AI Analysis](https://github.com/khushichhabra7921/CodeLensAI/actions/workflows/codelens.yml/badge.svg)

CodeLens AI is an AI-powered Python code analysis tool that scans a Python project, detects code quality issues, detects common security risks, generates pytest test suggestions, creates actual pytest test files, runs those tests automatically, calculates a code quality and security score, tracks score history over multiple runs, and produces Markdown, JSON, and HTML reports with an AI-generated explanation of the codebase.

It also supports a project-level configuration file named `codelens.yml`, so users can define default project paths, report formats, output folders, analysis settings, and rule thresholds.

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
- Tracks score history between analysis runs
- Shows whether the score improved, declined, or stayed unchanged
- Generates pytest test suggestions
- Creates actual pytest test files
- Runs generated pytest tests automatically
- Generates a Markdown report
- Generates a structured JSON report
- Generates a browser-friendly HTML report
- Generates score history reports
- Supports CLI options for report format, skipping AI, skipping tests, and disabling history
- Supports project configuration using `codelens.yml`
- Supports custom rule settings from config
- Uses Groq LLM to generate an AI explanation of the codebase
- Runs automatically on GitHub Actions for every push and pull request
- Uploads reports as GitHub Actions artifacts

---

## Tech Stack

- Python
- AST module
- Pytest
- Groq LLM
- python-dotenv
- PyYAML
- GitHub Actions
- Markdown report generation
- JSON report generation
- HTML report generation
- Score history tracking
- argparse CLI
- YAML configuration

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
│   ├── config_loader.py
│   ├── history_tracker.py
│   ├── html_reporter.py
│   ├── json_reporter.py
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
│   ├── codelens_report.md
│   ├── codelens_report.json
│   ├── codelens_report.html
│   ├── score_history.json
│   └── score_history.md
│
├── .env
├── .gitignore
├── codelens.yml
├── DEMO_GUIDE.md
├── main.py
├── README.md
└── requirements.txt
```

---

## How It Works

```text
User runs CodeLens AI
        ↓
CodeLens loads CLI options and codelens.yml config
        ↓
It resolves project path, report format, output folder, and analysis settings
        ↓
It scans all Python files
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
It creates Markdown, JSON, and HTML reports
        ↓
It updates score history and trend reports
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

You can also run the project without AI explanation by using:

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

---

## Configuration File

CodeLens AI supports a root-level config file:

```text
codelens.yml
```

Example:

```yaml
project:
  default_path: sample_projects/calculator_app

reports:
  format: all
  output_dir: reports

analysis:
  skip_ai: true
  skip_tests: false
  track_history: true

rules:
  max_function_lines: 30
  max_arguments: 5
  check_security: true
  allow_http_urls: false
```

---

## Config Options

### `project.default_path`

Default project folder to analyze when no path is provided.

```yaml
project:
  default_path: sample_projects/calculator_app
```

This allows:

```bash
python main.py analyze
```

---

### `reports.format`

Controls which report format to generate.

Allowed values:

```text
all
markdown
md
json
html
```

Example:

```yaml
reports:
  format: html
```

---

### `reports.output_dir`

Controls where reports are saved.

```yaml
reports:
  output_dir: reports
```

---

### `analysis.skip_ai`

Skips AI explanation generation.

```yaml
analysis:
  skip_ai: true
```

Useful when:

- You do not have a Groq API key
- You want faster local testing
- You only want static analysis reports

---

### `analysis.skip_tests`

Skips pytest file generation and pytest execution.

```yaml
analysis:
  skip_tests: false
```

---

### `analysis.track_history`

Controls score history tracking.

```yaml
analysis:
  track_history: true
```

---

### `rules.max_function_lines`

Controls the line-count threshold for long function detection.

```yaml
rules:
  max_function_lines: 30
```

---

### `rules.max_arguments`

Controls the argument-count threshold for too many arguments.

```yaml
rules:
  max_arguments: 5
```

---

### `rules.check_security`

Enables or disables security analysis.

```yaml
rules:
  check_security: true
```

---

### `rules.allow_http_urls`

Controls whether insecure `http://` URLs should be reported.

```yaml
rules:
  allow_http_urls: false
```

---

## CLI Overrides Config

CLI options override values from `codelens.yml`.

For example, if config has:

```yaml
analysis:
  skip_ai: true
```

You can force AI generation with:

```bash
python main.py analyze --use-ai
```

If config has:

```yaml
analysis:
  skip_tests: true
```

You can force tests to run with:

```bash
python main.py analyze --run-tests
```

---

## Basic Usage

Analyze the default project from `codelens.yml`:

```bash
python main.py analyze
```

Analyze the calculator sample project:

```bash
python main.py analyze sample_projects/calculator_app
```

Analyze the vulnerable sample project:

```bash
python main.py analyze sample_projects/vulnerable_app
```

Use a specific config file:

```bash
python main.py analyze --config codelens.yml
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

## CLI Options

### Generate All Reports

```bash
python main.py analyze sample_projects/calculator_app --format all
```

This creates:

```text
reports/codelens_report.md
reports/codelens_report.json
reports/codelens_report.html
reports/score_history.json
reports/score_history.md
```

---

### Generate Only Markdown Report

```bash
python main.py analyze sample_projects/calculator_app --format markdown
```

or:

```bash
python main.py analyze sample_projects/calculator_app --format md
```

---

### Generate Only JSON Report

```bash
python main.py analyze sample_projects/calculator_app --format json
```

---

### Generate Only HTML Report

```bash
python main.py analyze sample_projects/calculator_app --format html
```

---

### Skip AI Explanation

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

---

### Force AI Explanation

```bash
python main.py analyze sample_projects/calculator_app --use-ai
```

---

### Skip Test Generation and Pytest Run

```bash
python main.py analyze sample_projects/calculator_app --skip-tests
```

---

### Force Test Generation and Pytest Run

```bash
python main.py analyze sample_projects/calculator_app --run-tests
```

---

### Disable Score History Tracking

```bash
python main.py analyze sample_projects/calculator_app --no-history
```

---

### Force Score History Tracking

```bash
python main.py analyze sample_projects/calculator_app --track-history
```

---

### Combine Options

```bash
python main.py analyze sample_projects/vulnerable_app --format html --skip-ai --skip-tests
```

---

### Custom Output Directory

```bash
python main.py analyze sample_projects/calculator_app --output-dir custom_reports
```

This creates reports inside:

```text
custom_reports/
```

---

## Example Terminal Output

```text
Runtime Options
----------------------------------------
Project path: sample_projects/calculator_app
Report format: all
Output directory: reports
Skip AI: True
Skip tests: False
Track history: True
Check security: True
Max function lines: 30
Max arguments: 5
Allow HTTP URLs: False

CodeLens AI Report
========================================
Files scanned: 1
Imports found: 0
Functions found: 7
Classes found: 0
Total issues found: 7
Code quality issues found: 7
Security issues found: 0
Test suggestions generated: 7
Pytest files generated: 1
Test run status: Passed
AI explanation generated: False (skipped)

Code Quality and Security Score
----------------------------------------
Score: 53/100
Grade: D
Status: Poor
Critical severity issues: 0
High severity issues: 1
Medium severity issues: 2
Low severity issues: 4

Score History
----------------------------------------
Total runs tracked: 2
Trend: Unchanged
Previous score: 53/100
Score change: 0

Markdown report generated: reports/codelens_report.md
JSON report generated: reports/codelens_report.json
HTML report generated: reports/codelens_report.html
Score history JSON generated: reports/score_history.json
Score history Markdown generated: reports/score_history.md
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

## Score History Tracking

CodeLens AI tracks score history across runs.

It generates:

```text
reports/score_history.json
reports/score_history.md
```

### `score_history.json`

This file stores structured score history data.

It includes:

- Run timestamp
- Project path
- Current score
- Previous score
- Score change
- Trend
- Grade
- Status
- Issue counts
- Test status
- Generated report paths

### `score_history.md`

This file stores a readable history table.

It shows:

- Latest run
- Current score
- Previous score
- Score change
- Trend
- Recent run history

Trend values can be:

```text
First run for this project
Improved
Declined
Unchanged
```

To avoid updating history during temporary testing:

```bash
python main.py analyze sample_projects/calculator_app --no-history
```

---

## Reports

After running CodeLens AI, reports are generated inside:

```text
reports/
```

Main reports:

```text
reports/codelens_report.md
reports/codelens_report.json
reports/codelens_report.html
```

Score history reports:

```text
reports/score_history.json
reports/score_history.md
```

### Markdown Report

The Markdown report is useful for:

- Reading inside VS Code
- Uploading as a GitHub Actions artifact
- Sharing project analysis in text format

### JSON Report

The JSON report is useful for:

- Web dashboards
- GitHub Actions artifacts
- API integrations
- Charts and visualizations
- Score history tracking
- Comparing projects over time

### HTML Report

The HTML report is useful for:

- Browser viewing
- Project demos
- Faculty mentor presentations
- Future dashboard design

Open the HTML report on Windows:

```bash
start reports/codelens_report.html
```

---

## Sample Projects

### Calculator App

The calculator app is a simple project used to test basic code quality analysis.

Run:

```bash
python main.py analyze sample_projects/calculator_app
```

or simply:

```bash
python main.py analyze
```

if `codelens.yml` has:

```yaml
project:
  default_path: sample_projects/calculator_app
```

---

### Vulnerable App

The vulnerable app intentionally contains unsafe code patterns so that CodeLens AI can demonstrate security detection.

Run:

```bash
python main.py analyze sample_projects/vulnerable_app --skip-tests
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
Run CodeLens AI using codelens.yml config
        ↓
Run generated pytest tests
        ↓
Upload Markdown, JSON, HTML, and score history reports as artifacts
```

The uploaded artifact contains:

```text
reports/codelens_report.md
reports/codelens_report.json
reports/codelens_report.html
reports/score_history.json
reports/score_history.md
```

---

## Git Ignore Note

The `reports/` and `generated_tests/` folders are generated output folders.

They are usually ignored by Git because they are created automatically whenever CodeLens AI runs.

---

## Current Status

Completed:

- Static Python code scanner
- Rule-based code quality analyzer
- Rule-based security analyzer
- Code quality and security score calculator
- Markdown report generator
- JSON report generator
- HTML report generator
- Score history tracking
- CLI options
- Config file support using `codelens.yml`
- Test suggestion generator
- Pytest file generator
- Automatic pytest runner
- AI-powered codebase explanation using Groq
- Sample calculator project
- Sample vulnerable project
- Demo guide
- GitHub Actions workflow
- GitHub Actions report artifact upload

---

## Future Improvements

Planned improvements:

- Better AI-generated test cases
- Pull request comment generation
- Support for analyzing larger real-world repositories
- Support for multiple programming languages
- Web dashboard for reports
- Issue trend comparison between runs
- More security rules
- Dependency vulnerability scanning
- Advanced config rule profiles
- Exporting report summaries as GitHub PR comments

---

## Author

Built as a Python automation and AI code analysis project.