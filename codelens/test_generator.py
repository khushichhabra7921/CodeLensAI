def infer_test_strategy(function):
    """
    Infers a simple test strategy from function metadata.
    """

    function_name = function["name"].lower()
    argument_count = function["argument_count"]
    has_division = function.get("has_division", False)
    parent_class = function.get("parent_class")

    strategies = []

    if parent_class:
        strategies.append("Class method detected. Test requires object setup.")

    if argument_count == 0:
        strategies.append("Function has no arguments. Add a smoke test.")

    if argument_count > 0:
        strategies.append("Test with normal valid inputs.")

    if has_division:
        strategies.append("Test with non-zero denominator.")
        strategies.append("Test zero denominator behavior.")

    if any(keyword in function_name for keyword in ["add", "sum", "plus"]):
        strategies.append("Test addition with positive, negative, and zero values.")

    if any(keyword in function_name for keyword in ["subtract", "minus", "difference"]):
        strategies.append("Test subtraction with positive, negative, and zero values.")

    if any(keyword in function_name for keyword in ["multiply", "product"]):
        strategies.append("Test multiplication with positive, negative, and zero values.")

    if any(keyword in function_name for keyword in ["divide", "division"]):
        strategies.append("Test division with valid divisor and zero divisor.")

    if any(keyword in function_name for keyword in ["power", "square", "cube"]):
        strategies.append("Test numeric power-style behavior.")

    if any(keyword in function_name for keyword in ["reverse", "palindrome"]):
        strategies.append("Test string edge cases.")

    if any(keyword in function_name for keyword in ["even", "odd"]):
        strategies.append("Test even and odd numbers.")

    if not strategies:
        strategies.append("Start with import, existence, callable, and smoke tests.")

    return strategies


def build_suggested_tests(function):
    """
    Builds readable pytest test suggestions.
    """

    function_name = function["name"]
    qualified_name = function.get("qualified_name", function_name)
    parent_class = function.get("parent_class")

    suggestions = []

    suggestions.append(f"test_{function_name}_exists")
    suggestions.append(f"test_{function_name}_is_callable")

    if parent_class:
        suggestions.append(f"test_{qualified_name.replace('.', '_')}_with_object_setup")
        return suggestions

    lower_name = function_name.lower()

    if any(keyword in lower_name for keyword in ["add", "sum", "plus"]):
        suggestions.append(f"test_{function_name}_adds_positive_numbers")
        suggestions.append(f"test_{function_name}_handles_zero")
        suggestions.append(f"test_{function_name}_handles_negative_numbers")

    elif any(keyword in lower_name for keyword in ["subtract", "minus", "difference"]):
        suggestions.append(f"test_{function_name}_subtracts_numbers")
        suggestions.append(f"test_{function_name}_handles_negative_numbers")

    elif any(keyword in lower_name for keyword in ["multiply", "product"]):
        suggestions.append(f"test_{function_name}_multiplies_numbers")
        suggestions.append(f"test_{function_name}_handles_zero")

    elif any(keyword in lower_name for keyword in ["divide", "division"]):
        suggestions.append(f"test_{function_name}_divides_numbers")
        suggestions.append(f"test_{function_name}_handles_zero_division")

    elif "square" in lower_name:
        suggestions.append(f"test_{function_name}_squares_number")

    elif "cube" in lower_name:
        suggestions.append(f"test_{function_name}_cubes_number")

    elif "power" in lower_name:
        suggestions.append(f"test_{function_name}_calculates_power")

    elif "reverse" in lower_name:
        suggestions.append(f"test_{function_name}_reverses_string")

    elif "palindrome" in lower_name:
        suggestions.append(f"test_{function_name}_detects_palindrome")

    elif "even" in lower_name:
        suggestions.append(f"test_{function_name}_detects_even_number")

    elif "odd" in lower_name:
        suggestions.append(f"test_{function_name}_detects_odd_number")

    else:
        suggestions.append(f"test_{function_name}_with_valid_input")
        suggestions.append(f"test_{function_name}_with_edge_input")
        suggestions.append(f"test_{function_name}_with_invalid_input")

    return suggestions


def build_ai_test_prompt(file_path, function):
    """
    Builds a prompt that can later be sent to an AI model for better test generation.
    """

    function_name = function["name"]
    arguments = ", ".join(function["arguments"])
    qualified_name = function.get("qualified_name", function_name)

    return (
        "Generate robust pytest tests for this Python function.\n"
        f"File: {file_path}\n"
        f"Function: {qualified_name}({arguments})\n"
        f"Line: {function['line_number']}\n"
        f"Argument count: {function['argument_count']}\n"
        f"Has division operation: {function.get('has_division', False)}\n"
        f"Is async: {function.get('is_async', False)}\n"
        "Include normal cases, edge cases, invalid inputs, and expected behavior."
    )


def generate_test_suggestions(scan_results):
    """
    Generates smarter test suggestions for each discovered function.

    The output remains compatible with the existing reporters.
    """

    suggestions = []

    for file_result in scan_results:
        file_path = file_result["file"]

        for function in file_result["functions"]:
            suggestion = {
                "file": file_path,
                "function": function["name"],
                "qualified_function": function.get("qualified_name", function["name"]),
                "parent_class": function.get("parent_class"),
                "arguments": function["arguments"],
                "argument_count": function["argument_count"],
                "line_number": function["line_number"],
                "is_async": function.get("is_async", False),
                "has_division": function.get("has_division", False),
                "suggested_tests": build_suggested_tests(function),
                "test_strategy": infer_test_strategy(function),
                "ai_test_prompt": build_ai_test_prompt(file_path, function),
            }

            suggestions.append(suggestion)

    return suggestions