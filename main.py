import sys
from pathlib import Path

from codelens.scanner import scan_project
from codelens.analyzer import analyze_project
from codelens.security_analyzer import analyze_security_issues
from codelens.test_generator import generate_test_suggestions
from codelens.test_writer import generate_pytest_files
from codelens.test_runner import run_pytest
from codelens.ai_explainer import generate_ai_explanation
from codelens.reporter import generate_markdown_report
from codelens.score_calculator import calculate_code_score


def get_project_path():
    """
    Supports both commands:

    python main.py sample_projects/calculator_app
    python main.py analyze sample_projects/calculator_app
    """

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <project_path>")
        print("  python main.py analyze <project_path>")
        return None

    if sys.argv[1] == "analyze":
        if len(sys.argv) < 3:
            print("Usage: python main.py analyze <project_path>")
            return None

        return sys.argv[2]

    return sys.argv[1]


def print_project_summary(
    results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    code_score,
):
    """
    Prints a short summary of the analysis result.
    """

    print()
    print("CodeLens AI Report")
    print("=" * 40)

    total_files = len(results)
    total_imports = sum(len(file_result["imports"]) for file_result in results)
    total_functions = sum(len(file_result["functions"]) for file_result in results)
    total_classes = sum(len(file_result["classes"]) for file_result in results)

    print(f"Files scanned: {total_files}")
    print(f"Imports found: {total_imports}")
    print(f"Functions found: {total_functions}")
    print(f"Classes found: {total_classes}")
    print(f"Total issues found: {len(all_issues)}")
    print(f"Code quality issues found: {len(code_quality_issues)}")
    print(f"Security issues found: {len(security_issues)}")
    print(f"Test suggestions generated: {len(test_suggestions)}")
    print(f"Pytest files generated: {len(generated_test_files)}")
    print(f"Generated tests passed: {test_run_result['passed']}")
    print("AI explanation generated: True")

    print()
    print("Code Quality and Security Score")
    print("-" * 40)
    print(f"Score: {code_score['score']}/100")
    print(f"Grade: {code_score['grade']}")
    print(f"Status: {code_score['status']}")
    print(f"Critical severity issues: {code_score['issue_summary']['Critical']}")
    print(f"High severity issues: {code_score['issue_summary']['High']}")
    print(f"Medium severity issues: {code_score['issue_summary']['Medium']}")
    print(f"Low severity issues: {code_score['issue_summary']['Low']}")


def print_detailed_file_analysis(results):
    """
    Prints detailed information for every scanned Python file.
    """

    print()
    print("Detailed File Analysis")
    print("-" * 40)

    for file_result in results:
        print()
        print(f"File: {file_result['file']}")

        print("Imports:")
        if file_result["imports"]:
            for item in file_result["imports"]:
                print(f" - {item}")
        else:
            print(" None")

        print("Functions:")
        if file_result["functions"]:
            for function in file_result["functions"]:
                name = function["name"]
                arguments = ", ".join(function["arguments"])
                line_number = function["line_number"]
                line_count = function["line_count"]
                argument_count = function["argument_count"]
                has_docstring = "Yes" if function["has_docstring"] else "No"
                has_division = "Yes" if function["has_division"] else "No"

                print(f" - {name}({arguments})")
                print(f"   Line: {line_number}")
                print(f"   Lines of code: {line_count}")
                print(f"   Arguments count: {argument_count}")
                print(f"   Docstring: {has_docstring}")
                print(f"   Uses division: {has_division}")
        else:
            print(" None")

        print("Classes:")
        if file_result["classes"]:
            for class_info in file_result["classes"]:
                name = class_info["name"]
                line_number = class_info["line_number"]
                has_docstring = "Yes" if class_info["has_docstring"] else "No"

                print(f" - {name}")
                print(f"   Line: {line_number}")
                print(f"   Docstring: {has_docstring}")
        else:
            print(" None")


def print_issues(title, issues):
    """
    Prints issues in terminal.
    """

    print()
    print(title)
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


def print_ai_explanation(ai_explanation):
    """
    Prints AI generated explanation or fallback explanation.
    """

    print()
    print("AI Codebase Explanation")
    print("-" * 40)
    print(ai_explanation)


def print_generated_tests(generated_test_files, test_run_result):
    """
    Prints generated pytest files and pytest result.
    """

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


def main():
    project_path = get_project_path()

    if project_path is None:
        return

    project_path = Path(project_path)

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return

    if not project_path.is_dir():
        print(f"Error: Project path is not a folder: {project_path}")
        return

    results = scan_project(project_path)

    if not results:
        print("No Python files found in the given project path.")
        return

    code_quality_issues = analyze_project(results)

    security_issues = analyze_security_issues(results)

    all_issues = code_quality_issues + security_issues

    code_score = calculate_code_score(results, all_issues)

    test_suggestions = generate_test_suggestions(results)

    generated_test_files = generate_pytest_files(results)

    test_run_result = run_pytest("generated_tests")

    ai_explanation = generate_ai_explanation(
        results,
        all_issues,
        test_suggestions,
    )

    report_path = generate_markdown_report(
        results,
        all_issues,
        test_suggestions,
        generated_test_files,
        test_run_result,
        ai_explanation,
        code_score,
        security_issues,
    )

    print_project_summary(
        results,
        code_quality_issues,
        security_issues,
        all_issues,
        test_suggestions,
        generated_test_files,
        test_run_result,
        code_score,
    )

    print_detailed_file_analysis(results)

    print_issues("Code Quality Issues", code_quality_issues)

    print_issues("Security Issues", security_issues)

    print_ai_explanation(ai_explanation)

    print_generated_tests(generated_test_files, test_run_result)

    print()
    print(f"Markdown report generated: {report_path}")


if __name__ == "__main__":
    main()