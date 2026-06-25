from pathlib import Path


def generate_markdown_report(
    scan_results,
    issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    output_path="reports/codelens_report.md"
):
    """
    Generates a Markdown report from scanner, analyzer, test suggestion,
    generated test files, and pytest run results.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(scan_results)
    total_imports = sum(len(file["imports"]) for file in scan_results)
    total_functions = sum(len(file["functions"]) for file in scan_results)
    total_classes = sum(len(file["classes"]) for file in scan_results)

    lines = []

    lines.append("# CodeLens AI Report")
    lines.append("")
    lines.append("## Project Summary")
    lines.append("")
    lines.append(f"- Files scanned: {total_files}")
    lines.append(f"- Imports found: {total_imports}")
    lines.append(f"- Functions found: {total_functions}")
    lines.append(f"- Classes found: {total_classes}")
    lines.append(f"- Issues found: {len(issues)}")
    lines.append(f"- Test suggestions generated: {len(test_suggestions)}")
    lines.append(f"- Pytest files generated: {len(generated_test_files)}")
    lines.append(f"- Test run passed: {test_run_result['passed']}")
    lines.append("")

    lines.append("## Detailed File Analysis")
    lines.append("")

    for file_result in scan_results:
        lines.append(f"### File: `{file_result['file']}`")
        lines.append("")

        lines.append("#### Imports")
        if file_result["imports"]:
            for item in file_result["imports"]:
                lines.append(f"- `{item}`")
        else:
            lines.append("- None")

        lines.append("")
        lines.append("#### Functions")

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

    lines.append("## Code Quality Issues")
    lines.append("")

    if issues:
        for issue in issues:
            lines.append(f"### {issue['type']}")
            lines.append("")
            lines.append(f"- Severity: **{issue['severity']}**")
            lines.append(f"- File: `{issue['file']}`")
            lines.append(f"- Line: {issue['line']}")
            lines.append(f"- Message: {issue['message']}")
            lines.append(f"- Suggestion: {issue['suggestion']}")
            lines.append("")
    else:
        lines.append("No issues found.")
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