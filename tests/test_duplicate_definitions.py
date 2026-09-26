from codelens.analyzer import analyze_project
from codelens.scanner import scan_python_file


def scan_source(tmp_path, source):
    file_path = tmp_path / "module.py"
    file_path.write_text(source, encoding="utf-8")
    return scan_python_file(file_path)


def test_detects_duplicate_decorated_route(tmp_path):
    # The bug CodeLens missed in a real FastAPI project: the second route never runs
    result = scan_source(
        tmp_path,
        """
@router.get("/")
def get_tasks(db):
    return db.all()

@router.get("/")
def get_tasks(page, limit, db):
    return db.page(page, limit)
""",
    )

    issues = analyze_project([result])
    duplicate_issues = [issue for issue in issues if issue["type"] == "Duplicate Definition"]

    assert len(duplicate_issues) == 1
    assert duplicate_issues[0]["severity"] == "High"
    assert duplicate_issues[0]["line"] == 7
    assert "line 3" in duplicate_issues[0]["message"]


def test_detects_duplicate_method_and_class(tmp_path):
    result = scan_source(
        tmp_path,
        """
class Report:
    def render(self):
        pass

    def render(self):
        pass

class Report:
    pass
""",
    )

    duplicates = {(d["scope"], d["name"]) for d in result["duplicate_definitions"]}

    assert duplicates == {("Report", "render"), (None, "Report")}


def test_ignores_intentional_redefinitions(tmp_path):
    result = scan_source(
        tmp_path,
        """
from functools import singledispatch
from typing import overload

class Temperature:
    @property
    def celsius(self):
        return self._c

    @celsius.setter
    def celsius(self, value):
        self._c = value

    class Config:
        pass

class Other:
    class Config:
        pass

@overload
def parse(value: int) -> int: ...
@overload
def parse(value: str) -> str: ...
def parse(value):
    return value

@singledispatch
def show(value):
    pass

@show.register
def _(value: int):
    pass

@show.register
def _(value: str):
    pass

try:
    from fast import helper
except ImportError:
    def helper():
        pass
""",
    )

    assert result["duplicate_definitions"] == []
