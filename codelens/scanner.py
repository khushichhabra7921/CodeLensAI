import ast
from pathlib import Path


def function_has_division(function_node):
    """
    Checks if a function uses division.
    Example: a / b
    """

    for node in ast.walk(function_node):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return True

    return False


def get_function_line_count(function_node):
    """
    Counts how many lines a function takes.
    """

    if hasattr(function_node, "end_lineno") and function_node.end_lineno is not None:
        return function_node.end_lineno - function_node.lineno + 1

    return 1


def scan_python_file(file_path):
    """
    Scans one Python file and extracts imports, functions, classes,
    arguments, line numbers, docstrings, and simple risk signals.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    imports = []
    functions = []
    classes = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)

        elif isinstance(node, ast.FunctionDef):
            arguments = []

            for arg in node.args.args:
                arguments.append(arg.arg)

            real_arguments = [
                arg for arg in arguments
                if arg not in ["self", "cls"]
            ]

            docstring = ast.get_docstring(node)

            functions.append({
                "name": node.name,
                "arguments": arguments,
                "argument_count": len(real_arguments),
                "line_number": node.lineno,
                "line_count": get_function_line_count(node),
                "has_docstring": docstring is not None,
                "docstring": docstring,
                "has_division": function_has_division(node),
            })

        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)

            classes.append({
                "name": node.name,
                "line_number": node.lineno,
                "has_docstring": docstring is not None,
                "docstring": docstring,
            })

    return {
        "file": str(file_path),
        "imports": imports,
        "functions": functions,
        "classes": classes,
    }


def scan_project(project_path):
    """
    Scans all Python files inside a project folder.
    """

    project_path = Path(project_path)
    python_files = list(project_path.rglob("*.py"))

    results = []

    for file_path in python_files:
        result = scan_python_file(file_path)
        results.append(result)

    return results