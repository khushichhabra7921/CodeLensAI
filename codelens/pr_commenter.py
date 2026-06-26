from pathlib import Path


COMMENT_MARKER = "<!-- codelens-ai-pr-comment -->"


def get_test_status_label(test_run_result):
    """
    Returns a readable test status.
    """

    if test_run_result.get("skipped"):
        return "Skipped"

    if test_run_result.get("passed"):
        return "Passed"

    return "Failed"


def get_trend_line(history_summary):
    """
    Builds score trend line for PR comment.
    """

    if not history_summary:
        return "- Score trend: Not available"

    trend = history_summary.get("trend", "Unknown")
    previous_score = history_summary.get("previous_score")
    score_change = history_summary.get("score_change")

    if previous_score is None:
        return f"- Score trend: {trend}"

    return f"- Score trend: {trend} from previous score {previous_score}/100, change {score_change}"


def get_issue_trend_line(issue_trend_summary):
    """
    Builds issue trend line for PR comment.
    """

    if not issue_trend_summary:
        return "- Issue trend: Not available"

    trend = issue_trend_summary.get("trend", "Unknown")
    added_count = issue_trend_summary.get("added_count", 0)
    resolved_count = issue_trend_summary.get("resolved_count", 0)
    unchanged_count = issue_trend_summary.get("unchanged_count", 0)

    return (
        f"- Issue trend: {trend} "
        f"({added_count} added, {resolved_count} resolved, {unchanged_count} unchanged)"
    )


def build_top_issues_section(title, issues, max_items=5):
    """
    Builds a compact section for top issues.
    """

    lines = []

    lines.append(f"### {title}")
    lines.append("")

    if not issues:
        lines.append("No issues found.")
        lines.append("")
        return lines

    for issue in issues[:max_items]:
        issue_type = issue.get("type", "Issue")
        severity = issue.get("severity", "Low")
        file_path = issue.get("file", "")
        line = issue.get("line", "")
        message = issue.get("message", "")

        lines.append(
            f"- **{severity}** `{issue_type}` in `{file_path}` line `{line}`"
        )
        lines.append(f"  - {message}")

    if len(issues) > max_items:
        lines.append("")
        lines.append(f"Showing first {max_items} of {len(issues)} issues.")

    lines.append("")
    return lines


def generate_pr_comment(
    project_path,
    scan_results,
    code_quality_issues,
    security_issues,
    dependency_issues,
    all_issues,
    code_score,
    test_suggestions,
    generated_test_files,
    test_run_result,
    history_summary=None,
    issue_trend_summary=None,
    report_paths=None,
    output_path="reports/pr_comment.md",
):
    """
    Generates a Markdown summary designed for GitHub pull request comments.
    """

    if report_paths is None:
        report_paths = {}

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    lines = []

    lines.append(COMMENT_MARKER)
    lines.append("")
    lines.append("## CodeLens AI Pull Request Summary")
    lines.append("")
    lines.append(f"Project analyzed: `{project_path}`")
    lines.append("")

    lines.append("### Overall Result")
    lines.append("")
    lines.append(f"- Score: **{code_score['score']}/100**")
    lines.append(f"- Grade: **{code_score['grade']}**")
    lines.append(f"- Status: **{code_score['status']}**")
    lines.append(f"- Test status: **{get_test_status_label(test_run_result)}**")
    lines.append(get_trend_line(history_summary))
    lines.append(get_issue_trend_line(issue_trend_summary))
    lines.append("")

    lines.append("### Project Summary")
    lines.append("")
    lines.append(f"- Files scanned: {total_files}")
    lines.append(f"- Imports found: {total_imports}")
    lines.append(f"- Functions found: {total_functions}")
    lines.append(f"- Classes found: {total_classes}")
    lines.append(f"- Test suggestions generated: {len(test_suggestions)}")
    lines.append(f"- Pytest files generated: {len(generated_test_files)}")
    lines.append("")

    lines.append("### Issue Summary")
    lines.append("")
    lines.append(f"- Total issues: **{len(all_issues)}**")
    lines.append(f"- Code quality issues: {len(code_quality_issues)}")
    lines.append(f"- Security issues: {len(security_issues)}")
    lines.append(f"- Dependency issues: {len(dependency_issues)}")
    lines.append(f"- Critical severity issues: {code_score['issue_summary']['Critical']}")
    lines.append(f"- High severity issues: {code_score['issue_summary']['High']}")
    lines.append(f"- Medium severity issues: {code_score['issue_summary']['Medium']}")
    lines.append(f"- Low severity issues: {code_score['issue_summary']['Low']}")
    lines.append("")

    lines.extend(build_top_issues_section("Top Code Quality Issues", code_quality_issues))
    lines.extend(build_top_issues_section("Top Security Issues", security_issues))
    lines.extend(build_top_issues_section("Top Dependency Issues", dependency_issues))

    lines.append("### Generated Reports")
    lines.append("")

    if report_paths:
        for report_name, report_path in report_paths.items():
            lines.append(f"- {report_name}: `{report_path}`")
    else:
        lines.append("Reports were generated as GitHub Actions artifacts.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Generated automatically by CodeLens AI._")

    comment_content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(comment_content)

    return str(output_path)