import ast
from pathlib import Path


DEFAULT_IGNORED_FOLDERS = [
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "generated_tests",
    "reports",
    "node_modules",
    "dist",
    "build",
]


DEFAULT_IGNORED_FILES = []


def get_import_name(node):
    """
    Extracts import names from AST import nodes.
    """

    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]

    if isinstance(node, ast.ImportFrom):
        module_name = node.module or ""

        imported_names = []

        for alias in node.names:
            if module_name:
                imported_names.append(f"{module_name}.{alias.name}")
            else:
                imported_names.append(alias.name)

        return imported_names

    return []


def function_uses_division(function_node):
    """
    Checks whether a function contains division operations.
    """

    division_nodes = (
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
    )

    for node in ast.walk(function_node):
        if isinstance(node, ast.BinOp) and isinstance(node.op, division_nodes):
            return True

    return False


def get_function_arguments(function_node):
    """
    Extracts function argument names.
    """

    arguments = []

    for argument in function_node.args.args:
        arguments.append(argument.arg)

    for argument in function_node.args.kwonlyargs:
        arguments.append(argument.arg)

    if function_node.args.vararg:
        arguments.append(f"*{function_node.args.vararg.arg}")

    if function_node.args.kwarg:
        arguments.append(f"**{function_node.args.kwarg.arg}")

    return arguments


def get_line_count(node):
    """
    Calculates line count for an AST node.
    """

    start_line = getattr(node, "lineno", None)
    end_line = getattr(node, "end_lineno", None)

    if start_line is None or end_line is None:
        return 0

    return max(1, end_line - start_line + 1)


def should_ignore_folder(folder_name, ignored_folders):
    """
    Checks whether a folder should be ignored.
    """

    return folder_name in ignored_folders


def should_ignore_file(file_name, ignored_files):
    """
    Checks whether a file should be ignored.
    """

    return file_name in ignored_files


def normalize_ignore_config(ignore_config=None):
    """
    Normalizes ignore config from codelens.yml.
    """

    if ignore_config is None:
        ignore_config = {}

    ignored_folders = ignore_config.get("folders", DEFAULT_IGNORED_FOLDERS)
    ignored_files = ignore_config.get("files", DEFAULT_IGNORED_FILES)

    if ignored_folders is None:
        ignored_folders = []

    if ignored_files is None:
        ignored_files = []

    return {
        "folders": set(ignored_folders),
        "files": set(ignored_files),
    }


def discover_python_files(project_path, ignore_config=None):
    """
    Discovers Python files while respecting ignored folders and files.
    """

    project_path = Path(project_path)
    normalized_ignore = normalize_ignore_config(ignore_config)

    ignored_folders = normalized_ignore["folders"]
    ignored_files = normalized_ignore["files"]

    python_files = []

    for file_path in project_path.rglob("*.py"):
        relative_parts = file_path.relative_to(project_path).parts

        if any(should_ignore_folder(part, ignored_folders) for part in relative_parts[:-1]):
            continue

        if should_ignore_file(file_path.name, ignored_files):
            continue

        python_files.append(file_path)

    return sorted(python_files)


class PythonFileVisitor(ast.NodeVisitor):
    """
    AST visitor that extracts imports, functions, and classes.

    It also detects whether a function is a top-level function or a class method.
    """

    def __init__(self):
        self.imports = []
        self.functions = []
        self.classes = []
        self.class_stack = []

    def visit_Import(self, node):
        self.imports.extend(get_import_name(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports.extend(get_import_name(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_name = node.name

        self.classes.append(
            {
                "name": class_name,
                "line_number": node.lineno,
                "line_count": get_line_count(node),
                "has_docstring": ast.get_docstring(node) is not None,
            }
        )

        self.class_stack.append(class_name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node):
        self._visit_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node):
        self._visit_function(node, is_async=True)

    def _visit_function(self, node, is_async):
        arguments = get_function_arguments(node)

        parent_class = self.class_stack[-1] if self.class_stack else None

        if parent_class:
            qualified_name = f"{parent_class}.{node.name}"
        else:
            qualified_name = node.name

        self.functions.append(
            {
                "name": node.name,
                "qualified_name": qualified_name,
                "parent_class": parent_class,
                "arguments": arguments,
                "argument_count": len(arguments),
                "line_number": node.lineno,
                "line_count": get_line_count(node),
                "has_docstring": ast.get_docstring(node) is not None,
                "has_division": function_uses_division(node),
                "is_async": is_async,
            }
        )

        self.generic_visit(node)


def scan_python_file(file_path):
    """
    Scans one Python file and extracts imports, functions, classes, and metadata.
    """

    file_path = Path(file_path)

    result = {
        "file": str(file_path),
        "imports": [],
        "functions": [],
        "classes": [],
    }

    try:
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)
    except UnicodeDecodeError:
        result["parse_error"] = "File could not be read using UTF-8 encoding."
        return result
    except SyntaxError as error:
        result["parse_error"] = f"Syntax error on line {error.lineno or 1}."
        return result

    visitor = PythonFileVisitor()
    visitor.visit(tree)

    result["imports"] = sorted(set(visitor.imports))
    result["functions"] = visitor.functions
    result["classes"] = visitor.classes

    return result


def scan_project(project_path, ignore_config=None):
    """
    Scans a Python project folder while respecting ignore patterns.
    """

    project_path = Path(project_path)

    python_files = discover_python_files(project_path, ignore_config)

    scan_results = []

    for file_path in python_files:
        scan_results.append(scan_python_file(file_path))

    return scan_results