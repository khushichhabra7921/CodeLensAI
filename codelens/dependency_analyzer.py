from pathlib import Path


VERSION_OPERATORS = [
    "==",
    ">=",
    "<=",
    "~=",
    "!=",
    ">",
    "<",
]


def add_issue(issues, issue_type, severity, file_path, line, message, suggestion):
    """
    Adds a dependency issue.
    """

    issues.append(
        {
            "type": issue_type,
            "category": "Dependency",
            "severity": severity,
            "file": file_path,
            "line": line,
            "message": message,
            "suggestion": suggestion,
        }
    )


def strip_inline_comment(line):
    """
    Removes inline comments from a requirement line.
    """

    if " #" in line:
        return line.split(" #", 1)[0].strip()

    return line.strip()


def is_ignored_requirement_line(line):
    """
    Checks whether a requirement line should be ignored.
    """

    stripped = line.strip()

    if not stripped:
        return True

    if stripped.startswith("#"):
        return True

    return False


def is_option_line(line):
    """
    Checks if the line is a pip option line.
    """

    option_prefixes = [
        "--index-url",
        "--extra-index-url",
        "--trusted-host",
        "--find-links",
        "-f ",
    ]

    return any(line.startswith(prefix) for prefix in option_prefixes)


def is_nested_requirement_line(line):
    """
    Checks if the line points to another requirements file.
    """

    return (
        line.startswith("-r ")
        or line.startswith("--requirement ")
        or line.startswith("-c ")
        or line.startswith("--constraint ")
    )


def is_editable_install(line):
    """
    Checks if the line uses editable install.
    """

    return line.startswith("-e ") or line.startswith("--editable ")


def is_direct_url_dependency(line):
    """
    Checks if the line is a direct URL dependency.
    """

    return (
        line.startswith("http://")
        or line.startswith("https://")
        or line.startswith("git+")
    )


def is_local_path_dependency(line):
    """
    Checks if the line appears to be a local path dependency.
    """

    return (
        line.startswith(".")
        or line.startswith("/")
        or line.startswith("../")
        or line.startswith("./")
    )


def has_exact_pin(line):
    """
    Checks whether dependency has exact version pin using ==.
    """

    return "==" in line


def has_loose_version_constraint(line):
    """
    Checks whether dependency has a loose version constraint.
    """

    loose_operators = [
        ">=",
        "<=",
        "~=",
        "!=",
        ">",
        "<",
    ]

    return any(operator in line for operator in loose_operators)


def has_any_version_operator(line):
    """
    Checks whether dependency has any version operator.
    """

    return any(operator in line for operator in VERSION_OPERATORS)


def has_wildcard_pin(line):
    """
    Checks for wildcard pins like package==*.
    """

    if "==" not in line:
        return False

    version_part = line.split("==", 1)[1].strip()

    return "*" in version_part


def find_requirements_file(project_path):
    """
    Finds a requirements.txt file.

    Priority:
    1. requirements.txt inside analyzed project folder
    2. requirements.txt in current repository root
    3. expected path inside analyzed project folder
    """

    project_path = Path(project_path)

    project_requirements = project_path / "requirements.txt"

    if project_requirements.exists():
        return project_requirements

    root_requirements = Path("requirements.txt")

    if root_requirements.exists():
        return root_requirements

    return project_requirements


