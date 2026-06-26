from pathlib import Path


def generate_markdown_report(
    scan_results,
    issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    ai_explanation,
    code_score=None,
    security_issues=None,
    output_path="reports/codelens_report.md",
):
    """
    Generates a Markdown report from scanner, analyzer, security analyzer,
    test suggestions, generated test files, pytest result, AI explanation,
    and code quality score.
    """

    if security_issues is None:
        security_issues = []

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    code_quality_issues = [
        issue for issue in issues if issue.get("category") != "Security"
    ]

    lines = []

    lines.append("# CodeLens AI Report")
    lines.append("")

    lines.append("## Project Summary")
    lines.append("")
    lines.append(f"- Files scanned: {total_files}")
    lines.append(f"- Imports found: {total_imports}")
    lines.append(f"- Functions found: {total_functions}")
    lines.append(f"- Classes found: {total_classes}")
    lines.append(f"- Total issues found: {len(issues)}")
    lines.append(f"- Code quality issues found: {len(code_quality_issues)}")
    lines.append(f"- Security issues found: {len(security_issues)}")
    lines.append(f"- Test suggestions generated: {len(test_suggestions)}")
    lines.append(f"- Pytest files generated: {len(generated_test_files)}")
    lines.append(f"- Test run passed: {test_run_result['passed']}")
    lines.append("")

    if code_score:
        lines.append("## Code Quality and Security Score")
        lines.append("")
        lines.append(f"- Score: **{code_score['score']}/100**")
        lines.append(f"- Grade: **{code_score['grade']}**")
        lines.append(f"- Status: **{code_score['status']}**")
        lines.append(f"- Total issues: {code_score['total_issues']}")
        lines.append(f"- Critical severity issues: {code_score['issue_summary']['Critical']}")
        lines.append(f"- High severity issues: {code_score['issue_summary']['High']}")
        lines.append(f"- Medium severity issues: {code_score['issue_summary']['Medium']}")
        lines.append(f"- Low severity issues: {code_score['issue_summary']['Low']}")
        lines.append("")

    lines.append("## Detailed File Analysis")
    lines.append("")

    for file_result in scan_results:
        lines.append(f"### File: `{file_result['file']}`")
        lines.append("")

        lines.append("#### Imports")
        lines.append("")

        if file_result["imports"]:
            for item in file_result["imports"]:
                lines.append(f"- `{item}`")
        else:
            lines.append("- None")

        lines.append("")

        lines.append("#### Functions")
        lines.append("")

        if file_result["functions"]:
            for function in file_result["functions"]:
                name = function["name"]
                arguments = ", ".join(function["arguments"])
                line_number = function["line_number"]
                line_count = function["line_count"]
                argument_count = function["argument_count"]
                has_docstring = "Yes" if function["has_docstring"] else "No"
                has_division = "Yes" if function["has_division"] else "No"

                lines.append(f"- `{name}({arguments})`")
                lines.append(f"  - Line: {line_number}")
                lines.append(f"  - Lines of code: {line_count}")
                lines.append(f"  - Arguments count: {argument_count}")
                lines.append(f"  - Docstring: {has_docstring}")
                lines.append(f"  - Uses division: {has_division}")
        else:
            lines.append("- None")

        lines.append("")

        lines.append("#### Classes")
        lines.append("")

        if file_result["classes"]:
            for class_info in file_result["classes"]:
                name = class_info["name"]
                line_number = class_info["line_number"]
                has_docstring = "Yes" if class_info["has_docstring"] else "No"

                lines.append(f"- `{name}`")
                lines.append(f"  - Line: {line_number}")
                lines.append(f"  - Docstring: {has_docstring}")
        else:
            lines.append("- None")

        lines.append("")

    lines.append("## AI Codebase Explanation")
    lines.append("")

    if ai_explanation:
        lines.append(ai_explanation)
    else:
        lines.append("No AI explanation generated.")

    lines.append("")

    lines.append("## Code Quality Issues")
    lines.append("")

    if code_quality_issues:
        for issue in code_quality_issues:
            lines.append(f"### {issue['type']}")
            lines.append("")
            lines.append(f"- Severity: **{issue['severity']}**")
            lines.append(f"- File: `{issue['file']}`")
            lines.append(f"- Line: {issue['line']}")
            lines.append(f"- Message: {issue['message']}")
            lines.append(f"- Suggestion: {issue['suggestion']}")
            lines.append("")
    else:
        lines.append("No code quality issues found.")
        lines.append("")

    lines.append("## Security Issues")
    lines.append("")

    if security_issues:
        for issue in security_issues:
            lines.append(f"### {issue['type']}")
            lines.append("")
            lines.append(f"- Severity: **{issue['severity']}**")
            lines.append(f"- File: `{issue['file']}`")
            lines.append(f"- Line: {issue['line']}")
            lines.append(f"- Message: {issue['message']}")
            lines.append(f"- Suggestion: {issue['suggestion']}")
            lines.append("")
    else:
        lines.append("No security issues found.")
        lines.append("")

    lines.append("## Test Suggestions")
    lines.append("")

    if test_suggestions:
        for suggestion in test_suggestions:
            function_name = suggestion["function"]
            arguments = ", ".join(suggestion["arguments"])

            lines.append(f"### `{function_name}({arguments})`")
            lines.append("")
            lines.append(f"- File: `{suggestion['file']}`")
            lines.append("- Suggested pytest tests:")

            for test in suggestion["suggested_tests"]:
                lines.append(f"  - `{test}`")

            lines.append("")
    else:
        lines.append("No test suggestions generated.")
        lines.append("")

    lines.append("## Generated Pytest Files")
    lines.append("")

    if generated_test_files:
        for file_path in generated_test_files:
            lines.append(f"- `{file_path}`")
    else:
        lines.append("No pytest files generated.")

    lines.append("")

    lines.append("## Pytest Run Result")
    lines.append("")

    if test_run_result["passed"]:
        lines.append("✅ **All generated tests passed.**")
    else:
        lines.append("❌ **Some generated tests failed.**")

    lines.append("")
    lines.append(f"- Command: `{test_run_result['command']}`")
    lines.append(f"- Return code: `{test_run_result['return_code']}`")
    lines.append("")

    lines.append("### Pytest Output")
    lines.append("")
    lines.append("```text")
    lines.append(test_run_result["stdout"])
    lines.append("```")
    lines.append("")

    if test_run_result["stderr"]:
        lines.append("### Pytest Errors")
        lines.append("")
        lines.append("```text")
        lines.append(test_run_result["stderr"])
        lines.append("```")
        lines.append("")

    report_content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report_content)

    return str(output_path)