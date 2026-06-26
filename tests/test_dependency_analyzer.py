from codelens.dependency_analyzer import analyze_dependency_issues


def test_dependency_analyzer_detects_requirements_issues(tmp_path):
    requirements_file = tmp_path / "requirements-test.txt"

    requirements_file.write_text(
        """
requests
flask>=2.0.0
http://example.com/package.tar.gz
""",
        encoding="utf-8",
    )

    issues = analyze_dependency_issues(
        tmp_path,
        rules_config={
            "check_dependencies": True,
            "dependency_file_patterns": ["requirements-test.txt"],
            "require_pinned_dependencies": True,
            "allow_http_dependencies": False,
            "allow_editable_installs": False,
        },
    )

    assert len(issues) >= 3

    combined_issue_text = " ".join(
        f"{issue.get('type', '')} {issue.get('message', '')}"
        for issue in issues
    ).lower()

    assert "unpinned" in combined_issue_text
    assert "loose" in combined_issue_text
    assert "http" in combined_issue_text


def test_dependency_analyzer_detects_missing_dependency_file(tmp_path):
    issues = analyze_dependency_issues(
        tmp_path,
        rules_config={
            "check_dependencies": True,
            "dependency_file_patterns": ["missing-test-requirements.txt"],
        },
    )

    assert len(issues) == 1
    assert issues[0]["category"] == "Dependency"

    combined_issue_text = (
        f"{issues[0].get('type', '')} {issues[0].get('message', '')}"
    ).lower()

    assert "missing" in combined_issue_text


def test_dependency_analyzer_can_disable_dependency_checks(tmp_path):
    issues = analyze_dependency_issues(
        tmp_path,
        rules_config={
            "check_dependencies": False,
        },
    )

    assert issues == []


def test_dependency_analyzer_reads_pyproject_dependencies(tmp_path):
    pyproject_file = tmp_path / "pyproject.toml"

    pyproject_file.write_text(
        """
[project]
dependencies = [
    "requests",
    "flask>=2.0.0"
]
""",
        encoding="utf-8",
    )

    issues = analyze_dependency_issues(
        tmp_path,
        rules_config={
            "check_dependencies": True,
            "dependency_file_patterns": ["pyproject.toml"],
            "require_pinned_dependencies": True,
        },
    )

    assert len(issues) >= 2

    combined_issue_text = " ".join(
        f"{issue.get('type', '')} {issue.get('message', '')}"
        for issue in issues
    ).lower()

    assert "unpinned" in combined_issue_text
    assert "loose" in combined_issue_text