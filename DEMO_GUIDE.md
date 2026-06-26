# CodeLens AI Demo Guide

This guide helps you present CodeLens AI confidently to a faculty mentor, project evaluator, or interviewer.

---

## 1. One-Line Project Introduction

CodeLens AI is a Python code analysis tool that scans a project, detects code quality and security issues, generates test suggestions, creates pytest tests, calculates a quality score, tracks score history, and exports Markdown, JSON, and HTML reports.

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

CodeLens AI solves this by automatically analyzing Python projects and generating clear reports with score tracking.

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
- GitHub Actions automation

---

## 6. Project Architecture

```text
User Command
    |
    v
main.py
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

If the API key is missing, the project can still run using:

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

> CodeLens AI is a Python code analysis tool that automatically scans a project, detects code quality and security issues, generates tests, calculates a score, tracks score history, and exports reports in Markdown, JSON, and HTML.

---

### Step 2: Show the Project Structure

Show these folders:

```text
codelens/
sample_projects/
generated_tests/
reports/
.github/workflows/
```

Explain:

> The `codelens` folder contains the actual tool logic. The `sample_projects` folder contains example projects. The `reports` folder stores generated reports. The `.github/workflows` folder contains GitHub Actions automation.

---

### Step 3: Run Calculator App Analysis

Run:

```bash
python main.py analyze sample_projects/calculator_app --format all --skip-ai
```

Explain:

> This command analyzes a simple calculator project and generates all report formats. I am using `--skip-ai` here so the demo runs quickly even without depending on an API call.

Expected output includes:

```text
Markdown report generated: reports/codelens_report.md
JSON report generated: reports/codelens_report.json
HTML report generated: reports/codelens_report.html
Score history JSON generated: reports/score_history.json
Score history Markdown generated: reports/score_history.md
```

---

### Step 4: Run Calculator App Again to Show History

Run the same command again:

```bash
python main.py analyze sample_projects/calculator_app --format all --skip-ai
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

### Step 5: Open HTML Report

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

### Step 6: Show Score History Report

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

### Step 7: Run Vulnerable App Analysis

Run:

```bash
python main.py analyze sample_projects/vulnerable_app --format all --skip-ai --skip-tests
```

Explain:

> This project intentionally contains unsafe code so that we can demonstrate the security analyzer. I am using `--skip-tests` because this project is mainly for security demonstration.

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

### Step 8: Show JSON Report

Open:

```text
reports/codelens_report.json
```

Explain:

> The JSON report is useful for dashboards, APIs, GitHub Actions artifacts, and future automation.

---

### Step 9: Show GitHub Actions

Open:

```text
.github/workflows/codelens.yml
```

Explain:

> This workflow runs CodeLens AI automatically whenever code is pushed to GitHub or a pull request is opened. It also uploads Markdown, JSON, HTML, and score history reports as artifacts.

---

## 9. Useful Commands

### Analyze and generate all reports

```bash
python main.py analyze sample_projects/calculator_app --format all
```

### Analyze quickly without AI

```bash
python main.py analyze sample_projects/calculator_app --format all --skip-ai
```

### Generate only HTML report

```bash
python main.py analyze sample_projects/calculator_app --format html
```

### Skip AI explanation

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

### Skip test generation and pytest

```bash
python main.py analyze sample_projects/vulnerable_app --skip-tests
```

### Skip both AI and tests

```bash
python main.py analyze sample_projects/vulnerable_app --format html --skip-ai --skip-tests
```

### Disable score history tracking

