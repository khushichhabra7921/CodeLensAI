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


def load_issue_trends(history_path):
    """
    Loads issue trend history from JSON file.
    """

    history_path = Path(history_path)

    if not history_path.exists():
        return {
            "tool": "CodeLens AI",
            "history_type": "issue_trends",
            "runs": [],
        }

    try:
        with open(history_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "runs" not in data or not isinstance(data["runs"], list):
            data["runs"] = []

        return data

    except json.JSONDecodeError:
        return {
            "tool": "CodeLens AI",
            "history_type": "issue_trends",
            "runs": [],
        }


def save_issue_trends(history_path, history_data):
    """
    Saves issue trend history to JSON file.
    """

    history_path = Path(history_path)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    history_data = make_json_safe(history_data)

    with open(history_path, "w", encoding="utf-8") as file:
        json.dump(history_data, file, indent=4)


def build_issue_key(issue):
    """
    Builds a stable issue key for comparing issues between runs.

    The key uses category, type, file, line, and message.
    """

    category = str(issue.get("category", "Unknown"))
    issue_type = str(issue.get("type", "Unknown"))
    file_path = str(issue.get("file", ""))
    line = str(issue.get("line", ""))
    message = str(issue.get("message", ""))

    return f"{category}|{issue_type}|{file_path}|{line}|{message}"


def simplify_issue(issue):
    """
    Keeps only important issue fields for trend reports.
    """

    return {
        "key": build_issue_key(issue),
        "type": issue.get("type", "Unknown"),
        "category": issue.get("category", "Unknown"),
        "severity": issue.get("severity", "Low"),
        "file": issue.get("file", ""),
        "line": issue.get("line", ""),
        "message": issue.get("message", ""),
        "suggestion": issue.get("suggestion", ""),
    }


def build_issue_map(issues):
    """
    Converts issue list into a dictionary keyed by stable issue key.
    """

    issue_map = {}

    for issue in issues:
        simplified_issue = simplify_issue(issue)
        issue_map[simplified_issue["key"]] = simplified_issue

    return issue_map


def find_previous_run_for_project(history_data, project_path):
    """
    Finds the most recent previous issue trend run for the same project.
    """

    project_path = str(project_path)

    for run in reversed(history_data.get("runs", [])):
        if run.get("project_path") == project_path:
            return run

    return None


def count_by_field(issues, field_name):
    """
    Counts issues by a specific field such as category, severity, or type.
    """

    counts = {}

    for issue in issues:
        value = issue.get(field_name, "Unknown")
        counts[value] = counts.get(value, 0) + 1

    return counts


def calculate_issue_trend(previous_issues, current_issues):
    """
    Compares previous issues and current issues.

    Returns added, resolved, and unchanged issue lists.
    """

    previous_map = build_issue_map(previous_issues)
    current_map = build_issue_map(current_issues)

    previous_keys = set(previous_map.keys())
    current_keys = set(current_map.keys())

    added_keys = sorted(current_keys - previous_keys)
    resolved_keys = sorted(previous_keys - current_keys)
    unchanged_keys = sorted(current_keys & previous_keys)

    added_issues = [
        current_map[key]
        for key in added_keys
    ]

    resolved_issues = [
        previous_map[key]
        for key in resolved_keys
    ]

    unchanged_issues = [
        current_map[key]
        for key in unchanged_keys
    ]

    return {
        "added_issues": added_issues,
        "resolved_issues": resolved_issues,
        "unchanged_issues": unchanged_issues,
        "added_count": len(added_issues),
        "resolved_count": len(resolved_issues),
        "unchanged_count": len(unchanged_issues),
        "previous_total": len(previous_issues),
        "current_total": len(current_issues),
        "issue_count_change": len(current_issues) - len(previous_issues),
    }


def get_trend_label(issue_count_change, added_count, resolved_count):
    """
    Creates a readable trend label.
    """

    if issue_count_change < 0:
        return "Improved"

    if issue_count_change > 0:
        return "Declined"

    if added_count == 0 and resolved_count == 0:
        return "Unchanged"

    return "Mixed"


def build_issue_trend_entry(project_path, all_issues, previous_run):
    """
    Builds one issue trend run entry.
    """

    current_issues = [
        simplify_issue(issue)
        for issue in all_issues
    ]

    if previous_run:
        previous_issues = previous_run.get("current_issues", [])
        comparison = calculate_issue_trend(previous_issues, current_issues)
        trend = get_trend_label(
            comparison["issue_count_change"],
            comparison["added_count"],
            comparison["resolved_count"],
        )
    else:
        comparison = {
            "added_issues": current_issues,
            "resolved_issues": [],
            "unchanged_issues": [],
            "added_count": len(current_issues),
            "resolved_count": 0,
            "unchanged_count": 0,
            "previous_total": None,
            "current_total": len(current_issues),
            "issue_count_change": None,
        }
        trend = "First run for this project"

    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project_path": str(project_path),
        "trend": trend,
        "previous_total_issues": comparison["previous_total"],
        "current_total_issues": comparison["current_total"],
        "issue_count_change": comparison["issue_count_change"],
        "added_count": comparison["added_count"],
        "resolved_count": comparison["resolved_count"],
        "unchanged_count": comparison["unchanged_count"],
        "category_breakdown": count_by_field(current_issues, "category"),
        "severity_breakdown": count_by_field(current_issues, "severity"),
        "type_breakdown": count_by_field(current_issues, "type"),
        "added_issues": comparison["added_issues"],
        "resolved_issues": comparison["resolved_issues"],
        "unchanged_issues": comparison["unchanged_issues"],
        "current_issues": current_issues,
    }

    return entry


