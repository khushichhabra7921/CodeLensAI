# CodeLens AI Demo Guide

This guide explains how to demonstrate CodeLens AI clearly during a project review, mentor meeting, viva, or presentation.

---

## 1. What to Say First

Start with this:

> CodeLens AI is a Python-based code review automation tool. It scans a Python project, detects code quality issues, security risks, and dependency problems, generates pytest tests, calculates a quality score, tracks score and issue trends, creates Markdown, JSON, and HTML reports, and integrates with GitHub Actions to support pull request comments and quality gate checks.

Then say:

> The goal of this project is to help developers quickly understand the health of a Python codebase and improve code quality before merging or deploying code.

---

## 2. Main Problem Statement

Explain the problem like this:

> Developers often need to manually review code for quality issues, security risks, missing tests, and dependency problems. This process is time-consuming and inconsistent. CodeLens AI automates this process by scanning the project and generating a structured analysis report.

---

## 3. Main Objective

Say:

> The objective of CodeLens AI is to build a lightweight automated code review tool for Python projects that can run locally and inside GitHub Actions.

---

## 4. Current Features

CodeLens AI currently supports:

```text
Code scanner
Code quality analyzer
Security analyzer
Dependency analyzer
Better dependency file support
Ignore / exclude patterns
Score calculator
Score history tracking
Issue trend tracking
Test suggestion generator
Improved pytest generator
Automatic pytest runner
AI codebase explanation
Markdown report
JSON report
HTML dashboard report
Pull request comment generation
Quality gate checks
CLI options
Config file support
GitHub Actions workflow
```

---

## 5. Suggested Demo Flow

Use this order during the demo:

```text
1. Show project structure
2. Show codelens.yml config file
3. Run analysis on calculator sample project
4. Explain terminal output
5. Open HTML dashboard report
6. Open Markdown report
7. Open JSON report briefly
8. Show generated pytest files
9. Show score history
10. Show issue trends
11. Show quality gate report
12. Run vulnerable project demo
13. Explain GitHub Actions workflow
14. Explain PR comment generation
15. End with future improvements
```

---

## 6. Before Demo Checklist

Before starting the demo, run:

```bash
git status
```

Make sure it says:

```text
nothing to commit, working tree clean
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run a quick test:

```bash
python main.py analyze --skip-ai
```

Open the HTML report:

```bash
start reports/codelens_report.html
```

If everything works, you are ready for the demo.

---

## 7. Show Project Structure

Say:

> The project is organized into separate modules so each feature is easy to understand and maintain.

Important files:

```text
main.py
```

This is the main entry point.

```text
codelens/scanner.py
```

Scans Python files and extracts imports, functions, classes, and metadata.

```text
codelens/analyzer.py
```

Detects code quality issues.

```text
codelens/security_analyzer.py
```

Detects security-related risks.

```text
codelens/dependency_analyzer.py
```

Checks dependency files.

```text
codelens/score_calculator.py
```

Calculates the code quality, security, and dependency score.

```text
codelens/test_generator.py
codelens/test_writer.py
codelens/test_runner.py
```

Generate test suggestions, write pytest files, and run generated tests.

```text
codelens/reporter.py
codelens/json_reporter.py
codelens/html_reporter.py
```

Generate Markdown, JSON, and HTML reports.

```text
codelens/history_tracker.py
codelens/issue_trend_tracker.py
```

Track score and issue trends.

```text
codelens/pr_commenter.py
```

Generates pull request comment summary.

```text
codelens/quality_gate.py
```

Evaluates quality gate rules.

```text
codelens/config_loader.py
```

Loads and validates `codelens.yml`.

---

## 8. Show Config File

Open:

```text
codelens.yml
```

Say:

> This config file controls how CodeLens AI runs. It defines the default project path, report format, output directory, analysis options, rule thresholds, dependency file patterns, ignore patterns, PR comment generation, and quality gate rules.

Important section:

```yaml
project:
  default_path: sample_projects/calculator_app
