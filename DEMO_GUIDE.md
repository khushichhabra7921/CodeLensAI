# CodeLens AI Demo Guide

This guide helps you present CodeLens AI confidently to a faculty mentor, project evaluator, or interviewer.

---

## 1. One-Line Project Introduction

CodeLens AI is a Python code analysis tool that scans a project, detects code quality and security issues, generates test suggestions, creates pytest tests, calculates a quality score, tracks score history, supports config files, and exports Markdown, JSON, and HTML reports.

---

## 2. Simple Explanation

CodeLens AI works like a lightweight AI-powered code review assistant.

It takes a Python project as input and automatically checks:

- What files are present
- What functions and classes exist
- Whether functions/classes have docstrings
- Whether functions are too long
- Whether functions have too many arguments
- Whether division operations may cause runtime errors
- Whether unsafe security patterns exist
- Whether generated tests pass
- What overall score the project deserves
- Whether the score improved, declined, or stayed unchanged compared to previous runs

It can be controlled using:

- CLI options
- A root-level `codelens.yml` config file

Then it creates reports that can be viewed in:

- Markdown format
- JSON format
- HTML format

It also creates score history files to track project health over time.

---

## 3. Problem Statement

Developers often need to manually review code for quality, security, testing, and documentation issues.

Manual review can be:

- Time-consuming
- Inconsistent
- Easy to forget
- Difficult for beginners
- Hard to automate in small projects
- Difficult to compare over time
- Hard to standardize across multiple runs

CodeLens AI solves this by automatically analyzing Python projects and generating clear reports with scoring, history tracking, and configuration support.

---

## 4. Main Goal

The main goal of CodeLens AI is to automate basic code review for Python projects.

It helps developers quickly understand:

- The structure of a codebase
- Code quality problems
- Security risks
- Missing tests
- Overall code health
- Score trend between multiple analysis runs
- Reusable project settings through `codelens.yml`

---

## 5. Current Features

CodeLens AI currently supports:

- Python project scanning
- AST-based code analysis
- Code quality issue detection
- Security issue detection
- Code quality and security scoring
- Score history tracking
- Test suggestion generation
- Pytest file generation
- Automatic pytest execution
- AI-generated codebase explanation using Groq
- Markdown report generation
- JSON report generation
- HTML report generation
- CLI options
- Config file support using `codelens.yml`
- GitHub Actions automation

---

## 6. Project Architecture

```text
User Command
    |
    v
main.py
    |
    |-- config_loader.py
    |       Loads codelens.yml and merges config with CLI options
    |
    |-- scanner.py
    |       Scans Python files and extracts imports, functions, classes, and metadata
    |
    |-- analyzer.py
    |       Detects code quality issues
    |
    |-- security_analyzer.py
    |       Detects security issues
    |
    |-- score_calculator.py
    |       Calculates score and grade
    |
    |-- test_generator.py
    |       Creates test suggestions
    |
    |-- test_writer.py
    |       Writes pytest test files
    |
    |-- test_runner.py
    |       Runs pytest automatically
    |
    |-- ai_explainer.py
    |       Generates AI explanation using Groq
    |
    |-- reporter.py
    |       Generates Markdown report
    |
    |-- json_reporter.py
    |       Generates JSON report
    |
    |-- html_reporter.py
    |       Generates HTML report
    |
    |-- history_tracker.py
            Tracks score history across runs
```

---

## 7. Important Files to Explain

### `main.py`

This is the entry point of the project.

It controls the full workflow:

```text
Parse CLI arguments
Load codelens.yml config
Resolve final runtime options
Scan project
Analyze code quality
Analyze security
Calculate score
Generate tests
Run tests
Generate AI explanation
Generate reports
Update score history
Print output
```

---

### `codelens/config_loader.py`

This file loads the config file:

```text
codelens.yml
```

It handles:

- Default config values
- YAML parsing
- Deep merging user config with defaults
- Config validation
- Report format normalization

It makes the tool easier to use because users can define default settings once instead of typing long commands every time.

---

### `codelens.yml`

This is the project-level configuration file.

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

### `codelens/scanner.py`

This file scans Python files using Python's AST module.

It extracts:

- Imports
- Functions
- Classes
- Function arguments
- Line numbers
- Docstring availability
- Function length
- Division usage

---

