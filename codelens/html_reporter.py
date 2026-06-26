from datetime import datetime
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


def get_status_class(status):
    """
    Returns a CSS class name for score status.
    """

    status = str(status).lower()

    if status in ["excellent", "good"]:
        return "status-good"

    if status in ["needs improvement", "poor"]:
        return "status-warning"

    if status == "critical":
        return "status-danger"

    return "status-warning"


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


def count_by_field(issues, field_name):
    """
    Counts issues by category, severity, or type.
    """

    counts = {}

    for issue in issues:
        value = issue.get(field_name, "Unknown")
        counts[value] = counts.get(value, 0) + 1

    return counts


def build_metric_card(label, value, helper_text=""):
    """
    Builds a dashboard metric card.
    """

    helper_html = ""

    if helper_text:
        helper_html = f"<p>{html_escape(helper_text)}</p>"

    return f"""
    <div class="metric-card">
        <span>{html_escape(label)}</span>
        <strong>{html_escape(value)}</strong>
        {helper_html}
    </div>
    """


def build_breakdown_bar(label, count, total):
    """
    Builds one horizontal bar for a breakdown chart.
    """

    if total <= 0:
        percentage = 0
    else:
        percentage = round((count / total) * 100, 1)

    return f"""
    <div class="breakdown-row">
        <div class="breakdown-label">
            <span>{html_escape(label)}</span>
            <strong>{html_escape(count)}</strong>
        </div>
        <div class="bar-track">
            <div class="bar-fill" style="width: {percentage}%"></div>
        </div>
        <div class="breakdown-percent">{percentage}%</div>
    </div>
    """


def build_breakdown_section(title, counts):
    """
    Builds a dashboard section with horizontal bars.
    """

    if not counts:
        return f"""
        <div class="dashboard-panel">
            <h3>{html_escape(title)}</h3>
            <p class="empty-message">No data available.</p>
        </div>
        """

    total = sum(counts.values())

    rows = []

    for label, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        rows.append(build_breakdown_bar(label, count, total))

    return f"""
    <div class="dashboard-panel">
        <h3>{html_escape(title)}</h3>
        {''.join(rows)}
    </div>
    """


def build_severity_badge(severity):
    """
    Builds a severity badge.
    """

    severity_class = get_severity_class(severity)

    return f"""
    <span class="severity-badge {severity_class}">
        {html_escape(severity)}
    </span>
    """


def build_issue_table(issues, table_id):
    """
    Builds a compact issue table.
    """

    if not issues:
        return "<p class='empty-message'>No issues found.</p>"

    rows = []

    for issue in issues:
        rows.append(
            f"""
            <tr>
                <td>{build_severity_badge(issue.get("severity", "Low"))}</td>
                <td>{html_escape(issue.get("category", ""))}</td>
                <td>{html_escape(issue.get("type", ""))}</td>
                <td><code>{html_escape(issue.get("file", ""))}</code></td>
                <td>{html_escape(issue.get("line", ""))}</td>
                <td>{html_escape(issue.get("message", ""))}</td>
                <td>{html_escape(issue.get("suggestion", ""))}</td>
            </tr>
            """
        )

    return f"""
    <div class="table-wrapper">
        <table id="{html_escape(table_id)}">
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Category</th>
                    <th>Type</th>
                    <th>File</th>
                    <th>Line</th>
                    <th>Message</th>
                    <th>Suggestion</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    """