```bash
python main.py analyze sample_projects/calculator_app --no-history
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

> Today I am presenting CodeLens AI, a Python code analysis and reporting tool. It scans a Python project, detects code quality and security issues, generates pytest suggestions and test files, runs those tests, calculates a score, tracks score history, and creates Markdown, JSON, and HTML reports.

---

### While showing scanner

> The scanner uses Python's AST module, so it analyzes the structure of the Python code instead of just reading text line by line.

---

### While showing analyzer

> The analyzer applies rule-based checks for maintainability issues like missing docstrings, long functions, too many arguments, and possible division-by-zero problems.

---

### While showing security analyzer

> The security analyzer detects risky patterns such as eval, exec, os.system, shell=True, pickle loading, unsafe YAML loading, hardcoded secrets, and insecure HTTP URLs.

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

> The project currently works as a complete static analysis and reporting tool. In the future, I can extend it with better AI-generated tests, pull request comments, dependency vulnerability scanning, and support for larger repositories.

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

### Q3. Is this a replacement for tools like SonarQube or Bandit?

**Answer:**

No. CodeLens AI is a lightweight educational and project-level tool. It demonstrates how static analysis, security detection, test generation, scoring, report generation, and trend tracking can be combined. It is not intended to replace mature production tools.

---

### Q4. How does security detection work?

**Answer:**

It parses the Python file using AST and looks for known risky patterns such as `eval`, `exec`, `os.system`, subprocess calls with `shell=True`, unsafe pickle usage, unsafe YAML loading, hardcoded secrets, and insecure HTTP URLs.

---

### Q5. Can it detect every possible security vulnerability?

**Answer:**

No. It currently detects common static patterns. More advanced vulnerabilities require deeper data-flow analysis, dependency analysis, and context-aware checks.

---

### Q6. How is the score calculated?

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

### Q7. What does score history tracking do?

**Answer:**

Score history tracking stores the score from each run and compares the latest score with the previous score for the same project. It shows whether the project improved, declined, or stayed unchanged.

---

### Q8. Where is score history stored?

**Answer:**

It is stored in:

```text
reports/score_history.json
reports/score_history.md
```

The JSON file is machine-readable, and the Markdown file is human-readable.

---

### Q9. Why did you generate JSON reports?

**Answer:**

JSON reports make the tool easier to integrate with dashboards, APIs, GitHub Actions, and future visualizations.

---

### Q10. Why did you generate HTML reports?

**Answer:**

HTML reports are easier to view in a browser and are useful for demos, presentations, and future dashboard development.

---

### Q11. How does test generation work?

**Answer:**

The tool reads function names and arguments, creates test suggestions, writes pytest test files, and then runs pytest automatically.

---

### Q12. Are the generated tests perfect?

**Answer:**

No. The current test generation is basic. A future improvement is to use AI to generate more accurate and context-aware test cases.

---

### Q13. Why did you add CLI options?

**Answer:**

CLI options make the project more flexible and professional. Users can choose report format, skip AI, skip tests, disable history, and set custom output directories.

---

### Q14. What happens if Groq API key is missing?

**Answer:**

The user can run the project with:

```bash
python main.py analyze sample_projects/calculator_app --skip-ai
```

This skips AI explanation and still generates reports.

---

### Q15. What is the role of GitHub Actions?

**Answer:**

GitHub Actions automatically runs CodeLens AI when code is pushed or a pull request is opened. It also uploads generated reports and score history files as artifacts.

---

### Q16. What is the biggest limitation right now?

**Answer:**

The main limitations are that test generation is basic, security detection is rule-based, and the tool currently supports only Python.

---

### Q17. What are the next improvements?

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
4. Open main.py
5. Run calculator app analysis
6. Run it again to show score history
7. Open HTML report
8. Open score_history.md
9. Run vulnerable app analysis
10. Show detected security issues
11. Open JSON report
12. Show GitHub Actions workflow
13. Explain future improvements
```

---

## 14. Final Presentation Script

Use this script if you need to present quickly.

> CodeLens AI is a Python code analysis tool that combines static analysis, security checks, test generation, scoring, score history tracking, and report generation.  
>
> The project takes a Python folder as input. It scans all Python files using the AST module and extracts functions, classes, imports, arguments, line numbers, docstrings, and other metadata.  
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
> I added CLI options so users can choose the report format, skip AI explanation, skip tests, disable history tracking, or set a custom output directory.  
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
python main.py analyze sample_projects/calculator_app --format all --skip-ai
```

Run it again:

```bash
python main.py analyze sample_projects/calculator_app --format all --skip-ai
```

Then run:

```bash
python main.py analyze sample_projects/vulnerable_app --format html --skip-ai --skip-tests
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
- Test suggestion generator
- Pytest writer
- Pytest runner
- AI explainer
- Markdown reporter
- JSON reporter
- HTML reporter
- CLI options
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
9. Config file support using `codelens.yml`
10. Exporting report summaries as GitHub PR comments

---

## 18. Short Closing Statement

> CodeLens AI demonstrates how static analysis, AI explanation, security checks, testing, scoring, score history tracking, and report generation can be combined into one automated developer tool.