### `codelens/analyzer.py`

This file detects code quality issues such as:

- Missing docstrings
- Possible division-by-zero risks
- Too many arguments
- Long functions

It also uses config values such as:

```yaml
rules:
  max_function_lines: 30
  max_arguments: 5
```

---

### `codelens/security_analyzer.py`

This file detects common security issues such as:

- `eval()`
- `exec()`
- `os.system()`
- `subprocess.run(..., shell=True)`
- `pickle.load()`
- `yaml.load()` without SafeLoader
- Hardcoded secrets
- Insecure HTTP URLs

It can be controlled using config:

```yaml
rules:
  check_security: true
  allow_http_urls: false
```

---

### `codelens/score_calculator.py`

This file calculates a score from 0 to 100.

The score starts at 100 and decreases based on issue severity.

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

### `codelens/history_tracker.py`

This file tracks project score history over multiple runs.

It generates:

```text
reports/score_history.json
reports/score_history.md
```

It stores:

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
- Report paths

Trend values can be:

```text
First run for this project
Improved
Declined
Unchanged
```

---

### `codelens/test_generator.py`

This file generates suggested test cases for each function.

For example:

```text
Test normal input
Test edge cases
Test invalid input
```

---

### `codelens/test_writer.py`

This file writes actual pytest files into:

```text
generated_tests/
```

---

### `codelens/test_runner.py`

This file runs pytest automatically using Python subprocess.

It returns:

- Whether tests passed
- Command used
- Return code
- Standard output
- Error output

---

### `codelens/ai_explainer.py`

This file uses Groq API to generate an AI explanation of the analyzed codebase.

If the API key is missing, the project can still run using config:

```yaml
analysis:
  skip_ai: true
```

or CLI:

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

---

### `codelens/reporter.py`

This file generates:

```text
reports/codelens_report.md
```

This report is good for reading inside VS Code or GitHub.

---

### `codelens/json_reporter.py`

This file generates:

```text
reports/codelens_report.json
```

This report is useful for:

- Dashboards
- APIs
- GitHub Actions artifacts
- Future data visualization
- Score tracking

---

### `codelens/html_reporter.py`

This file generates:

```text
reports/codelens_report.html
```

This report is useful for:

- Browser viewing
- Project demo
- Faculty mentor presentation
- Visual explanation

---

## 8. Demo Flow

Use this order during your demo.

---

### Step 1: Introduce the Project

Say:

> CodeLens AI is a Python code analysis tool that automatically scans a project, detects code quality and security issues, generates tests, calculates a score, tracks score history, supports config files, and exports reports in Markdown, JSON, and HTML.

---

### Step 2: Show the Project Structure

Show these files and folders:

```text
codelens/
sample_projects/
generated_tests/
reports/
.github/workflows/
codelens.yml
```

Explain:

> The `codelens` folder contains the actual tool logic. The `sample_projects` folder contains example projects. The `reports` folder stores generated reports. The `.github/workflows` folder contains GitHub Actions automation. The `codelens.yml` file stores default configuration.

---

### Step 3: Show the Config File

Open:

```text
codelens.yml
```

Explain:

> This config file allows users to set default project path, report format, output folder, AI behavior, test behavior, history tracking, and analysis rule thresholds.

Point out:

```yaml
project:
  default_path: sample_projects/calculator_app

analysis:
  skip_ai: true

rules:
  max_function_lines: 30
  max_arguments: 5
```

---

### Step 4: Run Analysis Using Config Only

Run:

```bash
python main.py analyze
```

Explain:

> I do not need to pass the project path here because CodeLens AI reads it from `codelens.yml`.

Expected output includes:

```text
Runtime Options
----------------------------------------
Project path: sample_projects/calculator_app
Report format: all
Output directory: reports
Skip AI: True
```

---

### Step 5: Run Calculator App Again to Show History

Run:

```bash
python main.py analyze
```

Explain:

> Running the same project again updates the score history and compares the latest score with the previous run.

Expected output may include:

```text
Score History
----------------------------------------
Total runs tracked: 2
Trend: Unchanged
Previous score: 53/100
Score change: 0
```

---

### Step 6: Open HTML Report

Run:

```bash
start reports/codelens_report.html
```

Explain:

> This opens the browser-friendly report, which is useful for demos and presentations.