```

Say:

> This tells CodeLens AI which project to analyze by default.

Important section:

```yaml
reports:
  format: all
  output_dir: reports
  generate_pr_comment: true
```

Say:

> This tells the tool to generate all reports and also create a PR comment file.

Important section:

```yaml
analysis:
  skip_ai: true
  skip_tests: false
  track_history: true
  track_issue_trends: true
```

Say:

> AI is skipped by default for faster local and CI runs, but test generation and tracking features are enabled.

Important section:

```yaml
quality_gate:
  enabled: true
  min_score: 0
  max_critical_issues: 0
  max_high_issues: 10
  fail_on_tests_failed: true
```

Say:

> The quality gate decides whether the project passes or fails based on the configured quality rules.

Important section:

```yaml
ignore:
  folders:
    - .git
    - .venv
    - venv
    - generated_tests
    - reports
```

Say:

> Ignore patterns prevent generated reports, tests, virtual environments, and cache folders from being scanned.

---

## 9. Run Calculator Project Demo

Run:

```bash
python main.py analyze sample_projects/calculator_app --format all --skip-ai
```

Say:

> This command analyzes the calculator sample project, generates all report formats, skips AI explanation for faster execution, generates pytest tests, runs them, updates score history, updates issue trends, evaluates quality gate, and creates a PR comment summary.

Point out terminal sections:

```text
Runtime Options
```

Say:

> This shows the final options resolved from the config file and CLI arguments.

```text
CodeLens AI Report
```

Say:

> This shows the project summary, including files scanned, imports, functions, classes, issues, tests, and score.

```text
Code Quality Issues
```

Say:

> This section shows code quality problems such as missing docstrings or long functions.

```text
Security Issues
```

Say:

> This section shows risky security patterns if found.

```text
Dependency Issues
```

Say:

> This section shows dependency hygiene problems, such as unpinned dependencies.

```text
Score History
```

Say:

> This shows whether the score improved, declined, or stayed unchanged compared to previous runs.

```text
Issue Trends
```

Say:

> This shows added, resolved, and unchanged issues.

```text
Quality Gate
```

Say:

> This shows whether the project passes the configured quality rules.

---

## 10. Open HTML Dashboard Report

Run:

```bash
start reports/codelens_report.html
```

Say:

> This is the main visual report. It is useful for developers and reviewers because it presents the analysis in a dashboard format.

Show these sections:

```text
Project Summary
```

Say:

> These cards summarize the number of files, imports, functions, classes, issues, test suggestions, and generated tests.

```text
Code Quality, Security, and Dependency Score
```

Say:

> This score gives a quick understanding of overall project health.

```text
Issue Breakdowns
```

Say:

> These breakdowns show issues by severity, category, and type.

```text
All Issues
```

Say:

> This table gives a complete list of all issues found in the project.

```text
Code Quality Issues
Security Issues
Dependency Issues
```

Say:

> Issues are also separated into categories for easier review.

```text
Detailed File Analysis
```

Say:

> This section shows what CodeLens AI extracted from every Python file.

```text
Test Suggestions
Generated Pytest Files
Pytest Result
```

Say:

> This shows generated test suggestions, generated pytest files, and test execution results.

---

## 11. Open Markdown Report

Run:

```bash
code reports/codelens_report.md
```

Say:

> The Markdown report is useful for documentation, GitHub artifacts, and quick text-based review.

Show that it includes:

```text
Project Summary
Score
Detailed File Analysis
Code Quality Issues
Security Issues
Dependency Issues
Test Suggestions
Generated Pytest Files
Pytest Result
AI Codebase Explanation
```

---

## 12. Open JSON Report

Run:

```bash
code reports/codelens_report.json
```

Say:

> The JSON report is useful for automation and future integrations because all analysis data is stored in a structured format.

Mention:

> This can be used later to build dashboards, APIs, or external integrations.

---

## 13. Show Generated Pytest Files

Open:

```text
generated_tests/
```

or run:

```bash
code generated_tests
```

Say:

> CodeLens AI automatically generates pytest files based on detected functions.

Point out examples such as:

```text
test_add_exists
test_add_is_callable
test_add_adds_positive_numbers
test_subtract_subtracts_numbers
test_multiply_multiplies_numbers
test_divide_divides_numbers
```

Then run:

```bash
python -m pytest generated_tests -v
```

Say:

> The generated tests can be run independently using pytest.

---

## 14. Show Score History

Open:

```bash
code reports/score_history.md
```

Say:

> Score history tracks the score across multiple runs for the same project.

Explain:

```text
Trend: Improved
Trend: Declined
Trend: Unchanged
First run for this project
```

Say:

> This helps developers understand whether code quality is improving over time.

---

## 15. Show Issue Trends

Open:

```bash
code reports/issue_trends.md
```

Say:

> Issue trend tracking compares current issues with the previous run.

Explain:

```text
Added Issues
Resolved Issues
Unchanged Issues
Category Breakdown
Severity Breakdown
Recent Runs
```

Say:

> This is useful because a project may have the same score but different issues. Issue trends show exactly what changed.

---

## 16. Show Quality Gate Report

Open:

```bash
code reports/quality_gate.md
```

Say:

> The quality gate checks whether the project satisfies configured rules.

Show:

```text
Status: PASSED
```

or:

```text
Status: FAILED
```

Say:

> If the quality gate fails, CodeLens AI exits with a non-zero status code. This allows GitHub Actions to fail the CI workflow.

To demonstrate failure temporarily, change in `codelens.yml`:

```yaml
quality_gate:
  min_score: 95
