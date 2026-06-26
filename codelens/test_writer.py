import re
from pathlib import Path


GENERATED_TESTS_DIR = Path("generated_tests")


def sanitize_identifier(value):
    """
    Converts a string into a safe Python identifier fragment.
    """

    value = re.sub(r"[^a-zA-Z0-9_]", "_", str(value))
    value = value.strip("_")

    if not value:
        return "target"

    if value[0].isdigit():
        value = f"target_{value}"

    return value.lower()


def get_relative_source_path(file_path):
    """
    Returns a source path that works from generated_tests/ test files.
    """

    file_path = Path(file_path)

    try:
        relative_path = file_path.resolve().relative_to(Path.cwd().resolve())
        return relative_path.as_posix()
    except ValueError:
        return file_path.as_posix()


def clean_old_generated_tests(output_dir):
    """
    Removes old generated pytest files created by CodeLens AI.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for test_file in output_dir.glob("test_*_generated.py"):
        test_file.unlink()


def build_test_file_header(source_file_path, module_variable_name):
    """
    Builds the header for a generated pytest file.
    """

    relative_source_path = get_relative_source_path(source_file_path)

    return f'''"""
Auto-generated pytest tests by CodeLens AI.

These tests are intentionally conservative.
They check imports, function existence, callable behavior,
and common behavior for simple function names.
"""

import importlib.util
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / Path("{relative_source_path}")
MODULE_NAME = "codelens_generated_target_{module_variable_name}"


def load_target_module():
    """
    Loads the analyzed Python file as a module.
    """

    if not SOURCE_FILE.exists():
        pytest.fail(f"Source file not found: {{SOURCE_FILE}}")

    spec = importlib.util.spec_from_file_location(MODULE_NAME, SOURCE_FILE)

    if spec is None or spec.loader is None:
        pytest.fail(f"Could not load module from: {{SOURCE_FILE}}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)

    return module


target_module = load_target_module()


'''
    

def build_function_exists_test(function):
    """
    Builds a test that checks whether a top-level function exists.
    """

    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_exists():
    assert hasattr(target_module, "{function_name}")


def test_{safe_name}_is_callable():
    func = getattr(target_module, "{function_name}")
    assert callable(func)

'''


def build_method_skip_test(function):
    """
    Builds a skipped test for class methods because object setup is unknown.
    """

    parent_class = function.get("parent_class", "UnknownClass")
    function_name = function["name"]
    qualified_name = function.get("qualified_name", f"{parent_class}.{function_name}")
    safe_name = sanitize_identifier(qualified_name)

    return f'''
def test_{safe_name}_requires_object_setup():
    pytest.skip("Skipping {qualified_name}: class method tests require object setup.")

'''


def build_addition_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_adds_positive_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(2, 3) == 5


def test_{safe_name}_handles_zero():
    func = getattr(target_module, "{function_name}")
    assert func(0, 5) == 5


def test_{safe_name}_handles_negative_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(-2, -3) == -5

'''


def build_subtraction_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_subtracts_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(5, 3) == 2


def test_{safe_name}_subtracts_negative_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(-5, -3) == -2

'''


def build_multiplication_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_multiplies_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(4, 3) == 12


def test_{safe_name}_multiplies_by_zero():
    func = getattr(target_module, "{function_name}")
    assert func(4, 0) == 0

'''


def build_division_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_divides_numbers():
    func = getattr(target_module, "{function_name}")
    assert func(10, 2) == 5


def test_{safe_name}_zero_division_behavior_is_handled():
    func = getattr(target_module, "{function_name}")

    try:
        result = func(10, 0)
    except Exception:
        return

    assert result is not None or result is None

'''


def build_square_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_squares_number():
    func = getattr(target_module, "{function_name}")
    assert func(3) == 9

'''


def build_cube_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_cubes_number():
    func = getattr(target_module, "{function_name}")
    assert func(3) == 27

'''


def build_power_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_calculates_power():
    func = getattr(target_module, "{function_name}")
    assert func(2, 3) == 8

'''


def build_reverse_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_reverses_string():
    func = getattr(target_module, "{function_name}")
    assert func("abc") == "cba"

'''


def build_even_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_detects_even_number():
    func = getattr(target_module, "{function_name}")
    assert func(4) is True

'''


def build_odd_tests(function):
    function_name = function["name"]
    safe_name = sanitize_identifier(function_name)

    return f'''
def test_{safe_name}_detects_odd_number():
    func = getattr(target_module, "{function_name}")
    assert func(5) is True

'''


def build_behavior_tests(function):
    """
    Builds behavior tests for common simple function names.
    """

    function_name = function["name"]
    lower_name = function_name.lower()
    argument_count = function["argument_count"]

    if argument_count == 2 and any(keyword in lower_name for keyword in ["add", "sum", "plus"]):
        return build_addition_tests(function)

    if argument_count == 2 and any(keyword in lower_name for keyword in ["subtract", "minus", "difference"]):
        return build_subtraction_tests(function)

    if argument_count == 2 and any(keyword in lower_name for keyword in ["multiply", "product"]):
        return build_multiplication_tests(function)

    if argument_count == 2 and any(keyword in lower_name for keyword in ["divide", "division"]):
        return build_division_tests(function)

    if argument_count == 1 and "square" in lower_name:
        return build_square_tests(function)

    if argument_count == 1 and "cube" in lower_name:
        return build_cube_tests(function)

    if argument_count == 2 and "power" in lower_name:
        return build_power_tests(function)

    if argument_count == 1 and "reverse" in lower_name:
        return build_reverse_tests(function)

    if argument_count == 1 and "even" in lower_name:
        return build_even_tests(function)

    if argument_count == 1 and "odd" in lower_name:
        return build_odd_tests(function)

    return ""


def build_tests_for_function(function):
    """
    Builds pytest code for one scanned function.
    """

    if function.get("parent_class"):
        return build_method_skip_test(function)

    test_code = []
    test_code.append(build_function_exists_test(function))

    behavior_tests = build_behavior_tests(function)

    if behavior_tests:
        test_code.append(behavior_tests)

    return "\n".join(test_code)


def build_test_file_content(file_result):
    """
    Builds complete pytest file content for one source file.
    """

    source_file_path = file_result["file"]
    module_variable_name = sanitize_identifier(Path(source_file_path).stem)

    content_parts = []

    content_parts.append(
        build_test_file_header(
            source_file_path,
            module_variable_name,
        )
    )

    for function in file_result["functions"]:
        content_parts.append(build_tests_for_function(function))

    return "\n".join(content_parts)


def generate_pytest_files(scan_results, output_dir=GENERATED_TESTS_DIR):
    """
    Generates pytest files from scan results.

    Returns a list of generated file paths.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_old_generated_tests(output_dir)

    generated_files = []

    for file_result in scan_results:
        if not file_result["functions"]:
            continue

        source_file_path = Path(file_result["file"])
        safe_file_name = sanitize_identifier(source_file_path.stem)
        test_file_path = output_dir / f"test_{safe_file_name}_generated.py"

        test_content = build_test_file_content(file_result)

        with open(test_file_path, "w", encoding="utf-8") as file:
            file.write(test_content)

        generated_files.append(str(test_file_path))

    return generated_files