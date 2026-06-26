from html import escape
from pathlib import Path


def html_escape(value):
    """
    Safely converts a value to escaped HTML text.
    """

    if value is None:
        return ""

    return escape(str(value))


def get_severity_class(severity):
    """
    Returns a CSS class name for issue severity.
    """

    severity = str(severity).lower()

    if severity == "critical":
        return "severity-critical"

    if severity == "high":
        return "severity-high"

    if severity == "medium":
        return "severity-medium"

    if severity == "low":
        return "severity-low"

    return "severity-low"


def get_test_status_label(test_run_result):
    """
    Returns a readable test status.
    """

    if test_run_result.get("skipped"):
        return "Skipped"

    if test_run_result.get("passed"):
        return "Passed"

    return "Failed"


def get_test_status_class(test_run_result):
    """
    Returns CSS class for test status.
    """

    if test_run_result.get("skipped"):
        return "status-skip"

    if test_run_result.get("passed"):
        return "status-pass"

    return "status-fail"


def build_issue_cards(issues):
    """
    Builds HTML cards for code quality or security issues.
    """

    if not issues:
        return "<p class='empty-message'>No issues found.</p>"

    cards = []

    for issue in issues:
        severity = html_escape(issue.get("severity", "Low"))
        severity_class = get_severity_class(severity)

        cards.append(
            f"""
            <div class="issue-card">
                <div class="issue-header">
                    <h3>{html_escape(issue.get("type", "Issue"))}</h3>
                    <span class="severity-badge {severity_class}">{severity}</span>
                </div>
                <p><strong>File:</strong> <code>{html_escape(issue.get("file", ""))}</code></p>
                <p><strong>Line:</strong> {html_escape(issue.get("line", ""))}</p>
                <p><strong>Message:</strong> {html_escape(issue.get("message", ""))}</p>
                <p><strong>Suggestion:</strong> {html_escape(issue.get("suggestion", ""))}</p>
            </div>
            """
        )

    return "\n".join(cards)


def build_file_analysis(scan_results):
    """
    Builds HTML for detailed file analysis.
    """

    if not scan_results:
        return "<p class='empty-message'>No files scanned.</p>"

    sections = []

    for file_result in scan_results:
        imports_html = ""

        if file_result["imports"]:
            imports_html = "".join(
                f"<li><code>{html_escape(item)}</code></li>"
                for item in file_result["imports"]
            )
        else:
            imports_html = "<li>None</li>"

        functions_html = ""

        if file_result["functions"]:
            for function in file_result["functions"]:
                arguments = ", ".join(function["arguments"])
                has_docstring = "Yes" if function["has_docstring"] else "No"
                has_division = "Yes" if function["has_division"] else "No"

                functions_html += f"""
                <div class="mini-card">
                    <h4><code>{html_escape(function["name"])}({html_escape(arguments)})</code></h4>
                    <p><strong>Line:</strong> {html_escape(function["line_number"])}</p>
                    <p><strong>Lines of code:</strong> {html_escape(function["line_count"])}</p>
                    <p><strong>Arguments count:</strong> {html_escape(function["argument_count"])}</p>
                    <p><strong>Docstring:</strong> {has_docstring}</p>
                    <p><strong>Uses division:</strong> {has_division}</p>
                </div>
                """
        else:
            functions_html = "<p class='empty-message'>No functions found.</p>"

        classes_html = ""

        if file_result["classes"]:
            for class_info in file_result["classes"]:
                has_docstring = "Yes" if class_info["has_docstring"] else "No"

                classes_html += f"""
                <div class="mini-card">
                    <h4><code>{html_escape(class_info["name"])}</code></h4>
                    <p><strong>Line:</strong> {html_escape(class_info["line_number"])}</p>
                    <p><strong>Docstring:</strong> {has_docstring}</p>
                </div>
                """
        else:
            classes_html = "<p class='empty-message'>No classes found.</p>"

        sections.append(
            f"""
            <div class="file-card">
                <h3>{html_escape(file_result["file"])}</h3>

                <h4>Imports</h4>
                <ul>
                    {imports_html}
                </ul>

                <h4>Functions</h4>
                {functions_html}

                <h4>Classes</h4>
                {classes_html}
            </div>
            """
        )

    return "\n".join(sections)


