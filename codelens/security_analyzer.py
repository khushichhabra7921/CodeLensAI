import ast
from pathlib import Path


SECRET_KEYWORDS = [
    "password",
    "passwd",
    "pwd",
    "secret",
    "api_key",
    "apikey",
    "access_key",
    "private_key",
    "token",
    "auth_token",
    "client_secret",
]

PLACEHOLDER_VALUES = [
    "",
    "none",
    "null",
    "changeme",
    "change_me",
    "your_api_key_here",
    "your-token-here",
    "your_token_here",
    "example",
    "sample",
    "test",
    "dummy",
    "placeholder",
]


def get_call_name(node):
    """
    Converts a function call AST node into a readable name.

    Examples:
    eval(...) -> eval
    os.system(...) -> os.system
    subprocess.run(...) -> subprocess.run
    pickle.loads(...) -> pickle.loads
    """

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent_name = get_call_name(node.value)

        if parent_name:
            return f"{parent_name}.{node.attr}"

        return node.attr

    return None


def is_string_value(node):
    """
    Checks whether an AST node is a string value.
    """

    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def get_string_value(node):
    """
    Safely extracts a string value from an AST node.
    """

    if is_string_value(node):
        return node.value

    return None


def is_placeholder_secret(value):
    """
    Checks if a hardcoded secret value is only a placeholder.
    """

    cleaned_value = value.strip().lower()

    if cleaned_value in PLACEHOLDER_VALUES:
        return True

    if "your" in cleaned_value and "here" in cleaned_value:
        return True

    if cleaned_value.startswith("<") and cleaned_value.endswith(">"):
        return True

    return False


def looks_like_secret_name(name):
    """
    Checks whether a variable name looks like it may contain a secret.
    """

    normalized_name = name.lower().replace("-", "_")

    for keyword in SECRET_KEYWORDS:
        if keyword in normalized_name:
            return True

    return False


def get_assignment_target_names(node):
    """
    Extracts variable names from assignment statements.

    Examples:
    password = "abc" -> password
    config.api_key = "abc" -> config.api_key
    """

    target_names = []

    if isinstance(node, ast.Assign):
        targets = node.targets
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
    else:
        return target_names

    for target in targets:
        if isinstance(target, ast.Name):
            target_names.append(target.id)

        elif isinstance(target, ast.Attribute):
            target_name = get_call_name(target)
            if target_name:
                target_names.append(target_name)

        elif isinstance(target, ast.Tuple):
            for element in target.elts:
                if isinstance(element, ast.Name):
                    target_names.append(element.id)

    return target_names


def keyword_argument_is_true(call_node, keyword_name):
    """
    Checks if a function call has keyword_name=True.

    Example:
    subprocess.run("ls", shell=True)
    """

    for keyword in call_node.keywords:
        if keyword.arg == keyword_name:
            if isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                return True

    return False


def yaml_load_without_safe_loader(call_node):
    """
    Detects yaml.load(...) without SafeLoader.
    """

    call_name = get_call_name(call_node.func)

    if call_name != "yaml.load":
        return False

    for keyword in call_node.keywords:
        if keyword.arg == "Loader":
            loader_name = get_call_name(keyword.value)

            if loader_name and "SafeLoader" in loader_name:
                return False

    return True


def add_issue(issues, issue_type, severity, file_path, line, message, suggestion):
    """
    Adds a security issue in the same format used by the normal analyzer.
    """

    issues.append(
        {
            "type": issue_type,
            "category": "Security",
            "severity": severity,
            "file": file_path,
            "line": line,
            "message": message,
            "suggestion": suggestion,
        }
    )