def analyze_requirement_line(
    issues,
    line,
    line_number,
    requirements_path,
    rules_config,
):
    """
    Analyzes one requirement line.
    """

    require_pinned_dependencies = rules_config.get(
        "require_pinned_dependencies",
        True,
    )

    allow_editable_installs = rules_config.get(
        "allow_editable_installs",
        False,
    )

    allow_http_dependencies = rules_config.get(
        "allow_http_dependencies",
        False,
    )

    if is_option_line(line):
        return

    if is_nested_requirement_line(line):
        add_issue(
            issues,
            "Nested Requirements File",
            "Low",
            str(requirements_path),
            line_number,
            "The requirements file references another requirements or constraints file.",
            "Make sure nested requirements files are also reviewed and version-pinned.",
        )
        return

    if is_editable_install(line):
        if not allow_editable_installs:
            add_issue(
                issues,
                "Editable Install",
                "Medium",
                str(requirements_path),
                line_number,
                "The requirements file uses an editable install.",
                "Avoid editable installs in production requirements. Use pinned package versions instead.",
            )
        return

    if line.startswith("http://") and not allow_http_dependencies:
        add_issue(
            issues,
            "Unsafe HTTP Dependency URL",
            "High",
            str(requirements_path),
            line_number,
            "The requirements file contains a dependency loaded over insecure HTTP.",
            "Use HTTPS dependency URLs whenever possible.",
        )
        return

    if is_direct_url_dependency(line):
        add_issue(
            issues,
            "Direct URL Dependency",
            "Low",
            str(requirements_path),
            line_number,
            "The requirements file uses a direct URL or VCS dependency.",
            "Prefer pinned package versions from a trusted package index when possible.",
        )
        return

    if is_local_path_dependency(line):
        add_issue(
            issues,
            "Local Path Dependency",
            "Low",
            str(requirements_path),
            line_number,
            "The requirements file uses a local path dependency.",
            "Local path dependencies may not work reliably in CI or other environments.",
        )
        return

    if not require_pinned_dependencies:
        return

    if has_wildcard_pin(line):
        add_issue(
            issues,
            "Wildcard Dependency Version",
            "Medium",
            str(requirements_path),
            line_number,
            "The dependency uses a wildcard version pin.",
            "Use an exact version pin such as package==1.2.3.",
        )
        return

    if has_loose_version_constraint(line):
        add_issue(
            issues,
            "Loose Dependency Version",
            "Medium",
            str(requirements_path),
            line_number,
            "The dependency uses a loose version constraint.",
            "Use exact version pins for reproducible installs, for example package==1.2.3.",
        )
        return

    if not has_any_version_operator(line):
        add_issue(
            issues,
            "Unpinned Dependency",
            "Medium",
            str(requirements_path),
            line_number,
            "The dependency is not pinned to an exact version.",
            "Pin the dependency version, for example package==1.2.3.",
        )


def analyze_dependency_issues(project_path, rules_config=None):
    """
    Analyzes dependency hygiene using requirements.txt.

    Detects:
    - Missing requirements.txt
    - Empty requirements.txt
    - Unpinned dependencies
    - Loose dependency versions
    - Wildcard dependency versions
    - Unsafe HTTP dependency URLs
    - Editable installs
    - Direct URL dependencies
    - Local path dependencies
    """

    if rules_config is None:
        rules_config = {}

    check_dependencies = rules_config.get("check_dependencies", True)

    if not check_dependencies:
        return []

    issues = []

    requirements_path = find_requirements_file(project_path)

    if not requirements_path.exists():
        add_issue(
            issues,
            "Missing Requirements File",
            "Low",
            str(requirements_path),
            1,
            "No requirements.txt file was found for dependency analysis.",
            "Add a requirements.txt file with pinned dependencies.",
        )
        return issues

    try:
        lines = requirements_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        add_issue(
            issues,
            "Unreadable Requirements File",
            "Low",
            str(requirements_path),
            1,
            "requirements.txt could not be read using UTF-8 encoding.",
            "Convert requirements.txt to UTF-8 encoding.",
        )
        return issues

    meaningful_lines = [
        line
        for line in lines
        if not is_ignored_requirement_line(line)
    ]

    if not meaningful_lines:
        add_issue(
            issues,
            "Empty Requirements File",
            "Low",
            str(requirements_path),
            1,
            "requirements.txt is empty or contains only comments.",
            "Add required dependencies with pinned versions.",
        )
        return issues

    for line_number, raw_line in enumerate(lines, start=1):
        if is_ignored_requirement_line(raw_line):
            continue

        cleaned_line = strip_inline_comment(raw_line)

        if not cleaned_line:
            continue

        analyze_requirement_line(
            issues,
            cleaned_line,
            line_number,
            requirements_path,
            rules_config,
        )

    return issues