Show sections:

- Project Summary
- Code Quality and Security Score
- Code Quality Issues
- Security Issues
- Detailed File Analysis
- Test Suggestions
- Generated Pytest Files
- AI Codebase Explanation

---

### Step 7: Show Score History Report

Open:

```text
reports/score_history.md
```

Explain:

> This report tracks previous runs and shows whether the project score improved, declined, or stayed unchanged.

Show:

- Latest run
- Score
- Previous score
- Score change
- Trend
- Run history table

---

### Step 8: Run Vulnerable App Using CLI Override

Run:

```bash
python main.py analyze sample_projects/vulnerable_app --format html --skip-tests
```

Explain:

> Here I override the config file from the command line. The config file default project is calculator app, but this command analyzes the vulnerable app instead.

Expected security issues:

```text
Hardcoded Secret
Unsafe eval Usage
Unsafe exec Usage
Unsafe os.system Usage
Subprocess shell=True
Unsafe Pickle Usage
Unsafe YAML Load
Insecure HTTP URL
```

---

### Step 9: Show JSON Report

Open:

```text
reports/codelens_report.json
```

Explain:

> The JSON report is useful for dashboards, APIs, GitHub Actions artifacts, and future automation.

---

### Step 10: Show GitHub Actions

Open:

```text
.github/workflows/codelens.yml
```

Explain:

> This workflow runs CodeLens AI automatically whenever code is pushed to GitHub or a pull request is opened. It uses the `codelens.yml` config and uploads Markdown, JSON, HTML, and score history reports as artifacts.

---

## 9. Useful Commands

### Analyze using config

```bash
python main.py analyze
```

### Analyze using a specific config file

```bash
python main.py analyze --config codelens.yml
```

### Analyze calculator app directly

```bash
python main.py analyze sample_projects/calculator_app
```

### Analyze vulnerable app

```bash
python main.py analyze sample_projects/vulnerable_app --skip-tests
```

### Generate all reports

```bash
python main.py analyze sample_projects/calculator_app --format all
```

### Generate only HTML report

```bash
python main.py analyze sample_projects/calculator_app --format html
```

### Skip AI explanation

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

### Force AI explanation

```bash
python main.py analyze sample_projects/calculator_app --use-ai
```

### Skip test generation and pytest

```bash
python main.py analyze sample_projects/vulnerable_app --skip-tests
```

### Force tests to run

```bash
python main.py analyze sample_projects/calculator_app --run-tests
```

### Disable score history tracking

```bash
python main.py analyze sample_projects/calculator_app --no-history
```

### Force score history tracking

```bash
python main.py analyze sample_projects/calculator_app --track-history
```

### Custom output folder

```bash
python main.py analyze sample_projects/calculator_app --output-dir custom_reports
```

### Run generated tests manually

```bash
python -m pytest generated_tests -v
```

### Open HTML report on Windows

```bash
start reports/codelens_report.html
```

### Open score history Markdown in VS Code

```bash
code reports/score_history.md
```

---

## 10. What to Say During Demo

### Opening

> Today I am presenting CodeLens AI, a Python code analysis and reporting tool. It scans a Python project, detects code quality and security issues, generates pytest suggestions and test files, runs those tests, calculates a score, tracks score history, supports config files, and creates Markdown, JSON, and HTML reports.

---

### While showing config

> The `codelens.yml` file stores default settings like project path, report format, output directory, whether AI should be skipped, whether tests should run, whether history should be tracked, and rule thresholds such as maximum function length and maximum arguments.

---

### While showing scanner

> The scanner uses Python's AST module, so it analyzes the structure of the Python code instead of just reading text line by line.

---

### While showing analyzer

> The analyzer applies rule-based checks for maintainability issues like missing docstrings, long functions, too many arguments, and possible division-by-zero problems. These thresholds can now be changed from the config file.

---

### While showing security analyzer

> The security analyzer detects risky patterns such as eval, exec, os.system, shell=True, pickle loading, unsafe YAML loading, hardcoded secrets, and insecure HTTP URLs. Security checks can also be enabled or disabled from config.

---

### While showing score

> The score starts at 100 and decreases based on issue severity. This gives a quick overview of project health.

---

### While showing score history

> The score history feature stores previous analysis runs and compares the latest score with the earlier score for the same project. This helps track whether the project is improving, declining, or staying unchanged.

