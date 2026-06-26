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


def get_issue_summary(code_score):
    """
    Safely gets issue severity summary from code score.
    """

    issue_summary = code_score.get("issue_summary", {})

    return {
        "Critical": issue_summary.get("Critical", 0),
        "High": issue_summary.get("High", 0),
        "Medium": issue_summary.get("Medium", 0),
        "Low": issue_summary.get("Low", 0),
    }


def add_failure(failures, rule, message):
    """
    Adds one quality gate failure.
    """

    failures.append(
        {
            "rule": rule,
            "message": message,
        }
    )


def check_optional_maximum(
    failures,
    rule_name,
    label,
    actual_value,
    max_allowed,
):
    """
    Checks optional max rules.

    If max_allowed is None, the rule is ignored.
    """

    if max_allowed is None:
        return

    if actual_value > max_allowed:
        add_failure(
            failures,
            rule_name,
            f"{label} is {actual_value}, which is above the allowed maximum of {max_allowed}.",
        )


def evaluate_quality_gate(
    code_score,
    all_issues,
    test_run_result,
    quality_gate_config=None,
):
    """
    Evaluates quality gate rules.

    Supported config:

    quality_gate:
      enabled: true
      min_score: 0
      max_total_issues: null
      max_critical_issues: 0
      max_high_issues: 10
      max_medium_issues: null
      max_low_issues: null
      fail_on_tests_failed: true
    """

    if quality_gate_config is None:
        quality_gate_config = {}

    enabled = bool(quality_gate_config.get("enabled", True))

    issue_summary = get_issue_summary(code_score)

    result = {
        "enabled": enabled,
        "passed": True,
        "status": "PASSED",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": code_score.get("score", 0),
        "grade": code_score.get("grade", "F"),
        "score_status": code_score.get("status", "Unknown"),
        "total_issues": len(all_issues),
        "issue_summary": issue_summary,
        "test_status": get_test_status_label(test_run_result),
        "config": quality_gate_config,
        "failures": [],
    }

    if not enabled:
        result["passed"] = True
        result["status"] = "DISABLED"
        return result

    failures = []

    min_score = quality_gate_config.get("min_score", 0)
    max_total_issues = quality_gate_config.get("max_total_issues")
    max_critical_issues = quality_gate_config.get("max_critical_issues", 0)
    max_high_issues = quality_gate_config.get("max_high_issues", 10)
    max_medium_issues = quality_gate_config.get("max_medium_issues")
    max_low_issues = quality_gate_config.get("max_low_issues")
    fail_on_tests_failed = bool(
        quality_gate_config.get("fail_on_tests_failed", True)
    )

    score = code_score.get("score", 0)

    if score < min_score:
        add_failure(
            failures,
            "min_score",
            f"Score is {score}/100, which is below the required minimum of {min_score}/100.",
        )

    check_optional_maximum(
        failures,
        "max_total_issues",
        "Total issues",
        len(all_issues),
        max_total_issues,
    )

    check_optional_maximum(
        failures,
        "max_critical_issues",
        "Critical issues",
        issue_summary["Critical"],
        max_critical_issues,
    )

    check_optional_maximum(
        failures,
        "max_high_issues",
        "High issues",
        issue_summary["High"],
        max_high_issues,
    )

    check_optional_maximum(
        failures,
        "max_medium_issues",
        "Medium issues",
        issue_summary["Medium"],
        max_medium_issues,
    )

    check_optional_maximum(
        failures,
        "max_low_issues",
        "Low issues",
        issue_summary["Low"],
        max_low_issues,
    )

    if fail_on_tests_failed:
        if not test_run_result.get("skipped") and not test_run_result.get("passed"):
            add_failure(
                failures,
                "fail_on_tests_failed",
                "Generated pytest tests failed.",
            )

    if failures:
        result["passed"] = False
        result["status"] = "FAILED"
        result["failures"] = failures

    return result


def generate_quality_gate_json(quality_gate_result, output_path):
    """
    Generates quality_gate.json.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    safe_result = make_json_safe(quality_gate_result)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(safe_result, file, indent=4)

    return str(output_path)


def generate_quality_gate_markdown(quality_gate_result, output_path):
    """
    Generates quality_gate.md.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# CodeLens AI Quality Gate Report")
    lines.append("")

    lines.append("## Result")
    lines.append("")
    lines.append(f"- Enabled: `{quality_gate_result['enabled']}`")
    lines.append(f"- Status: **{quality_gate_result['status']}**")
    lines.append(f"- Passed: `{quality_gate_result['passed']}`")
    lines.append(f"- Generated at UTC: `{quality_gate_result['generated_at_utc']}`")
    lines.append("")

    lines.append("## Score")
    lines.append("")
    lines.append(f"- Score: **{quality_gate_result['score']}/100**")
    lines.append(f"- Grade: **{quality_gate_result['grade']}**")
    lines.append(f"- Score status: **{quality_gate_result['score_status']}**")
    lines.append("")

    lines.append("## Issue Summary")
    lines.append("")
    lines.append(f"- Total issues: {quality_gate_result['total_issues']}")
    lines.append(f"- Critical issues: {quality_gate_result['issue_summary']['Critical']}")
    lines.append(f"- High issues: {quality_gate_result['issue_summary']['High']}")
    lines.append(f"- Medium issues: {quality_gate_result['issue_summary']['Medium']}")
    lines.append(f"- Low issues: {quality_gate_result['issue_summary']['Low']}")
    lines.append("")

    lines.append("## Test Summary")
    lines.append("")
    lines.append(f"- Test status: **{quality_gate_result['test_status']}**")
    lines.append("")

    lines.append("## Failures")
    lines.append("")

    if quality_gate_result["failures"]:
        for failure in quality_gate_result["failures"]:
            lines.append(f"- **{failure['rule']}**: {failure['message']}")
    else:
        lines.append("No quality gate failures.")

    lines.append("")

    lines.append("## Applied Rules")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(make_json_safe(quality_gate_result["config"]), indent=4))
    lines.append("```")
    lines.append("")

    report_content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report_content)

    return str(output_path)


def generate_quality_gate_reports(
    quality_gate_result,
    output_dir="reports",
):
    """
    Generates quality gate JSON and Markdown reports.
    """

    output_dir = Path(output_dir)

    quality_gate_json_path = output_dir / "quality_gate.json"
    quality_gate_markdown_path = output_dir / "quality_gate.md"

    json_path = generate_quality_gate_json(
        quality_gate_result,
        quality_gate_json_path,
    )

    markdown_path = generate_quality_gate_markdown(
        quality_gate_result,
        quality_gate_markdown_path,
    )

    return {
        "quality_gate_json_path": json_path,
        "quality_gate_markdown_path": markdown_path,
    }