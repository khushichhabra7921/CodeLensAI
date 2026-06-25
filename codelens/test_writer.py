from pathlib import Path


def generate_pytest_files(scan_results, output_dir="generated_tests"):
    """
    Generates actual pytest test files for scanned Python files.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for file_result in scan_results:
        source_file = Path(file_result["file"])
        test_file_name = f"test_{source_file.stem}_generated.py"
        test_file_path = output_dir / test_file_name

        lines = []

        lines.append("from pathlib import Path")
        lines.append("import importlib.util")
        lines.append("import pytest")
        lines.append("")
        lines.append("")
        lines.append("ROOT_DIR = Path(__file__).resolve().parents[1]")
        lines.append(f'SOURCE_FILE = ROOT_DIR / Path("{source_file.as_posix()}")')
        lines.append("")
        lines.append("")
        lines.append("spec = importlib.util.spec_from_file_location('target_module', SOURCE_FILE)")
        lines.append("module = importlib.util.module_from_spec(spec)")
        lines.append("spec.loader.exec_module(module)")
        lines.append("")

        for function in file_result["functions"]:
            function_name = function["name"]
            arguments = function["arguments"]

            # Skip class methods for now, like multiply(self, a, b)
            # We will handle class methods later.
            if arguments and arguments[0] in ["self", "cls"]:
                continue

            if function_name == "add":
                lines.append("")
                lines.append("")
                lines.append("def test_add_valid_input():")
                lines.append("    assert module.add(2, 3) == 5")

            elif function_name == "subtract":
                lines.append("")
                lines.append("")
                lines.append("def test_subtract_valid_input():")
                lines.append("    assert module.subtract(5, 3) == 2")

            elif function_name == "divide":
                lines.append("")
                lines.append("")
                lines.append("def test_divide_valid_input():")
                lines.append("    assert module.divide(10, 2) == 5")
                lines.append("")
                lines.append("")
                lines.append("def test_divide_by_zero():")
                lines.append("    with pytest.raises(ZeroDivisionError):")
                lines.append("        module.divide(10, 0)")

            elif function_name == "calculate_final_score":
                lines.append("")
                lines.append("")
                lines.append("def test_calculate_final_score_maximum_cap():")
                lines.append("    assert module.calculate_final_score(20, 30, 40, 50, 10) == 100")
                lines.append("")
                lines.append("")
                lines.append("def test_calculate_final_score_minimum_cap():")
                lines.append("    assert module.calculate_final_score(-10, -20, -30, -40, -50) == 0")
                lines.append("")
                lines.append("")
                lines.append("def test_calculate_final_score_valid_input():")
                lines.append("    assert module.calculate_final_score(10, 20, 30, 25, 5) == 90")

            else:
                lines.append("")
                lines.append("")
                lines.append(f"def test_{function_name}_exists():")
                lines.append(f'    assert hasattr(module, "{function_name}")')
                lines.append(f"    assert callable(module.{function_name})")

        test_content = "\n".join(lines)

        with open(test_file_path, "w", encoding="utf-8") as file:
            file.write(test_content)

        generated_files.append(str(test_file_path))

    return generated_files