def build_issue_cards(issues):
    """
    Builds detailed HTML cards for issues.
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
                <p><strong>Category:</strong> {html_escape(issue.get("category", ""))}</p>
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
        parse_error_html = ""

        if file_result.get("parse_error"):
            parse_error_html = f"""
            <div class="alert-box">
                Parse error: {html_escape(file_result.get("parse_error"))}
            </div>
            """

        if file_result["imports"]:
            imports_html = "".join(
                f"<li><code>{html_escape(item)}</code></li>"
                for item in file_result["imports"]
            )
        else:
            imports_html = "<li>None</li>"

        if file_result["functions"]:
            functions_html = ""

            for function in file_result["functions"]:
                arguments = ", ".join(function["arguments"])
                has_docstring = "Yes" if function["has_docstring"] else "No"
                has_division = "Yes" if function["has_division"] else "No"
                is_async = "Yes" if function.get("is_async") else "No"

                functions_html += f"""
                <div class="mini-card">
                    <h4><code>{html_escape(function["name"])}({html_escape(arguments)})</code></h4>
                    <div class="mini-grid">
                        <p><strong>Line:</strong> {html_escape(function["line_number"])}</p>
                        <p><strong>Lines:</strong> {html_escape(function["line_count"])}</p>
                        <p><strong>Arguments:</strong> {html_escape(function["argument_count"])}</p>
                        <p><strong>Docstring:</strong> {has_docstring}</p>
                        <p><strong>Uses division:</strong> {has_division}</p>
                        <p><strong>Async:</strong> {is_async}</p>
                    </div>
                </div>
                """
        else:
            functions_html = "<p class='empty-message'>No functions found.</p>"

        if file_result["classes"]:
            classes_html = ""

            for class_info in file_result["classes"]:
                has_docstring = "Yes" if class_info["has_docstring"] else "No"

                classes_html += f"""
                <div class="mini-card">
                    <h4><code>{html_escape(class_info["name"])}</code></h4>
                    <div class="mini-grid">
                        <p><strong>Line:</strong> {html_escape(class_info["line_number"])}</p>
                        <p><strong>Lines:</strong> {html_escape(class_info.get("line_count", ""))}</p>
                        <p><strong>Docstring:</strong> {has_docstring}</p>
                    </div>
                </div>
                """
        else:
            classes_html = "<p class='empty-message'>No classes found.</p>"

        sections.append(
            f"""
            <div class="file-card">
                <h3>{html_escape(file_result["file"])}</h3>
                {parse_error_html}

                <h4>Imports</h4>
                <ul class="import-list">
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


def build_navigation():
    """
    Builds dashboard navigation.
    """

    return """
    <nav class="top-nav">
        <a href="#summary">Summary</a>
        <a href="#score">Score</a>
        <a href="#breakdowns">Breakdowns</a>
        <a href="#all-issues">All Issues</a>
        <a href="#quality">Quality</a>
        <a href="#security">Security</a>
        <a href="#dependency">Dependency</a>
        <a href="#files">Files</a>
        <a href="#tests">Tests</a>
        <a href="#ai">AI</a>
    </nav>
    """


