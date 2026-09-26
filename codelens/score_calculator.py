def calculate_code_score(scan_results, issues):
    """
    Calculates an overall code quality and security score from 0 to 100.

    Score starts at 100 and decreases based on issue severity.

    Medium and Low penalties are capped, so many minor issues (e.g. missing
    docstrings) lower the score but can't outweigh a single real vulnerability.
    Critical and High penalties are not capped.
    """

    score = 100

    severity_penalties = {
        "Critical": 20,
        "High": 15,
        "Medium": 8,
        "Low": 4,
    }

    severity_penalty_caps = {
        "Medium": 30,
        "Low": 20,
    }

    severity_penalty_totals = {}

    issue_summary = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }

    for issue in issues:
        severity = issue.get("severity", "Low")
        penalty = severity_penalties.get(severity, 4)

        severity_penalty_totals[severity] = severity_penalty_totals.get(severity, 0) + penalty

        if severity in issue_summary:
            issue_summary[severity] += 1

    for severity, total_penalty in severity_penalty_totals.items():
        cap = severity_penalty_caps.get(severity)
        score -= min(total_penalty, cap) if cap is not None else total_penalty

    total_files = len(scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    final_score = max(score, 0)

    if final_score >= 90:
        grade = "A"
        status = "Excellent"
    elif final_score >= 75:
        grade = "B"
        status = "Good"
    elif final_score >= 60:
        grade = "C"
        status = "Needs Improvement"
    elif final_score >= 40:
        grade = "D"
        status = "Poor"
    else:
        grade = "F"
        status = "Critical"

    return {
        "score": final_score,
        "grade": grade,
        "status": status,
        "total_files": total_files,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "total_issues": len(issues),
        "issue_summary": issue_summary,
    }