def add_issue(issues, issue_type, severity, file_path, line, message, suggestion):
    """
    Adds a code quality issue.
    """

    issues.append(
        {
            "type": issue_type,
            "category": "Code Quality",
            "severity": severity,
            "file": file_path,
            "line": line,
            "message": message,
            "suggestion": suggestion,
        }
    )


def analyze_project(scan_results, rules_config=None):
    """
    Analyzes scanned Python files for code quality issues.

    Detects:
    - Missing function docstrings
    - Missing class docstrings
    - Possible division-by-zero risks
    - Functions with too many arguments
    - Long functions
    """

    if rules_config is None:
        rules_config = {}

    max_function_lines = rules_config.get("max_function_lines", 30)
    max_arguments = rules_config.get("max_arguments", 5)

    issues = []

    for file_result in scan_results:
        file_path = file_result["file"]

        for function in file_result["functions"]:
            function_name = function["name"]
            line_number = function["line_number"]

            if not function["has_docstring"]:
                add_issue(
                    issues,
                    "Missing Docstring",
                    "Low",
                    file_path,
                    line_number,
                    f"Function '{function_name}' does not have a docstring.",
                    "Add a short docstring explaining what the function does.",
                )

            if function["has_division"]:
                add_issue(
                    issues,
                    "Possible Runtime Error",
                    "High",
                    file_path,
                    line_number,
                    f"Function '{function_name}' uses division. This may crash if the denominator is zero.",
                    "Add a check before division, for example: if b == 0, raise ValueError.",
                )

            if function["argument_count"] > max_arguments:
                add_issue(
                    issues,
                    "Too Many Arguments",
                    "Medium",
                    file_path,
                    line_number,
                    f"Function '{function_name}' has {function['argument_count']} arguments.",
                    f"Try to keep function arguments at or below {max_arguments}. Consider grouping related values into a dictionary, class, or data object.",
                )

            if function["line_count"] > max_function_lines:
                add_issue(
                    issues,
                    "Long Function",
                    "Medium",
                    file_path,
                    line_number,
                    f"Function '{function_name}' has {function['line_count']} lines of code.",
                    f"Try to keep functions at or below {max_function_lines} lines. Split this function into smaller helper functions.",
                )

        for class_info in file_result["classes"]:
            class_name = class_info["name"]
            line_number = class_info["line_number"]

            if not class_info["has_docstring"]:
                add_issue(
                    issues,
                    "Missing Class Docstring",
                    "Low",
                    file_path,
                    line_number,
                    f"Class '{class_name}' does not have a docstring.",
                    "Add a short docstring explaining what the class represents.",
                )

    return issues