---

### While showing reports

> The Markdown report is human-readable in VS Code, the JSON report is machine-readable for integrations, and the HTML report is useful for demos and future dashboards.

---

### Closing

> The project currently works as a complete static analysis and reporting tool. In the future, I can extend it with better AI-generated tests, pull request comments, dependency vulnerability scanning, issue trend comparison, and support for larger repositories.

---

## 11. Mentor Questions and Good Answers

### Q1. Why did you use AST instead of simple string matching?

**Answer:**

AST gives the actual structure of the Python code. It can identify functions, classes, imports, arguments, and line numbers more reliably than simple string matching.

---

### Q2. What is AST?

**Answer:**

AST stands for Abstract Syntax Tree. It is a tree representation of source code. Python can parse code into an AST, and then we can inspect nodes like functions, classes, imports, and function calls.

---

### Q3. Why did you add config file support?

**Answer:**

Config file support makes the tool easier to reuse. Users can define default project paths, report formats, output folders, analysis settings, and rule thresholds once in `codelens.yml` instead of passing long CLI commands every time.

---

### Q4. Which has priority: CLI options or config file?

**Answer:**

CLI options override the config file. This is the expected behavior in many developer tools because the config provides defaults, while CLI options allow temporary changes.

---

### Q5. Is this a replacement for tools like SonarQube or Bandit?

**Answer:**

No. CodeLens AI is a lightweight educational and project-level tool. It demonstrates how static analysis, security detection, test generation, scoring, report generation, config support, and trend tracking can be combined. It is not intended to replace mature production tools.

---

### Q6. How does security detection work?

**Answer:**

It parses the Python file using AST and looks for known risky patterns such as `eval`, `exec`, `os.system`, subprocess calls with `shell=True`, unsafe pickle usage, unsafe YAML loading, hardcoded secrets, and insecure HTTP URLs.

---

### Q7. Can it detect every possible security vulnerability?

**Answer:**

No. It currently detects common static patterns. More advanced vulnerabilities require deeper data-flow analysis, dependency analysis, and context-aware checks.

---

### Q8. How is the score calculated?

**Answer:**

The score starts at 100. It subtracts points based on severity:

```text
Critical: -20
High:     -15
Medium:   -8
Low:      -4
```

Then it assigns a grade from A to F.

---

### Q9. What does score history tracking do?

**Answer:**

Score history tracking stores the score from each run and compares the latest score with the previous score for the same project. It shows whether the project improved, declined, or stayed unchanged.

---

### Q10. Where is score history stored?

**Answer:**

It is stored in:

```text
reports/score_history.json
reports/score_history.md
```

The JSON file is machine-readable, and the Markdown file is human-readable.

---

### Q11. Why did you generate JSON reports?

**Answer:**

JSON reports make the tool easier to integrate with dashboards, APIs, GitHub Actions, and future visualizations.

---

### Q12. Why did you generate HTML reports?

**Answer:**

HTML reports are easier to view in a browser and are useful for demos, presentations, and future dashboard development.

---

### Q13. How does test generation work?

**Answer:**

The tool reads function names and arguments, creates test suggestions, writes pytest test files, and then runs pytest automatically.

---

### Q14. Are the generated tests perfect?

**Answer:**

No. The current test generation is basic. A future improvement is to use AI to generate more accurate and context-aware test cases.

---

### Q15. Why did you add CLI options?

**Answer:**

CLI options make the project more flexible and professional. Users can choose report format, skip AI, skip tests, disable history, set custom output directories, and override config defaults.

---

### Q16. What happens if Groq API key is missing?

**Answer:**

The user can run the project with:

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

or set this in `codelens.yml`:

```yaml
analysis:
  skip_ai: true
```

This skips AI explanation and still generates reports.

---

### Q17. What is the role of GitHub Actions?

**Answer:**

GitHub Actions automatically runs CodeLens AI when code is pushed or a pull request is opened. It uses `codelens.yml` and uploads generated reports and score history files as artifacts.

---

### Q18. What is the biggest limitation right now?

**Answer:**

The main limitations are that test generation is basic, security detection is rule-based, and the tool currently supports only Python.

---

### Q19. What are the next improvements?

**Answer:**