def build_styles():
    """
    Returns dashboard CSS.
    """

    return """
    :root {
        --bg: #f4f7fb;
        --card: #ffffff;
        --text: #111827;
        --muted: #6b7280;
        --border: #e5e7eb;
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --critical: #7f1d1d;
        --high: #dc2626;
        --medium: #f59e0b;
        --low: #2563eb;
        --good: #15803d;
        --warning: #b45309;
        --danger: #b91c1c;
        --shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    * {
        box-sizing: border-box;
    }

    html {
        scroll-behavior: smooth;
    }

    body {
        margin: 0;
        font-family: Arial, Helvetica, sans-serif;
        background: var(--bg);
        color: var(--text);
    }

    header {
        background: linear-gradient(135deg, #111827, #1e3a8a, #2563eb);
        color: white;
        padding: 42px 60px 34px;
    }

    header h1 {
        margin: 0;
        font-size: 44px;
        letter-spacing: -1px;
    }

    header p {
        margin-top: 12px;
        font-size: 17px;
        opacity: 0.95;
    }

    .top-nav {
        position: sticky;
        top: 0;
        z-index: 10;
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border);
        padding: 12px 24px;
        display: flex;
        gap: 10px;
        overflow-x: auto;
    }

    .top-nav a {
        color: var(--primary-dark);
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 999px;
        background: #eff6ff;
        white-space: nowrap;
    }

    .top-nav a:hover {
        background: #dbeafe;
    }

    main {
        max-width: 1280px;
        margin: 30px auto;
        padding: 0 20px 60px;
    }

    section {
        background: var(--card);
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 28px;
        box-shadow: var(--shadow);
        border: 1px solid rgba(229, 231, 235, 0.8);
    }

    h2 {
        margin-top: 0;
        border-bottom: 2px solid var(--border);
        padding-bottom: 12px;
        letter-spacing: -0.3px;
    }

    h3 {
        margin-top: 0;
    }

    code {
        background: #eef2ff;
        color: #1e40af;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 13px;
    }

    pre {
        background: #111827;
        color: #e5e7eb;
        padding: 18px;
        border-radius: 12px;
        overflow-x: auto;
        white-space: pre-wrap;
        line-height: 1.5;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
        gap: 16px;
    }

    .metric-card {
        background: linear-gradient(180deg, #ffffff, #f9fafb);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
    }

    .metric-card span {
        display: block;
        font-size: 14px;
        color: var(--muted);
        font-weight: 700;
    }

    .metric-card strong {
        display: block;
        margin-top: 8px;
        font-size: 30px;
        color: var(--text);
    }

    .metric-card p {
        margin-bottom: 0;
        color: var(--muted);
        font-size: 13px;
    }

    .score-layout {
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 24px;
        align-items: stretch;
    }

    .score-main {
        background: #111827;
        color: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .score-number {
        font-size: 62px;
        font-weight: 800;
        letter-spacing: -2px;
    }

    .score-grade {
        margin-top: 8px;
        font-size: 28px;
        font-weight: 800;
    }

    .score-status {
        display: inline-block;
        margin-top: 14px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.14);
        font-weight: 700;
    }

    .score-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 14px;
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 18px;
    }

    .dashboard-panel {
        border: 1px solid var(--border);
        background: #f9fafb;
        border-radius: 16px;
        padding: 20px;
    }

    .breakdown-row {
        margin-bottom: 14px;
    }

    .breakdown-label {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .bar-track {
        width: 100%;
        height: 10px;
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
    }

    .bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), #60a5fa);
        border-radius: 999px;
    }

    .breakdown-percent {
        margin-top: 4px;
        font-size: 12px;
        color: var(--muted);
        text-align: right;
    }

    .table-wrapper {
        overflow-x: auto;
        border: 1px solid var(--border);
        border-radius: 14px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        min-width: 920px;
        background: white;
    }

    th {
        background: #f3f4f6;
        color: #374151;
        text-align: left;
        padding: 13px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    td {
        padding: 13px;
        border-top: 1px solid var(--border);
        vertical-align: top;
        font-size: 14px;
    }

    .issue-card,
    .file-card,
    .mini-card {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 18px;
        background: #f9fafb;
    }

    .issue-header {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: center;
    }

    .severity-badge {
        color: white;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        display: inline-block;
    }

    .severity-critical {
        background: var(--critical);
    }

    .severity-high {
        background: var(--high);
    }

    .severity-medium {
        background: var(--medium);
    }

    .severity-low {
        background: var(--low);
    }

    .status-pass,
    .status-good {
        color: var(--good);
        font-weight: 800;
    }

    .status-fail,
    .status-danger {
        color: var(--danger);
        font-weight: 800;
    }

    .status-skip,
    .status-warning {
        color: var(--warning);
        font-weight: 800;
    }

    .empty-message {
        color: var(--muted);
        font-style: italic;
    }

    .alert-box {
        background: #fef2f2;
        color: #991b1b;
        border: 1px solid #fecaca;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 14px;
        font-weight: 700;
    }

    .mini-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 4px 16px;
    }

    .import-list {
        columns: 2;
    }

    footer {
        text-align: center;
        padding: 24px;
        color: var(--muted);
    }

    @media (max-width: 800px) {
        header {
            padding: 32px 24px;
        }

        header h1 {
            font-size: 34px;
        }

        .score-layout {
            grid-template-columns: 1fr;
        }

        section {
            padding: 22px;
        }

        .import-list {
            columns: 1;
        }
    }
    """


