def generate_test_suggestions(scan_results):
    """
    Generates simple pytest test suggestions for each function.
    """

    test_suggestions = []

    for file_result in scan_results:
        file_path = file_result["file"]

        for function in file_result["functions"]:
            function_name = function["name"]
            arguments = function["arguments"]

            suggested_tests = []

            # General test for every function
            suggested_tests.append(f"test_{function_name}_valid_input")

            # If function uses division, suggest division-by-zero test
            if function["has_division"]:
                suggested_tests.append(f"test_{function_name}_division_by_zero")

            # If function has many arguments, suggest boundary tests
            if function["argument_count"] > 4:
                suggested_tests.append(f"test_{function_name}_maximum_values")
                suggested_tests.append(f"test_{function_name}_minimum_values")
                suggested_tests.append(f"test_{function_name}_invalid_input")

            # Function-name based suggestions
            if "add" in function_name:
                suggested_tests.append(f"test_{function_name}_positive_numbers")
                suggested_tests.append(f"test_{function_name}_negative_numbers")

            if "subtract" in function_name:
                suggested_tests.append(f"test_{function_name}_positive_numbers")
                suggested_tests.append(f"test_{function_name}_negative_result")

            if "multiply" in function_name:
                suggested_tests.append(f"test_{function_name}_positive_numbers")
                suggested_tests.append(f"test_{function_name}_with_zero")

            # Remove duplicates while keeping order
            unique_tests = []
            for test in suggested_tests:
                if test not in unique_tests:
                    unique_tests.append(test)

            test_suggestions.append({
                "file": file_path,
                "function": function_name,
                "arguments": arguments,
                "suggested_tests": unique_tests,
            })

    return test_suggestions