Next improvements can include better AI-generated tests, pull request comments, dependency vulnerability scanning, issue trend comparison, HTML dashboard, and support for larger repositories.

---

## 12. Common Demo Mistakes to Avoid

Do not start by explaining every file immediately.

Start with:

```text
What problem does the project solve?
What does the tool do?
How do we run it?
What output does it generate?
```

Then explain the internal files.

---

Do not say:

> This detects all security vulnerabilities.

Say:

> This detects common static security patterns.

---

Do not say:

> The generated tests are perfect.

Say:

> The current test generation is basic and can be improved using AI.

---

Do not spend too much time on README.

Instead, focus on:

- Running commands
- Showing config
- Showing report output
- Explaining architecture
- Showing security detection
- Showing score history

---

## 13. Recommended Demo Order

Use this exact order:

```text
1. Open README.md
2. Explain project in one line
3. Show folder structure
4. Open codelens.yml
5. Open main.py
6. Run analysis using config: python main.py analyze
7. Run it again to show score history
8. Open HTML report
9. Open score_history.md
10. Run vulnerable app using CLI override
11. Show detected security issues
12. Open JSON report
13. Show GitHub Actions workflow
14. Explain future improvements
```

---

## 14. Final Presentation Script

Use this script if you need to present quickly.

> CodeLens AI is a Python code analysis tool that combines static analysis, security checks, test generation, scoring, score history tracking, config file support, and report generation.  
>
> The project takes a Python folder as input. It can get that input from the command line or from a `codelens.yml` config file.  
>
> It scans all Python files using the AST module and extracts functions, classes, imports, arguments, line numbers, docstrings, and other metadata.  
>
> Then it performs code quality analysis to detect issues like missing docstrings, long functions, too many arguments, and possible runtime errors.  
>
> It also performs security analysis to detect risky patterns such as eval, exec, os.system, shell=True, pickle loading, unsafe YAML loading, hardcoded secrets, and insecure HTTP URLs.  
>
> Based on the detected issues, it calculates a code quality and security score from 0 to 100.  
>
> It also generates pytest test suggestions, writes pytest files, runs them automatically, and includes the test results in the final reports.  
>
> The tool generates Markdown, JSON, and HTML reports. Markdown is useful for reading in VS Code, JSON is useful for integration, and HTML is useful for browser-based demos.  
>
> It also tracks score history over multiple runs, so we can see whether a project is improving, declining, or staying unchanged.  
>
> I added CLI options and config file support so users can choose the report format, skip AI explanation, skip tests, disable history tracking, set custom output directories, and define rule thresholds.  
>
> The project is integrated with GitHub Actions, so analysis can run automatically on push and pull requests.  
>
> Future improvements include better AI-generated tests, pull request comments, dependency vulnerability scanning, issue trend comparison, and support for larger repositories.

---

## 15. Final Checklist Before Demo

Before presenting, run:

```bash
git status
```

Make sure it says:

```text
nothing to commit, working tree clean
```

Then run:

```bash
python main.py analyze
```

Run it again:

```bash
python main.py analyze
```

Then run:

```bash
python main.py analyze sample_projects/vulnerable_app --format html --skip-tests
```

Then open:

```bash
start reports/codelens_report.html
```

Open score history:

```bash
code reports/score_history.md
```

Make sure the HTML report and score history open properly.

---

## 16. What You Have Completed

Completed modules:

- Scanner
- Code quality analyzer
- Security analyzer
- Score calculator
- Score history tracker
- Config loader
- Test suggestion generator
- Pytest writer
- Pytest runner
- AI explainer
- Markdown reporter
- JSON reporter
- HTML reporter
- CLI options
- Config file support
- GitHub Actions workflow
- README documentation
- Demo guide
- Vulnerable sample project

---

## 17. Best Next Technical Improvements

Recommended future technical improvements:

1. AI-based test case generation
2. Pull request comment generation
3. More security rules
4. Dependency vulnerability scanning
5. Issue trend comparison by issue type
6. HTML dashboard with charts
7. Support for large repositories
8. Support for JavaScript or Java
9. Advanced config profiles
10. Exporting report summaries as GitHub PR comments

---

## 18. Short Closing Statement

> CodeLens AI demonstrates how static analysis, AI explanation, security checks, testing, scoring, score history tracking, config support, and report generation can be combined into one automated developer tool.