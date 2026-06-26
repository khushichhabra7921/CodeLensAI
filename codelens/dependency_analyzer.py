from pathlib import Path
import tomllib


VERSION_OPERATORS = [
    "==",
    ">=",
    "<=",
    "~=",
    "!=",
    ">",
    "<",
]


DEFAULT_DEPENDENCY_FILE_PATTERNS = [
    "requirements.txt",
    "requirements-dev.txt",
    "dev-requirements.txt",
    "requirements/*.txt",
    "pyproject.toml",
    "Pipfile",
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


def normalize_dependency_patterns(rules_config):
    """
    Gets dependency file patterns from config.
    """

    patterns = rules_config.get(
        "dependency_file_patterns",
        DEFAULT_DEPENDENCY_FILE_PATTERNS,
    )

    if patterns is None:
        return []

    return patterns


def discover_dependency_files(project_path, rules_config):
    """
    Finds dependency files using config patterns.

    It searches:
    1. Inside the analyzed project folder
    2. In the repository root folder
    """

    project_path = Path(project_path)
    root_path = Path(".")
    patterns = normalize_dependency_patterns(rules_config)

    dependency_files = []

    for search_base in [project_path, root_path]:
        for pattern in patterns:
            matched_files = list(search_base.glob(pattern))

            for matched_file in matched_files:
                if matched_file.is_file() and matched_file not in dependency_files:
                    dependency_files.append(matched_file)

    return sorted(dependency_files)


def analyze_requirement_line(
    issues,
    line,
    line_number,
    dependency_file_path,
    rules_config,
):
    """
    Analyzes one requirement-style dependency line.
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
            str(dependency_file_path),
            line_number,
            "The dependency file references another requirements or constraints file.",
            "Make sure nested requirements files are also reviewed and version-pinned.",
        )
        return

    if is_editable_install(line):
        if not allow_editable_installs:
            add_issue(
                issues,
                "Editable Install",
                "Medium",
                str(dependency_file_path),
                line_number,
                "The dependency file uses an editable install.",
                "Avoid editable installs in production requirements. Use pinned package versions instead.",
            )
        return

    if line.startswith("http://") and not allow_http_dependencies:
        add_issue(
            issues,
            "Unsafe HTTP Dependency URL",
            "High",
            str(dependency_file_path),
            line_number,
            "The dependency file contains a dependency loaded over insecure HTTP.",
            "Use HTTPS dependency URLs whenever possible.",
        )
        return

    if is_direct_url_dependency(line):
        add_issue(
            issues,
            "Direct URL Dependency",
            "Low",
            str(dependency_file_path),
            line_number,
            "The dependency file uses a direct URL or VCS dependency.",
            "Prefer pinned package versions from a trusted package index when possible.",
        )
        return

    if is_local_path_dependency(line):
        add_issue(
            issues,
            "Local Path Dependency",
            "Low",
            str(dependency_file_path),
            line_number,
            "The dependency file uses a local path dependency.",
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
            str(dependency_file_path),
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
            str(dependency_file_path),
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
            str(dependency_file_path),
            line_number,
            "The dependency is not pinned to an exact version.",
            "Pin the dependency version, for example package==1.2.3.",
        )


def analyze_requirements_file(dependency_file_path, rules_config):
    """
    Analyzes requirements-style dependency files.

    Supported examples:
    - requirements.txt
    - requirements-dev.txt
    - dev-requirements.txt
    - requirements/*.txt
    """

    issues = []
    dependency_file_path = Path(dependency_file_path)

    try:
        lines = dependency_file_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        add_issue(
            issues,
            "Unreadable Dependency File",
            "Low",
            str(dependency_file_path),
            1,
            "The dependency file could not be read using UTF-8 encoding.",
            "Convert the dependency file to UTF-8 encoding.",
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
            "Empty Dependency File",
            "Low",
            str(dependency_file_path),
            1,
            "The dependency file is empty or contains only comments.",
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
            dependency_file_path,
            rules_config,
        )

    return issues


def load_toml_file(file_path):
    """
    Loads a TOML file such as pyproject.toml or Pipfile.
    """

    file_path = Path(file_path)

    with open(file_path, "rb") as file:
        return tomllib.load(file)


def dependency_spec_to_string(name, spec):
    """
    Converts dependency data from TOML files into a string for analysis.
    """

    if isinstance(spec, str):
        if spec == "*":
            return name

        return f"{name}{spec}"

    if isinstance(spec, dict):
        version = spec.get("version")

        if version:
            if version == "*":
                return name

            return f"{name}{version}"

        git_value = spec.get("git")
        path_value = spec.get("path")
        url_value = spec.get("url")

        if git_value:
            return f"git+{git_value}"

        if path_value:
            return str(path_value)

        if url_value:
            return str(url_value)

    return name


def analyze_toml_dependency_list(
    issues,
    dependency_list,
    dependency_file_path,
    section_name,
    rules_config,
):
    """
    Analyzes dependencies stored as a list in TOML.

    Example:
    [project]
    dependencies = [
        "requests>=2.0.0",
        "pytest",
    ]
    """

    for index, dependency in enumerate(dependency_list, start=1):
        if not isinstance(dependency, str):
            add_issue(
                issues,
                "Unsupported Dependency Format",
                "Low",
                str(dependency_file_path),
                index,
                f"The dependency in section '{section_name}' has an unsupported format.",
                "Use normal dependency strings such as package==1.2.3.",
            )
            continue

        analyze_requirement_line(
            issues,
            dependency.strip(),
            index,
            dependency_file_path,
            rules_config,
        )


def analyze_toml_dependency_table(
    issues,
    dependency_table,
    dependency_file_path,
    section_name,
    rules_config,
):
    """
    Analyzes dependencies stored as a TOML table.

    Example:
    [tool.poetry.dependencies]
    requests = "^2.31.0"

    [packages]
    flask = "*"
    """

    line_number = 1

    for dependency_name, dependency_spec in dependency_table.items():
        if dependency_name.lower() == "python":
            continue

        dependency_line = dependency_spec_to_string(
            dependency_name,
            dependency_spec,
        )

        analyze_requirement_line(
            issues,
            dependency_line,
            line_number,
            dependency_file_path,
            rules_config,
        )

        line_number += 1


def analyze_pyproject_file(dependency_file_path, rules_config):
    """
    Analyzes pyproject.toml dependencies.

    Supported sections:
    - [project] dependencies
    - [project] optional-dependencies
    - [tool.poetry.dependencies]
    - [tool.poetry.group.*.dependencies]
    """

    issues = []
    dependency_file_path = Path(dependency_file_path)

    try:
        data = load_toml_file(dependency_file_path)
    except tomllib.TOMLDecodeError:
        add_issue(
            issues,
            "Invalid TOML File",
            "Low",
            str(dependency_file_path),
            1,
            "The pyproject.toml file could not be parsed.",
            "Fix the TOML syntax and run CodeLens AI again.",
        )
        return issues

    project_section = data.get("project", {})
    dependencies = project_section.get("dependencies", [])

    if isinstance(dependencies, list):
        analyze_toml_dependency_list(
            issues,
            dependencies,
            dependency_file_path,
            "project.dependencies",
            rules_config,
        )

    optional_dependencies = project_section.get("optional-dependencies", {})

    if isinstance(optional_dependencies, dict):
        for group_name, group_dependencies in optional_dependencies.items():
            if isinstance(group_dependencies, list):
                analyze_toml_dependency_list(
                    issues,
                    group_dependencies,
                    dependency_file_path,
                    f"project.optional-dependencies.{group_name}",
                    rules_config,
                )

    tool_section = data.get("tool", {})
    poetry_section = tool_section.get("poetry", {})

    poetry_dependencies = poetry_section.get("dependencies", {})

    if isinstance(poetry_dependencies, dict):
        analyze_toml_dependency_table(
            issues,
            poetry_dependencies,
            dependency_file_path,
            "tool.poetry.dependencies",
            rules_config,
        )

    poetry_groups = poetry_section.get("group", {})

    if isinstance(poetry_groups, dict):
        for group_name, group_data in poetry_groups.items():
            if not isinstance(group_data, dict):
                continue

            group_dependencies = group_data.get("dependencies", {})

            if isinstance(group_dependencies, dict):
                analyze_toml_dependency_table(
                    issues,
                    group_dependencies,
                    dependency_file_path,
                    f"tool.poetry.group.{group_name}.dependencies",
                    rules_config,
                )

    if not issues and not dependencies and not poetry_dependencies:
        add_issue(
            issues,
            "No Dependencies Found",
            "Low",
            str(dependency_file_path),
            1,
            "The pyproject.toml file was found, but no supported dependency sections were detected.",
            "Add dependencies under [project] or [tool.poetry.dependencies] if this project uses pyproject.toml for dependency management.",
        )

    return issues


def analyze_pipfile(dependency_file_path, rules_config):
    """
    Analyzes Pipfile dependencies.

    Supported sections:
    - [packages]
    - [dev-packages]
    """

    issues = []
    dependency_file_path = Path(dependency_file_path)

    try:
        data = load_toml_file(dependency_file_path)
    except tomllib.TOMLDecodeError:
        add_issue(
            issues,
            "Invalid TOML File",
            "Low",
            str(dependency_file_path),
            1,
            "The Pipfile could not be parsed.",
            "Fix the TOML syntax and run CodeLens AI again.",
        )
        return issues

    packages = data.get("packages", {})
    dev_packages = data.get("dev-packages", {})

    if isinstance(packages, dict):
        analyze_toml_dependency_table(
            issues,
            packages,
            dependency_file_path,
            "packages",
            rules_config,
        )

    if isinstance(dev_packages, dict):
        analyze_toml_dependency_table(
            issues,
            dev_packages,
            dependency_file_path,
            "dev-packages",
            rules_config,
        )

    if not issues and not packages and not dev_packages:
        add_issue(
            issues,
            "No Dependencies Found",
            "Low",
            str(dependency_file_path),
            1,
            "The Pipfile was found, but no package sections were detected.",
            "Add dependencies under [packages] or [dev-packages].",
        )

    return issues


def analyze_dependency_file(dependency_file_path, rules_config):
    """
    Analyzes one dependency file based on file name.
    """

    dependency_file_path = Path(dependency_file_path)

    if dependency_file_path.name == "pyproject.toml":
        return analyze_pyproject_file(dependency_file_path, rules_config)

    if dependency_file_path.name == "Pipfile":
        return analyze_pipfile(dependency_file_path, rules_config)

    return analyze_requirements_file(dependency_file_path, rules_config)


def analyze_dependency_issues(project_path, rules_config=None):
    """
    Analyzes dependency hygiene using supported dependency files.

    Detects:
    - Missing dependency files
    - Empty dependency files
    - Unpinned dependencies
    - Loose dependency versions
    - Wildcard dependency versions
    - Unsafe HTTP dependency URLs
    - Editable installs
    - Direct URL dependencies
    - Local path dependencies
    - Unsupported dependency formats
    - Invalid TOML dependency files
    """

    if rules_config is None:
        rules_config = {}

    check_dependencies = rules_config.get("check_dependencies", True)

    if not check_dependencies:
        return []

    issues = []

    dependency_files = discover_dependency_files(project_path, rules_config)

    if not dependency_files:
        expected_patterns = ", ".join(normalize_dependency_patterns(rules_config))

        add_issue(
            issues,
            "Missing Dependency File",
            "Low",
            str(project_path),
            1,
            "No supported dependency file was found for dependency analysis.",
            f"Add one of these supported dependency files: {expected_patterns}.",
        )
        return issues

    for dependency_file in dependency_files:
        file_issues = analyze_dependency_file(
            dependency_file,
            rules_config,
        )

        issues.extend(file_issues)

    return issues