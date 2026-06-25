import sys
from codelens.scanner import scan_project
from codelens.analyzer import analyze_project
from codelens.test_generator import generate_test_suggestions
from codelens.test_writer import generate_pytest_files
from codelens.test_runner import run_pytest
from codelens.reporter import generate_markdown_report


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <project_path>")
        return

    project_path = sys.argv[1]

    results = scan_project(project_path)
    issues = analyze_project(results)
    test_suggestions = generate_test_suggestions(results)
    generated_test_files = generate_pytest_files(results)
    test_run_result = run_pytest("generated_tests")

    report_path = generate_markdown_report(
        results,
        issues,
        test_suggestions,
        generated_test_files,
        test_run_result
    )

    print()
    print("CodeLens AI Report")
    print("=" * 40)

    total_files = len(results)
    total_imports = sum(len(file["imports"]) for file in results)
    total_functions = sum(len(file["functions"]) for file in results)
    total_classes = sum(len(file["classes"]) for file in results)

    print(f"Files scanned: {total_files}")
    print(f"Imports found: {total_imports}")
    print(f"Functions found: {total_functions}")
    print(f"Classes found: {total_classes}")
    print(f"Issues found: {len(issues)}")
    print(f"Test suggestions generated: {len(test_suggestions)}")
    print(f"Pytest files generated: {len(generated_test_files)}")
    print(f"Generated tests passed: {test_run_result['passed']}")

    print()
    print("Detailed File Analysis")
    print("-" * 40)

    for file in results:
        print()
        print(f"File: {file['file']}")

        print("Imports:")
        if file["imports"]:
            for item in file["imports"]:
                print(f"  - {item}")
        else:
            print("  None")

        print("Functions:")
        if file["functions"]:
            for function in file["functions"]:
                name = function["name"]
                arguments = ", ".join(function["arguments"])
                line_number = function["line_number"]
                line_count = function["line_count"]
                argument_count = function["argument_count"]
                has_docstring = "Yes" if function["has_docstring"] else "No"
                has_division = "Yes" if function["has_division"] else "No"

                print(f"  - {name}({arguments})")
                print(f"    Line: {line_number}")
                print(f"    Lines of code: {line_count}")
                print(f"    Arguments count: {argument_count}")
                print(f"    Docstring: {has_docstring}")
                print(f"    Uses division: {has_division}")
        else:
            print("  None")

        print("Classes:")
        if file["classes"]:
            for class_info in file["classes"]:
                name = class_info["name"]
                line_number = class_info["line_number"]
                has_docstring = "Yes" if class_info["has_docstring"] else "No"

                print(f"  - {name}")
                print(f"    Line: {line_number}")
                print(f"    Docstring: {has_docstring}")
        else:
            print("  None")

    print()
    print("Code Quality Issues")
    print("-" * 40)

    if issues:
        for issue in issues:
            print(f"[{issue['type']}]")
            print(f"Severity: {issue['severity']}")
            print(f"File: {issue['file']}")
            print(f"Line: {issue['line']}")
            print(f"Message: {issue['message']}")
            print(f"Suggestion: {issue['suggestion']}")
            print()
    else:
        print("No issues found.")

    print()
    print("Test Suggestions")
    print("-" * 40)

    if test_suggestions:
        for suggestion in test_suggestions:
            function_name = suggestion["function"]
            arguments = ", ".join(suggestion["arguments"])

            print(f"Function: {function_name}({arguments})")
            print("Suggested tests:")

            for test in suggestion["suggested_tests"]:
                print(f"  - {test}")

            print()
    else:
        print("No test suggestions generated.")

    print()
    print("Generated Pytest Files")
    print("-" * 40)

    if generated_test_files:
        for file_path in generated_test_files:
            print(f"- {file_path}")
    else:
        print("No pytest files generated.")

    print()
    print("Pytest Run Result")
    print("-" * 40)

    if test_run_result["passed"]:
        print("All generated tests passed.")
    else:
        print("Some generated tests failed.")

    print(f"Command: {test_run_result['command']}")
    print(f"Return code: {test_run_result['return_code']}")

    print()
    print(f"Markdown report generated: {report_path}")


if __name__ == "__main__":
    main()