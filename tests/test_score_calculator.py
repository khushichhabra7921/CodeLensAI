from codelens.score_calculator import calculate_code_score


def make_issues(severity, count):
    return [{"severity": severity} for _ in range(count)]


def test_many_low_issues_are_capped():
    result = calculate_code_score([], make_issues("Low", 35))

    assert result["score"] == 80
    assert result["issue_summary"]["Low"] == 35
    assert result["total_issues"] == 35


def test_medium_issues_are_capped():
    assert calculate_code_score([], make_issues("Medium", 10))["score"] == 70


def test_high_and_critical_issues_are_not_capped():
    assert calculate_code_score([], make_issues("High", 4))["score"] == 40
    assert calculate_code_score([], make_issues("Critical", 6))["score"] == 0


def test_single_vulnerability_outweighs_style_issues():
    style_only = calculate_code_score([], make_issues("Low", 35))
    with_vulnerability = calculate_code_score([], make_issues("Low", 35) + make_issues("High", 1))

    assert with_vulnerability["score"] == style_only["score"] - 15