def analyze_security_issues(scan_results):
    """
    Analyzes scanned Python files for common security risks.

    Detects:
    - eval()
    - exec()
    - os.system()
    - subprocess with shell=True
    - pickle.load / pickle.loads
    - yaml.load without SafeLoader
    - hardcoded secrets
    - insecure HTTP URLs
    """

    security_issues = []

    for file_result in scan_results:
        file_path = file_result["file"]
        path = Path(file_path)

        try:
            source_code = path.read_text(encoding="utf-8")
            tree = ast.parse(source_code)
        except UnicodeDecodeError:
            add_issue(
                security_issues,
                "Unreadable File",
                "Low",
                file_path,
                1,
                "This file could not be read using UTF-8 encoding.",
                "Check the file encoding and convert it to UTF-8 if needed.",
            )
            continue
        except SyntaxError as error:
            add_issue(
                security_issues,
                "Syntax Error",
                "High",
                file_path,
                error.lineno or 1,
                "This file contains a syntax error, so security analysis may be incomplete.",
                "Fix the syntax error and run CodeLens AI again.",
            )
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_name = get_call_name(node.func)
                line_number = getattr(node, "lineno", 1)

                if call_name == "eval":
                    add_issue(
                        security_issues,
                        "Unsafe eval Usage",
                        "Critical",
                        file_path,
                        line_number,
                        "The code uses eval(), which can execute arbitrary Python code.",
                        "Avoid eval(). Use safer parsing methods such as ast.literal_eval() when possible.",
                    )

                elif call_name == "exec":
                    add_issue(
                        security_issues,
                        "Unsafe exec Usage",
                        "Critical",
                        file_path,
                        line_number,
                        "The code uses exec(), which can execute arbitrary Python code.",
                        "Avoid exec(). Refactor the logic so dynamic code execution is not required.",
                    )

                elif call_name == "os.system":
                    add_issue(
                        security_issues,
                        "Unsafe os.system Usage",
                        "High",
                        file_path,
                        line_number,
                        "The code uses os.system(), which may allow command injection if user input is included.",
                        "Use subprocess.run() with a list of arguments and avoid shell=True.",
                    )

                elif call_name in [
                    "subprocess.run",
                    "subprocess.call",
                    "subprocess.Popen",
                    "subprocess.check_call",
                    "subprocess.check_output",
                ]:
                    if keyword_argument_is_true(node, "shell"):
                        add_issue(
                            security_issues,
                            "Subprocess shell=True",
                            "High",
                            file_path,
                            line_number,
                            "The code uses subprocess with shell=True, which can be dangerous with user input.",
                            "Use shell=False and pass commands as a list of arguments.",
                        )

                elif call_name in ["pickle.load", "pickle.loads"]:
                    add_issue(
                        security_issues,
                        "Unsafe Pickle Usage",
                        "High",
                        file_path,
                        line_number,
                        "The code uses pickle to load data. Pickle can execute code when loading untrusted data.",
                        "Avoid loading pickle data from untrusted sources. Use JSON for safer data exchange.",
                    )

                elif yaml_load_without_safe_loader(node):
                    add_issue(
                        security_issues,
                        "Unsafe YAML Load",
                        "High",
                        file_path,
                        line_number,
                        "The code uses yaml.load() without SafeLoader.",
                        "Use yaml.safe_load() or yaml.load(..., Loader=yaml.SafeLoader).",
                    )

                elif call_name == "tempfile.mktemp":
                    add_issue(
                        security_issues,
                        "Insecure Temporary File",
                        "Medium",
                        file_path,
                        line_number,
                        "The code uses tempfile.mktemp(), which can create insecure temporary file names.",
                        "Use tempfile.NamedTemporaryFile() or tempfile.TemporaryDirectory() instead.",
                    )

            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                line_number = getattr(node, "lineno", 1)
                target_names = get_assignment_target_names(node)

                value_node = node.value
                value = get_string_value(value_node)

                if value is not None:
                    for target_name in target_names:
                        if looks_like_secret_name(target_name) and not is_placeholder_secret(value):
                            add_issue(
                                security_issues,
                                "Hardcoded Secret",
                                "High",
                                file_path,
                                line_number,
                                f"The variable '{target_name}' appears to contain a hardcoded secret.",
                                "Move secrets to environment variables or a secure secrets manager.",
                            )

                    if value.startswith("http://"):
                        add_issue(
                            security_issues,
                            "Insecure HTTP URL",
                            "Low",
                            file_path,
                            line_number,
                            "The code contains an insecure HTTP URL.",
                            "Use HTTPS URLs whenever possible.",
                        )

    return security_issues