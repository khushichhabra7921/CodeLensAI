import os

from dotenv import load_dotenv

load_dotenv()


def create_fallback_explanation(scan_results, issues, test_suggestions):
    """
    Creates a basic explanation if the API key is missing or the AI call fails.
    """

    total_files = len(scan_results)
    total_functions = sum(len(file["functions"]) for file in scan_results)
    total_classes = sum(len(file["classes"]) for file in scan_results)

    high_issues = [
        issue for issue in issues
        if issue["severity"] == "High"
    ]

    explanation = []

    explanation.append("This Python project was analyzed by CodeLens AI.")
    explanation.append(
        f"It contains {total_files} file(s), {total_functions} function(s), "
        f"and {total_classes} class(es)."
    )

    if issues:
        explanation.append(
            f"The analyzer found {len(issues)} code quality issue(s)."
        )
    else:
        explanation.append("No major code quality issues were found.")

    if high_issues:
        explanation.append(
            "There are high-severity issues that should be fixed first."
        )

    if test_suggestions:
        explanation.append(
            f"CodeLens AI generated test suggestions for {len(test_suggestions)} function(s)."
        )

    explanation.append(
        "Overall, the project would benefit from better documentation, stronger edge-case handling, and more automated tests."
    )

    return "\n".join(explanation)


def build_prompt(scan_results, issues, test_suggestions):
    """
    Builds a prompt for the LLM using scanner and analyzer results.
    """

    summary_lines = []

    for file_result in scan_results:
        summary_lines.append(f"File: {file_result['file']}")

        summary_lines.append("Functions:")
        for function in file_result["functions"]:
            summary_lines.append(
                f"- {function['name']}({', '.join(function['arguments'])}), "
                f"line {function['line_number']}, "
                f"docstring={function['has_docstring']}, "
                f"uses_division={function['has_division']}, "
                f"arguments_count={function['argument_count']}, "
                f"line_count={function['line_count']}"
            )

        summary_lines.append("Classes:")
        for class_info in file_result["classes"]:
            summary_lines.append(
                f"- {class_info['name']}, "
                f"line {class_info['line_number']}, "
                f"docstring={class_info['has_docstring']}"
            )

        summary_lines.append("")

    issue_lines = []

    for issue in issues:
        issue_lines.append(
            f"- {issue['type']} | {issue['severity']} | "
            f"{issue['message']} | Suggestion: {issue['suggestion']}"
        )

    test_lines = []

    for suggestion in test_suggestions:
        test_lines.append(
            f"- {suggestion['function']} should have tests: "
            f"{', '.join(suggestion['suggested_tests'])}"
        )

    prompt = f"""
You are CodeLens AI, an assistant that explains Python codebases to software developers.

Explain this codebase in simple, clear language.

Your explanation should include:
1. What the project seems to do
2. Important functions/classes
3. Main code quality issues
4. Which issues should be fixed first
5. What tests should be added
6. A short overall recommendation

Keep the explanation beginner-friendly but professional.

Codebase summary:
{chr(10).join(summary_lines)}

Issues found:
{chr(10).join(issue_lines) if issue_lines else "No issues found."}

Test suggestions:
{chr(10).join(test_lines) if test_lines else "No test suggestions generated."}
"""

    return prompt


def generate_ai_explanation(scan_results, issues, test_suggestions):
    """
    Generates an AI explanation using Groq.
    If something fails, it returns a fallback explanation.
    """

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        return create_fallback_explanation(
            scan_results,
            issues,
            test_suggestions
        )

    try:
        from groq import Groq

        client = Groq(api_key=api_key)

        prompt = build_prompt(scan_results, issues, test_suggestions)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful senior software engineer explaining code quality reports."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as error:
        fallback = create_fallback_explanation(
            scan_results,
            issues,
            test_suggestions
        )

        return (
            fallback
            + "\n\nNote: AI explanation fallback was used because the LLM request failed."
            + f"\nError: {error}"
        )