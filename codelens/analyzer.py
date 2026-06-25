def analyze_project(scan_results):
    """
    Takes scanner results and finds simple code quality issues.
    """

    issues = []

    for file_result in scan_results:
        file_path = file_result["file"]

        for function in file_result["functions"]:
            function_name = function["name"]
            line_number = function["line_number"]

            if not function["has_docstring"]:
                issues.append({
                    "type": "Missing Docstring",
                    "severity": "Low",
                    "file": file_path,
                    "line": line_number,
                    "message": f"Function '{function_name}' does not have a docstring.",
                    "suggestion": f"Add a short docstring explaining what '{function_name}' does.",
                })

            if function["has_division"]:
                issues.append({
                    "type": "Possible Runtime Error",
                    "severity": "High",
                    "file": file_path,
                    "line": line_number,
                    "message": f"Function '{function_name}' uses division. This may crash if the denominator is zero.",
                    "suggestion": "Add a check before division, for example: if b == 0, raise ValueError.",
                })

            if function["argument_count"] > 4:
                issues.append({
                    "type": "Too Many Arguments",
                    "severity": "Medium",
                    "file": file_path,
                    "line": line_number,
                    "message": f"Function '{function_name}' has {function['argument_count']} arguments.",
                    "suggestion": "Consider grouping related values into a dictionary, class, or data object.",
                })

            if function["line_count"] > 10:
                issues.append({
                    "type": "Long Function",
                    "severity": "Medium",
                    "file": file_path,
                    "line": line_number,
                    "message": f"Function '{function_name}' is {function['line_count']} lines long.",
                    "suggestion": "Consider splitting this function into smaller helper functions.",
                })

        for class_info in file_result["classes"]:
            class_name = class_info["name"]
            line_number = class_info["line_number"]

            if not class_info["has_docstring"]:
                issues.append({
                    "type": "Missing Docstring",
                    "severity": "Low",
                    "file": file_path,
                    "line": line_number,
                    "message": f"Class '{class_name}' does not have a docstring.",
                    "suggestion": f"Add a short docstring explaining the purpose of the '{class_name}' class.",
                })

    return issues