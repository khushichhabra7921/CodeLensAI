import argparse
from pathlib import Path

from codelens.scanner import scan_project
from codelens.analyzer import analyze_project
from codelens.security_analyzer import analyze_security_issues
from codelens.test_generator import generate_test_suggestions
from codelens.test_writer import generate_pytest_files
from codelens.test_runner import run_pytest
from codelens.ai_explainer import generate_ai_explanation
from codelens.reporter import generate_markdown_report
from codelens.json_reporter import generate_json_report
from codelens.html_reporter import generate_html_report
from codelens.history_tracker import update_score_history
from codelens.score_calculator import calculate_code_score


def parse_arguments():
    """
    Parses command-line arguments.

    Supported examples:

    python main.py sample_projects/calculator_app
    python main.py analyze sample_projects/calculator_app
    python main.py analyze sample_projects/calculator_app --format all
    python main.py analyze sample_projects/calculator_app --format html
    python main.py analyze sample_projects/calculator_app --skip-ai
    python main.py analyze sample_projects/calculator_app --skip-tests
    python main.py analyze sample_projects/calculator_app --no-history
    """

    parser = argparse.ArgumentParser(
        prog="CodeLens AI",
        description="Analyze Python projects for code quality, security issues, tests, and reports.",
    )

    parser.add_argument(
        "command_or_path",
        nargs="?",
        help="Use 'analyze' or directly provide a project path.",
    )

    parser.add_argument(
        "project_path",
        nargs="?",
        help="Path to the Python project folder.",
    )

    parser.add_argument(
        "--format",
        dest="report_format",
        choices=["all", "markdown", "md", "json", "html"],
        default="all",
        help="Report format to generate. Options: all, markdown, md, json, html. Default: all.",
    )

    parser.add_argument(
        "--skip-ai",
        action="store_true",
        help="Skip AI explanation generation.",
    )

    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip pytest file generation and pytest execution.",
    )

    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Do not update score history files.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory where reports will be saved. Default: reports.",
    )

    args = parser.parse_args()

    if args.command_or_path is None:
        parser.print_help()
        return None

    if args.command_or_path == "analyze":
        if args.project_path is None:
            parser.error("Please provide a project path after 'analyze'.")

        args.resolved_project_path = args.project_path
    else:
        if args.project_path is not None:
            parser.error(
                "Invalid command format. Use: python main.py analyze <project_path>"
            )

        args.resolved_project_path = args.command_or_path

    if args.report_format == "md":
        args.report_format = "markdown"

    return args


def should_generate_report(report_format, target_format):
    """
    Checks whether a report format should be generated.
    """

    return report_format == "all" or report_format == target_format


def create_skipped_test_result():
    """
    Creates a pytest result dictionary when --skip-tests is used.
    """

    return {
        "passed": None,
        "skipped": True,
        "command": "Skipped because --skip-tests was used.",
        "return_code": 0,
        "stdout": "Test generation and pytest execution were skipped.",
        "stderr": "",
    }


def get_test_status_label(test_run_result):
    """
    Returns a readable test status.
    """

    if test_run_result.get("skipped"):
        return "Skipped"

    if test_run_result.get("passed"):
        return "Passed"

    return "Failed"


def print_project_summary(
    results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    code_score,
    ai_skipped,
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
    print(f"Test run status: {get_test_status_label(test_run_result)}")

    if ai_skipped:
        print("AI explanation generated: False (skipped)")
    else:
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

    if test_run_result.get("skipped"):
        print("Test generation and pytest execution were skipped.")
        return

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


def print_generated_reports(report_paths):
    """
    Prints generated report paths.
    """

    print()

    if "markdown" in report_paths:
        print(f"Markdown report generated: {report_paths['markdown']}")

    if "json" in report_paths:
        print(f"JSON report generated: {report_paths['json']}")

    if "html" in report_paths:
        print(f"HTML report generated: {report_paths['html']}")

    if "history_json" in report_paths:
        print(f"Score history JSON generated: {report_paths['history_json']}")

    if "history_markdown" in report_paths:
        print(f"Score history Markdown generated: {report_paths['history_markdown']}")


def print_history_summary(history_summary):
    """
    Prints score history trend summary.
    """

    if not history_summary:
        return

    print()
    print("Score History")
    print("-" * 40)
    print(f"Total runs tracked: {history_summary['total_runs_tracked']}")
    print(f"Trend: {history_summary['trend']}")

    if history_summary["previous_score"] is not None:
        print(f"Previous score: {history_summary['previous_score']}/100")
        print(f"Score change: {history_summary['score_change']}")


def main():
    args = parse_arguments()

    if args is None:
        return

    project_path = Path(args.resolved_project_path)
    output_dir = Path(args.output_dir)

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

    if args.skip_tests:
        generated_test_files = []
        test_run_result = create_skipped_test_result()
    else:
        generated_test_files = generate_pytest_files(results)
        test_run_result = run_pytest("generated_tests")

    if args.skip_ai:
        ai_explanation = "AI explanation skipped because --skip-ai was used."
    else:
        ai_explanation = generate_ai_explanation(
            results,
            all_issues,
            test_suggestions,
        )

    report_paths = {}

    if should_generate_report(args.report_format, "markdown"):
        markdown_report_path = generate_markdown_report(
            results,
            all_issues,
            test_suggestions,
            generated_test_files,
            test_run_result,
            ai_explanation,
            code_score,
            security_issues,
            output_path=output_dir / "codelens_report.md",
        )

        report_paths["markdown"] = markdown_report_path

    if should_generate_report(args.report_format, "json"):
        json_report_path = generate_json_report(
            results,
            code_quality_issues,
            security_issues,
            all_issues,
            test_suggestions,
            generated_test_files,
            test_run_result,
            ai_explanation,
            code_score,
            project_path,
            output_path=output_dir / "codelens_report.json",
        )

        report_paths["json"] = json_report_path

    if should_generate_report(args.report_format, "html"):
        html_report_path = generate_html_report(
            results,
            code_quality_issues,
            security_issues,
            all_issues,
            test_suggestions,
            generated_test_files,
            test_run_result,
            ai_explanation,
            code_score,
            project_path,
            output_path=output_dir / "codelens_report.html",
        )

        report_paths["html"] = html_report_path

    history_summary = None

    if not args.no_history:
        history_summary = update_score_history(
            project_path,
            results,
            code_quality_issues,
            security_issues,
            all_issues,
            test_suggestions,
            generated_test_files,
            test_run_result,
            code_score,
            args.skip_ai,
            report_paths,
            output_dir=output_dir,
        )

        report_paths["history_json"] = history_summary["history_json_path"]
        report_paths["history_markdown"] = history_summary["history_markdown_path"]

    print_project_summary(
        results,
        code_quality_issues,
        security_issues,
        all_issues,
        test_suggestions,
        generated_test_files,
        test_run_result,
        code_score,
        args.skip_ai,
    )

    print_detailed_file_analysis(results)

    print_issues("Code Quality Issues", code_quality_issues)

    print_issues("Security Issues", security_issues)

    print_ai_explanation(ai_explanation)

    print_generated_tests(generated_test_files, test_run_result)

    print_history_summary(history_summary)

    print_generated_reports(report_paths)


if __name__ == "__main__":
    main()