def escape_markdown_table_value(value):
    """
    Escapes values for Markdown tables.
    """

    text = str(value)
    text = text.replace("|", "\\|")
    text = text.replace("\n", " ")
    return text


def build_issue_table_rows(issues, max_items=20):
    """
    Builds Markdown table rows for issue lists.
    """

    if not issues:
        return ["No issues."]

    lines = []
    lines.append("| Category | Severity | Type | File | Line |")
    lines.append("|---|---|---|---|---|")

    for issue in issues[:max_items]:
        category = escape_markdown_table_value(issue.get("category", "Unknown"))
        severity = escape_markdown_table_value(issue.get("severity", "Low"))
        issue_type = escape_markdown_table_value(issue.get("type", "Unknown"))
        file_path = escape_markdown_table_value(issue.get("file", ""))
        line = escape_markdown_table_value(issue.get("line", ""))

        lines.append(
            f"| {category} | {severity} | {issue_type} | `{file_path}` | {line} |"
        )

    if len(issues) > max_items:
        lines.append("")
        lines.append(f"Showing first {max_items} of {len(issues)} issues.")

    return lines


def generate_issue_trend_markdown(history_data, latest_entry, output_path):
    """
    Generates a Markdown issue trend report.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# CodeLens AI Issue Trend Report")
    lines.append("")

    lines.append("## Latest Run")
    lines.append("")
    lines.append(f"- Project: `{latest_entry['project_path']}`")
    lines.append(f"- Timestamp UTC: `{latest_entry['timestamp_utc']}`")
    lines.append(f"- Trend: **{latest_entry['trend']}**")
    lines.append(f"- Previous total issues: {latest_entry['previous_total_issues']}")
    lines.append(f"- Current total issues: {latest_entry['current_total_issues']}")
    lines.append(f"- Issue count change: {latest_entry['issue_count_change']}")
    lines.append(f"- Added issues: {latest_entry['added_count']}")
    lines.append(f"- Resolved issues: {latest_entry['resolved_count']}")
    lines.append(f"- Unchanged issues: {latest_entry['unchanged_count']}")
    lines.append("")

    lines.append("## Category Breakdown")
    lines.append("")
    if latest_entry["category_breakdown"]:
        lines.append("| Category | Count |")
        lines.append("|---|---|")
        for category, count in latest_entry["category_breakdown"].items():
            lines.append(f"| {escape_markdown_table_value(category)} | {count} |")
    else:
        lines.append("No category data.")
    lines.append("")

    lines.append("## Severity Breakdown")
    lines.append("")
    if latest_entry["severity_breakdown"]:
        lines.append("| Severity | Count |")
        lines.append("|---|---|")
        for severity, count in latest_entry["severity_breakdown"].items():
            lines.append(f"| {escape_markdown_table_value(severity)} | {count} |")
    else:
        lines.append("No severity data.")
    lines.append("")

    lines.append("## Added Issues")
    lines.append("")
    lines.extend(build_issue_table_rows(latest_entry["added_issues"]))
    lines.append("")

    lines.append("## Resolved Issues")
    lines.append("")
    lines.extend(build_issue_table_rows(latest_entry["resolved_issues"]))
    lines.append("")

    lines.append("## Unchanged Issues")
    lines.append("")
    lines.extend(build_issue_table_rows(latest_entry["unchanged_issues"]))
    lines.append("")

    lines.append("## Recent Runs")
    lines.append("")
    lines.append("| Timestamp UTC | Project | Trend | Previous Issues | Current Issues | Change | Added | Resolved |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|")

    recent_runs = history_data.get("runs", [])[-10:]

    for run in reversed(recent_runs):
        timestamp = escape_markdown_table_value(run.get("timestamp_utc", ""))
        project = escape_markdown_table_value(run.get("project_path", ""))
        trend = escape_markdown_table_value(run.get("trend", ""))
        previous_total = run.get("previous_total_issues")
        current_total = run.get("current_total_issues")
        change = run.get("issue_count_change")
        added = run.get("added_count")
        resolved = run.get("resolved_count")

        lines.append(
            f"| `{timestamp}` | `{project}` | {trend} | {previous_total} | {current_total} | {change} | {added} | {resolved} |"
        )

    report_content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report_content)

    return str(output_path)


def update_issue_trends(
    project_path,
    all_issues,
    output_dir="reports",
):
    """
    Updates issue trend history and generates JSON + Markdown reports.
    """

    output_dir = Path(output_dir)

    history_json_path = output_dir / "issue_trends.json"
    history_markdown_path = output_dir / "issue_trends.md"

    history_data = load_issue_trends(history_json_path)

    previous_run = find_previous_run_for_project(
        history_data,
        project_path,
    )

    latest_entry = build_issue_trend_entry(
        project_path,
        all_issues,
        previous_run,
    )

    history_data["runs"].append(latest_entry)

    save_issue_trends(history_json_path, history_data)

    generate_issue_trend_markdown(
        history_data,
        latest_entry,
        history_markdown_path,
    )

    return {
        "history_json_path": str(history_json_path),
        "history_markdown_path": str(history_markdown_path),
        "total_runs_tracked": len(history_data["runs"]),
        "trend": latest_entry["trend"],
        "previous_total_issues": latest_entry["previous_total_issues"],
        "current_total_issues": latest_entry["current_total_issues"],
        "issue_count_change": latest_entry["issue_count_change"],
        "added_count": latest_entry["added_count"],
        "resolved_count": latest_entry["resolved_count"],
        "unchanged_count": latest_entry["unchanged_count"],
    }