def build_test_suggestions(test_suggestions):
    """
    Builds HTML for generated test suggestions.
    """

    if not test_suggestions:
        return "<p class='empty-message'>No test suggestions generated.</p>"

    sections = []

    for suggestion in test_suggestions:
        arguments = ", ".join(suggestion["arguments"])

        tests_html = "".join(
            f"<li><code>{html_escape(test)}</code></li>"
            for test in suggestion["suggested_tests"]
        )

        sections.append(
            f"""
            <div class="mini-card">
                <h3><code>{html_escape(suggestion["function"])}({html_escape(arguments)})</code></h3>
                <p><strong>File:</strong> <code>{html_escape(suggestion["file"])}</code></p>
                <ul>
                    {tests_html}
                </ul>
            </div>
            """
        )

    return "\n".join(sections)


def build_generated_files_html(generated_test_files, test_run_result):
    """
    Builds HTML for generated pytest files.
    """

    if test_run_result.get("skipped"):
        return "<li>Test generation and pytest execution were skipped.</li>"

    if generated_test_files:
        return "".join(
            f"<li><code>{html_escape(file_path)}</code></li>"
            for file_path in generated_test_files
        )

    return "<li>No pytest files generated.</li>"


def generate_html_report(
    scan_results,
    code_quality_issues,
    security_issues,
    all_issues,
    test_suggestions,
    generated_test_files,
    test_run_result,
    ai_explanation,
    code_score,
    project_path,
    output_path="reports/codelens_report.html",
):
    """
    Generates a browser-friendly HTML report.

    The HTML report is useful for:
    - Project demos
    - Faculty mentor presentation
    - Browser viewing
    - Future dashboard design
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    generated_files_html = build_generated_files_html(
        generated_test_files,
        test_run_result,
    )

    test_status = get_test_status_label(test_run_result)
    test_status_class = get_test_status_class(test_run_result)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeLens AI Report</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #f4f6f8;
            color: #1f2937;
        }}

        header {{
            background: linear-gradient(135deg, #111827, #2563eb);
            color: white;
            padding: 40px 60px;
        }}

        header h1 {{
            margin: 0;
            font-size: 42px;
        }}

        header p {{
            margin-top: 10px;
            font-size: 18px;
            opacity: 0.95;
        }}

        main {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px 50px;
        }}

        section {{
            background: white;
            border-radius: 14px;
            padding: 28px;
            margin-bottom: 28px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }}

        h2 {{
            margin-top: 0;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }}

        h3 {{
            margin-bottom: 8px;
        }}

        code {{
            background: #eef2ff;
            color: #1e40af;
            padding: 2px 6px;
            border-radius: 5px;
        }}

        pre {{
            background: #111827;
            color: #e5e7eb;
            padding: 18px;
            border-radius: 10px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 16px;
        }}

        .summary-card {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 18px;
        }}

        .summary-card span {{
            display: block;
            font-size: 14px;
            color: #6b7280;
        }}

        .summary-card strong {{
            display: block;
            margin-top: 8px;
            font-size: 28px;
            color: #111827;
        }}

        .score-box {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: center;
        }}

        .score-main {{
            background: #111827;
            color: white;
            border-radius: 18px;
            padding: 28px;
            min-width: 220px;
            text-align: center;
        }}

        .score-main .score {{
            font-size: 52px;
            font-weight: bold;
        }}

        .score-main .grade {{
            font-size: 24px;
            margin-top: 8px;
        }}

        .score-details {{
            flex: 1;
            min-width: 240px;
        }}

        .issue-card,
        .file-card,
        .mini-card {{
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 18px;
            background: #f9fafb;
        }}

        .issue-header {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
        }}

        .severity-badge {{
            color: white;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: bold;
        }}

        .severity-critical {{
            background: #7f1d1d;
        }}

        .severity-high {{
            background: #dc2626;
        }}

        .severity-medium {{
            background: #f59e0b;
        }}

        .severity-low {{
            background: #2563eb;
        }}

        .status-pass {{
            color: #15803d;
            font-weight: bold;
        }}

        .status-fail {{
            color: #dc2626;
            font-weight: bold;
        }}

        .status-skip {{
            color: #92400e;
            font-weight: bold;
        }}

        .empty-message {{
            color: #6b7280;
            font-style: italic;
        }}

        footer {{
            text-align: center;
            padding: 24px;
            color: #6b7280;
        }}
    </style>
</head>
<body>
    <header>
        <h1>CodeLens AI Report</h1>
        <p>Project analyzed: <strong>{html_escape(project_path)}</strong></p>
    </header>

    <main>
        <section>
            <h2>Project Summary</h2>
            <div class="summary-grid">
                <div class="summary-card"><span>Files scanned</span><strong>{total_files}</strong></div>
                <div class="summary-card"><span>Imports found</span><strong>{total_imports}</strong></div>
                <div class="summary-card"><span>Functions found</span><strong>{total_functions}</strong></div>
                <div class="summary-card"><span>Classes found</span><strong>{total_classes}</strong></div>
                <div class="summary-card"><span>Total issues</span><strong>{len(all_issues)}</strong></div>
                <div class="summary-card"><span>Code quality issues</span><strong>{len(code_quality_issues)}</strong></div>
                <div class="summary-card"><span>Security issues</span><strong>{len(security_issues)}</strong></div>
                <div class="summary-card"><span>Test suggestions</span><strong>{len(test_suggestions)}</strong></div>
                <div class="summary-card"><span>Pytest files</span><strong>{len(generated_test_files)}</strong></div>
                <div class="summary-card"><span>Test run</span><strong class="{test_status_class}">{test_status}</strong></div>
            </div>
        </section>

        <section>
            <h2>Code Quality and Security Score</h2>
            <div class="score-box">
                <div class="score-main">
                    <div class="score">{html_escape(code_score["score"])}/100</div>
                    <div class="grade">Grade {html_escape(code_score["grade"])}</div>
                    <div>{html_escape(code_score["status"])}</div>
                </div>
                <div class="score-details">
                    <p><strong>Critical issues:</strong> {html_escape(code_score["issue_summary"]["Critical"])}</p>
                    <p><strong>High issues:</strong> {html_escape(code_score["issue_summary"]["High"])}</p>
                    <p><strong>Medium issues:</strong> {html_escape(code_score["issue_summary"]["Medium"])}</p>
                    <p><strong>Low issues:</strong> {html_escape(code_score["issue_summary"]["Low"])}</p>
                    <p><strong>Total issues:</strong> {html_escape(code_score["total_issues"])}</p>
                </div>
            </div>
        </section>

        <section>
            <h2>Code Quality Issues</h2>
            {build_issue_cards(code_quality_issues)}
        </section>

        <section>
            <h2>Security Issues</h2>
            {build_issue_cards(security_issues)}
        </section>

        <section>
            <h2>Detailed File Analysis</h2>
            {build_file_analysis(scan_results)}
        </section>

        <section>
            <h2>Test Suggestions</h2>
            {build_test_suggestions(test_suggestions)}
        </section>

        <section>
            <h2>Generated Pytest Files</h2>
            <ul>
                {generated_files_html}
            </ul>

            <h3>Pytest Result</h3>
            <p><strong>Status:</strong> <span class="{test_status_class}">{test_status}</span></p>
            <p><strong>Command:</strong> <code>{html_escape(test_run_result.get("command", ""))}</code></p>
            <p><strong>Return code:</strong> {html_escape(test_run_result.get("return_code", ""))}</p>

            <h3>Pytest Output</h3>
            <pre>{html_escape(test_run_result.get("stdout", ""))}</pre>

            <h3>Pytest Errors</h3>
            <pre>{html_escape(test_run_result.get("stderr", ""))}</pre>
        </section>

        <section>
            <h2>AI Codebase Explanation</h2>
            <pre>{html_escape(ai_explanation)}</pre>
        </section>
    </main>

    <footer>
        Generated by CodeLens AI
    </footer>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    return str(output_path)