```

Then run:

```bash
python main.py analyze
```

Expected:

```text
Quality Gate
----------------------------------------
Status: FAILED
```

Then change it back:

```yaml
quality_gate:
  min_score: 0
```

Run again:

```bash
python main.py analyze
```

Say:

> I keep the default minimum score at 0 during development so the workflow does not fail too aggressively while features are being built.

---

## 17. Show PR Comment File

Open:

```bash
code reports/pr_comment.md
```

Say:

> This file is designed for GitHub pull request comments.

It includes:

```text
Overall Result
Project Summary
Issue Summary
Top Code Quality Issues
Top Security Issues
Top Dependency Issues
Generated Reports
```

Say:

> In GitHub Actions, this file is posted automatically on pull requests using the GitHub API.

---

## 18. Run Vulnerable Project Demo

Run:

```bash
python main.py analyze sample_projects/vulnerable_app --format all --skip-ai --skip-tests --no-quality-gate
```

Say:

> This sample project intentionally contains vulnerable code patterns. I am disabling tests and quality gate here because the goal is to demonstrate security detection.

Show terminal output under:

```text
Security Issues
```

Explain that CodeLens AI can detect issues such as:

```text
eval()
exec()
os.system()
subprocess shell=True
pickle usage
yaml.load()
hardcoded secrets
insecure HTTP URLs
```

Then open HTML report:

```bash
start reports/codelens_report.html
```

Say:

> The security issues are visible in the dashboard and also affect the overall score.

---

## 19. Show Dependency Analysis

Open:

```text
requirements.txt
```

If it contains:

```text
pytest
groq
python-dotenv
PyYAML
```

Say:

> These are detected as unpinned dependencies because they do not use exact versions.

Explain:

```text
pytest
```

is less reproducible than:

```text
pytest==8.4.1
```

Say:

> Dependency analysis helps make project builds more reliable and safer.

Mention supported dependency files:

```text
requirements.txt
requirements-dev.txt
dev-requirements.txt
requirements/*.txt
pyproject.toml
Pipfile
```

---

## 20. Show GitHub Actions Workflow

Open:

```text
.github/workflows/codelens.yml
```

Say:

> This workflow runs CodeLens AI automatically on push, pull request, or manual trigger.

Explain important steps:

```yaml
- name: Checkout repository
```

Say:

> This gets the project code.

```yaml
- name: Set up Python
```

Say:

> This installs Python in the GitHub Actions runner.

```yaml
- name: Install dependencies
```

Say:

> This installs project dependencies from requirements.txt.

```yaml
- name: Run CodeLens AI using config
```

Say:

> This runs the analysis using codelens.yml.

```yaml
- name: Run generated pytest tests
```

Say:

> This runs the generated pytest files.

```yaml
- name: Comment CodeLens summary on pull request
```

Say:

> This posts or updates a CodeLens AI summary comment on pull requests.

```yaml
- name: Upload CodeLens reports
```

Say:

> This uploads all generated reports as GitHub Actions artifacts.

---

## 21. Commands to Demonstrate

### Default run

```bash
python main.py analyze
```

### Analyze calculator app

```bash
python main.py analyze sample_projects/calculator_app
```

### Analyze vulnerable app

```bash
python main.py analyze sample_projects/vulnerable_app --skip-ai --skip-tests --no-quality-gate
```

### Generate only HTML report

```bash
python main.py analyze --format html
```

### Skip AI

```bash
python main.py analyze --skip-ai
```

### Use AI

```bash
python main.py analyze --use-ai
```

### Skip tests

```bash
python main.py analyze --skip-tests
```

### Disable score history

```bash
python main.py analyze --no-history
```

### Disable issue trends

```bash
python main.py analyze --no-issue-trends
```

### Disable PR comment generation

```bash
python main.py analyze --no-pr-comment
```

### Disable quality gate

```bash
python main.py analyze --no-quality-gate
```

### Custom output directory

```bash
python main.py analyze --output-dir custom_reports
```

---

## 22. How to Explain Architecture

Say:

> CodeLens AI follows a modular architecture. Each responsibility is separated into its own Python file.

Explain:

```text
scanner.py
```

> Reads and understands Python source files using AST.

```text
analyzer.py
```

> Applies code quality rules.

```text
security_analyzer.py
```

> Applies security rules.

```text
dependency_analyzer.py
```

> Checks dependency files.

```text
score_calculator.py
```

> Converts issue severity into a numeric score.

```text
test_generator.py
test_writer.py
test_runner.py
```

> Suggests tests, generates pytest files, and runs them.

```text
reporter.py
json_reporter.py
html_reporter.py
```

> Generate different report formats.

```text
history_tracker.py
issue_trend_tracker.py
```

> Track score and issue changes across runs.

```text
quality_gate.py
```

> Decides whether the project passes quality rules.

```text
pr_commenter.py
```

> Creates pull request summary content.

```text
config_loader.py
```

> Loads and validates configuration.

```text
main.py
```

> Connects all modules together and controls the CLI flow.

---

## 23. How to Explain Scoring

Say:

> The score starts from 100. Each issue reduces the score based on severity.

Use this:

```text
Critical: -20
High:     -15
Medium:   -8
Low:      -4
```

Then say:

> This gives a simple and understandable quality score. More severe issues reduce the score more heavily.

Explain grades:

```text
A: Excellent
B: Good
C: Needs Improvement
D: Poor
F: Critical
```

---

## 24. How to Explain Quality Gate

Say:

> The quality gate converts the analysis result into a pass/fail decision.

Example:

```yaml
quality_gate:
  enabled: true
  min_score: 70
  max_critical_issues: 0
  max_high_issues: 5
  fail_on_tests_failed: true
```

Say:

> This is useful in CI/CD because the workflow can fail automatically if the project quality is below the accepted threshold.

---

## 25. How to Explain PR Comment Generation

Say:

> CodeLens AI generates a compact Markdown summary for pull requests. GitHub Actions reads this file and posts it as a PR comment.

Mention:

> If a previous CodeLens AI comment already exists, the workflow updates the old comment instead of creating duplicate comments.

---

## 26. How to Explain AI Usage

Say:

> AI explanation is optional. The core analysis works without AI. AI is used only to generate a human-readable explanation of the codebase.

Then say:

> This design makes the tool usable even without an API key.

---

## 27. Common Questions and Answers

### Q1. What is CodeLens AI?

Answer:

> CodeLens AI is an automated Python code review tool that scans code, detects quality issues, security issues, dependency issues, generates tests, creates reports, tracks trends, and integrates with GitHub Actions.

---

### Q2. Why did you use AST?

Answer:

> I used Python's AST module because it understands the structure of Python code. It is more reliable than simple string searching for detecting functions, classes, imports, arguments, and docstrings.

---

### Q3. What types of issues does it detect?

Answer:

> It detects code quality issues, security risks, and dependency hygiene issues. For example, missing docstrings, long functions, dangerous functions like eval, hardcoded secrets, insecure URLs, and unpinned dependencies.

---

### Q4. What reports does it generate?

Answer:

> It generates Markdown, JSON, HTML dashboard, score history, issue trends, quality gate report, and PR comment report.

---

### Q5. Why do you generate JSON?

Answer:

> JSON is useful for automation and future integrations. Other systems can read the JSON report and build dashboards or CI checks from it.

---

### Q6. Why do you generate HTML?

Answer:

> The HTML dashboard gives a visual and easy-to-understand summary of the project health.

---

### Q7. What is the quality gate?

Answer:

> The quality gate checks whether the project passes configured rules such as minimum score, maximum high issues, maximum critical issues, and whether tests passed.

---

### Q8. Why is the default minimum score 0?

Answer:

> During development, I kept the default minimum score low so the CI workflow does not fail aggressively while the tool is being built. It can be changed to stricter values like 70 or 80 for production use.

---

### Q9. Can this work in GitHub Actions?

Answer:

> Yes. The project includes a GitHub Actions workflow that runs CodeLens AI automatically, uploads reports, runs generated tests, and comments on pull requests.

---

### Q10. Does it require AI to work?

Answer:

> No. The main analysis works without AI. AI explanation is optional and can be skipped.

---

### Q11. What dependency files are supported?

Answer:

> It supports requirements.txt, requirements-dev.txt, dev-requirements.txt, requirements/*.txt, pyproject.toml, and Pipfile.

---

### Q12. Can it detect real vulnerable package versions?

Answer:

> Currently it checks dependency hygiene, such as unpinned versions and unsafe URLs. A future improvement would be to integrate pip-audit, Safety, or OSV for real vulnerability scanning.

---

### Q13. What makes this project useful?

Answer:

> It combines multiple developer workflow features in one tool: static analysis, security checks, dependency checks, test generation, reports, trends, quality gates, and GitHub Actions automation.

---

## 28. Best Final Demo Script

Use this exact script:

> I will demonstrate CodeLens AI, an automated Python code review tool. First, I will show the config file where the default project, reports, rules, ignore patterns, and quality gate are defined. Then I will run the tool on a calculator sample project. The tool scans the code, detects issues, generates tests, runs pytest, calculates a score, updates history, tracks issue trends, evaluates the quality gate, and generates reports. After that, I will open the HTML dashboard to show the visual report. Then I will show generated tests, issue trends, and quality gate reports. Finally, I will run it on a vulnerable sample project to demonstrate security detection and then show the GitHub Actions workflow that automates this process on push and pull requests.

---

## 29. Future Improvements to Mention

Say:

> Some future improvements are:

```text
Real dependency vulnerability scanning
SARIF output for GitHub code scanning
Inline pull request review comments
More advanced AI-generated tests
Cyclomatic complexity calculation
Duplicate code detection
Multi-language support
Web dashboard
Publishing as a pip package
```

---

## 30. Final Closing Statement

End with:

> CodeLens AI started as a code scanner, but it has grown into a complete automated code review pipeline. It can analyze code quality, security, dependencies, tests, trends, reports, pull requests, and CI quality gates. This makes it useful both as a learning project and as a foundation for a real developer productivity tool.