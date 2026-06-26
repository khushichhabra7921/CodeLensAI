import json
from datetime import datetime, timezone
from pathlib import Path


def make_json_safe(value):
    """
    Converts values into JSON-safe data.

    This helps avoid errors if any value is a Path, tuple, set,
    or another object that json.dump cannot directly serialize.
    """

    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, tuple):
        return [make_json_safe(item) for item in value]

    if isinstance(value, set):
        return [make_json_safe(item) for item in value]

    if isinstance(value, Path):
        return str(value)

    return value


def build_project_summary(
    scan_results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
):
    """
    Builds a summary dictionary for the JSON report.
    """

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    return {
        "files_scanned": total_files,
        "imports_found": total_imports,
        "functions_found": total_functions,
        "classes_found": total_classes,
        "total_issues_found": len(all_issues),
        "code_quality_issues_found": len(code_quality_issues),
        "security_issues_found": len(security_issues),
        "test_suggestions_generated": len(test_suggestions),
        "pytest_files_generated": len(generated_test_files),
        "test_run_passed": test_run_result["passed"],
    }


def generate_json_report(
    scan_results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    ai_explanation,
    code_score,
    project_path,
    output_path="reports/codelens_report.json",
):
    """
    Generates a structured JSON report.

    The JSON report can later be used for:
    - Web dashboards
    - GitHub Actions artifacts
    - API integrations
    - Charts
    - Score history tracking
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report_data = {
        "tool": {
            "name": "CodeLens AI",
            "report_type": "json",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "project": {
            "path": str(project_path),
        },
        "summary": build_project_summary(
            scan_results,
            code_quality_issues,
            security_issues,
            all_issues,
            test_suggestions,
            generated_test_files,
            test_run_result,
        ),
        "score": code_score,
        "scan_results": scan_results,
        "issues": {
            "all": all_issues,
            "code_quality": code_quality_issues,
            "security": security_issues,
        },
        "tests": {
            "suggestions": test_suggestions,
            "generated_files": generated_test_files,
            "pytest_result": test_run_result,
        },
        "ai_explanation": ai_explanation,
    }

    report_data = make_json_safe(report_data)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4)

    return str(output_path)