def generate_html_report(
    scan_results,
    code_quality_issues,
    security_issues,
    dependency_issues,
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
    Generates a browser-friendly HTML dashboard report.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_files = len(scan_results)
    total_imports = sum(len(file_result["imports"]) for file_result in scan_results)
    total_functions = sum(len(file_result["functions"]) for file_result in scan_results)
    total_classes = sum(len(file_result["classes"]) for file_result in scan_results)

    severity_counts = count_by_field(all_issues, "severity")
    category_counts = count_by_field(all_issues, "category")
    type_counts = count_by_field(all_issues, "type")

    generated_files_html = build_generated_files_html(
        generated_test_files,
        test_run_result,
    )

    test_status = get_test_status_label(test_run_result)
    test_status_class = get_test_status_class(test_run_result)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    styles = build_styles()
    navigation = build_navigation()

    score_status_class = get_status_class(code_score["status"])

    metric_cards = "".join(
        [
            build_metric_card("Files scanned", total_files),
            build_metric_card("Imports found", total_imports),
            build_metric_card("Functions found", total_functions),
            build_metric_card("Classes found", total_classes),
            build_metric_card("Total issues", len(all_issues)),
            build_metric_card("Code quality issues", len(code_quality_issues)),
            build_metric_card("Security issues", len(security_issues)),
            build_metric_card("Dependency issues", len(dependency_issues)),
            build_metric_card("Test suggestions", len(test_suggestions)),
            build_metric_card("Pytest files", len(generated_test_files)),
            build_metric_card("Test run", test_status),
        ]
    )

    score_detail_cards = "".join(
        [
            build_metric_card("Critical issues", code_score["issue_summary"]["Critical"]),
            build_metric_card("High issues", code_score["issue_summary"]["High"]),
            build_metric_card("Medium issues", code_score["issue_summary"]["Medium"]),
            build_metric_card("Low issues", code_score["issue_summary"]["Low"]),
            build_metric_card("Total issues", code_score["total_issues"]),
        ]
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodeLens AI Dashboard Report</title>
    <style>
        {styles}
    </style>
</head>
<body>
    <header>
        <h1>CodeLens AI Dashboard</h1>
        <p>Project analyzed: <strong>{html_escape(project_path)}</strong></p>
        <p>Generated at: <strong>{html_escape(generated_at)}</strong></p>
    </header>

    {navigation}

    <main>
        <section id="summary">
            <h2>Project Summary</h2>
            <div class="metric-grid">
                {metric_cards}
            </div>
        </section>

        <section id="score">
            <h2>Code Quality, Security, and Dependency Score</h2>
            <div class="score-layout">
                <div class="score-main">
                    <div class="score-number">{html_escape(code_score["score"])}/100</div>
                    <div class="score-grade">Grade {html_escape(code_score["grade"])}</div>
                    <div class="score-status {score_status_class}">
                        {html_escape(code_score["status"])}
                    </div>
                </div>

                <div class="score-details">
                    {score_detail_cards}
                </div>
            </div>
        </section>

        <section id="breakdowns">
            <h2>Issue Breakdowns</h2>
            <div class="dashboard-grid">
                {build_breakdown_section("By Severity", severity_counts)}
                {build_breakdown_section("By Category", category_counts)}
                {build_breakdown_section("By Issue Type", type_counts)}
            </div>
        </section>

        <section id="all-issues">
            <h2>All Issues</h2>
            {build_issue_table(all_issues, "all-issues-table")}
        </section>

        <section id="quality">
            <h2>Code Quality Issues</h2>
            {build_issue_cards(code_quality_issues)}
        </section>

        <section id="security">
            <h2>Security Issues</h2>
            {build_issue_cards(security_issues)}
        </section>

        <section id="dependency">
            <h2>Dependency Issues</h2>
            {build_issue_cards(dependency_issues)}
        </section>

        <section id="files">
            <h2>Detailed File Analysis</h2>
            {build_file_analysis(scan_results)}
        </section>

        <section id="tests">
            <h2>Test Suggestions</h2>
            {build_test_suggestions(test_suggestions)}

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

        <section id="ai">
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