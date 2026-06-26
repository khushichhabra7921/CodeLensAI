import json
from datetime import datetime, timezone
from pathlib import Path


def make_json_safe(value):
    """
    Converts values into JSON-safe data.
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


def get_test_status_label(test_run_result):
    """
    Returns a readable test status.
    """

    if test_run_result.get("skipped"):
        return "Skipped"

    if test_run_result.get("passed"):
        return "Passed"

    return "Failed"


def load_score_history(history_json_path):
    """
    Loads score history from a JSON file.

    If the file does not exist or is invalid, an empty history is returned.
    """

    history_json_path = Path(history_json_path)

    if not history_json_path.exists():
        return []

    try:
        with open(history_json_path, "r", encoding="utf-8") as file:
            history = json.load(file)

        if isinstance(history, list):
            return history

        return []

    except json.JSONDecodeError:
        return []


def save_score_history(history, history_json_path):
    """
    Saves score history to a JSON file.
    """

    history_json_path = Path(history_json_path)
    history_json_path.parent.mkdir(parents=True, exist_ok=True)

    history = make_json_safe(history)

    with open(history_json_path, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    return str(history_json_path)


def find_previous_run_for_project(history, project_path):
    """
    Finds the most recent previous run for the same project path.
    """

    project_path = str(project_path)

    for entry in reversed(history):
        if entry.get("project_path") == project_path:
            return entry

    return None


def calculate_score_trend(current_score, previous_score):
    """
    Calculates score trend compared with the previous run.
    """

    if previous_score is None:
        return {
            "previous_score": None,
            "score_change": None,
            "trend": "First run for this project",
        }

    score_change = current_score - previous_score

    if score_change > 0:
        trend = "Improved"
    elif score_change < 0:
        trend = "Declined"
    else:
        trend = "Unchanged"

    return {
        "previous_score": previous_score,
        "score_change": score_change,
        "trend": trend,
    }


def build_history_entry(
    project_path,
    scan_results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    code_score,
    ai_skipped,
    report_paths,
    trend_info,
):
    """
    Builds one score history entry.
    """

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_path": str(project_path),
        "score": code_score["score"],
        "grade": code_score["grade"],
        "status": code_score["status"],
        "previous_score": trend_info["previous_score"],
        "score_change": trend_info["score_change"],
        "trend": trend_info["trend"],
        "files_scanned": total_files,
        "imports_found": total_imports,
        "functions_found": total_functions,
        "classes_found": total_classes,
        "total_issues_found": len(all_issues),
        "code_quality_issues_found": len(code_quality_issues),
        "security_issues_found": len(security_issues),
        "critical_issues": code_score["issue_summary"]["Critical"],
        "high_issues": code_score["issue_summary"]["High"],
        "medium_issues": code_score["issue_summary"]["Medium"],
        "low_issues": code_score["issue_summary"]["Low"],
        "test_suggestions_generated": len(test_suggestions),
        "pytest_files_generated": len(generated_test_files),
        "test_status": get_test_status_label(test_run_result),
        "ai_skipped": ai_skipped,
        "tests_skipped": bool(test_run_result.get("skipped")),
        "report_paths": report_paths,
    }


def escape_markdown_table_value(value):
    """
    Escapes values for Markdown table cells.
    """

    if value is None:
        return "-"

    return str(value).replace("|", "\\|")


def generate_score_history_markdown(history, history_markdown_path):
    """
    Generates a readable Markdown score history report.
    """

    history_markdown_path = Path(history_markdown_path)
    history_markdown_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# CodeLens AI Score History")
    lines.append("")

    if not history:
        lines.append("No score history available.")
        lines.append("")

        with open(history_markdown_path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines))

        return str(history_markdown_path)

    latest_run = history[-1]

    lines.append("## Latest Run")
    lines.append("")
    lines.append(f"- Project: `{latest_run['project_path']}`")
    lines.append(f"- Generated at UTC: `{latest_run['generated_at_utc']}`")
    lines.append(f"- Score: **{latest_run['score']}/100**")
    lines.append(f"- Grade: **{latest_run['grade']}**")
    lines.append(f"- Status: **{latest_run['status']}**")
    lines.append(f"- Trend: **{latest_run['trend']}**")

    if latest_run["previous_score"] is not None:
        lines.append(f"- Previous score: {latest_run['previous_score']}/100")
        lines.append(f"- Score change: {latest_run['score_change']}")

    lines.append("")

    lines.append("## Run History")
    lines.append("")
    lines.append(
        "| # | Time UTC | Project | Score | Grade | Trend | Total Issues | Security Issues | Test Status |"
    )
    lines.append(
        "|---|----------|---------|-------|-------|-------|--------------|-----------------|-------------|"
    )

    recent_history = list(reversed(history[-30:]))

    for index, entry in enumerate(recent_history, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_markdown_table_value(index),
                    escape_markdown_table_value(entry.get("generated_at_utc")),
                    escape_markdown_table_value(entry.get("project_path")),
                    escape_markdown_table_value(entry.get("score")),
                    escape_markdown_table_value(entry.get("grade")),
                    escape_markdown_table_value(entry.get("trend")),
                    escape_markdown_table_value(entry.get("total_issues_found")),
                    escape_markdown_table_value(entry.get("security_issues_found")),
                    escape_markdown_table_value(entry.get("test_status")),
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- The score starts at 100 and decreases based on issue severity.")
    lines.append("- This file tracks recent analysis runs.")
    lines.append("- Reports are generated output files and may be ignored by Git.")
    lines.append("")

    with open(history_markdown_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return str(history_markdown_path)


def update_score_history(
    project_path,
    scan_results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    code_score,
    ai_skipped,
    report_paths,
    output_dir="reports",
    max_entries=100,
):
    """
    Updates score history JSON and Markdown files.

    Returns summary information about the updated history.
    """

    output_dir = Path(output_dir)

    history_json_path = output_dir / "score_history.json"
    history_markdown_path = output_dir / "score_history.md"

    history = load_score_history(history_json_path)

    previous_run = find_previous_run_for_project(history, project_path)

    previous_score = None
    if previous_run:
        previous_score = previous_run.get("score")

    trend_info = calculate_score_trend(
        code_score["score"],
        previous_score,
    )

    history_entry = build_history_entry(
        project_path,
        scan_results,
        code_quality_issues,
        security_issues,
        all_issues,
        test_suggestions,
        generated_test_files,
        test_run_result,
        code_score,
        ai_skipped,
        report_paths,
        trend_info,
    )

    history.append(history_entry)

    if len(history) > max_entries:
        history = history[-max_entries:]

    json_path = save_score_history(history, history_json_path)

    markdown_path = generate_score_history_markdown(
        history,
        history_markdown_path,
    )

    return {
        "history_json_path": json_path,
        "history_markdown_path": markdown_path,
        "total_runs_tracked": len(history),
        "latest_entry": history_entry,
        "previous_score": trend_info["previous_score"],
        "score_change": trend_info["score_change"],
        "trend": trend_info["trend"],
    }