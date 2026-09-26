from codelens.security_analyzer import analyze_config_secrets


def test_detects_hardcoded_secrets_in_yaml(tmp_path):
    (tmp_path / "docker-compose.yml").write_text(
        """
services:
  api:
    environment:
      - SECRET_KEY=your-secret-key-change-in-production
      - DATABASE_URL=sqlite:///./data/tasks.db
""",
        encoding="utf-8",
    )
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "deploy.yml").write_text(
        """
jobs:
  deploy:
    env:
      API_TOKEN: "a8f3kq29zx"  # copied from the dashboard
""",
        encoding="utf-8",
    )

    issues = analyze_config_secrets(tmp_path)

    flagged = sorted((issue["file"].replace("\\", "/").split("/")[-1], issue["line"]) for issue in issues)
    assert flagged == [("deploy.yml", 5), ("docker-compose.yml", 5)]
    assert all(issue["type"] == "Hardcoded Secret" and issue["severity"] == "High" for issue in issues)


def test_ignores_references_placeholders_and_keywords(tmp_path):
    (tmp_path / "ci.yml").write_text(
        """
permissions:
  id-token: write
jobs:
  test:
    secrets: inherit
    env:
      SECRET_KEY: ci-only-test-key
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
      PASSWORD_FILE: /run/secrets/db_password
    services:
      api:
        environment:
          - SECRET_KEY=${SECRET_KEY:?Set SECRET_KEY}
          - AUTH_TOKEN=$AUTH_TOKEN
          # - PASSWORD=hunter2hunter2
""",
        encoding="utf-8",
    )

    assert analyze_config_secrets(tmp_path) == []


def test_respects_ignored_folders_and_reads_utf16(tmp_path):
    ignored = tmp_path / "node_modules" / "pkg"
    ignored.mkdir(parents=True)
    (ignored / "config.yml").write_text("password: s3cr3t-value\n", encoding="utf-8")
    (tmp_path / "app.yaml").write_text("password: s3cr3t-value\n", encoding="utf-16")

    issues = analyze_config_secrets(tmp_path)

    assert [issue["file"].replace("\\", "/").split("/")[-1] for issue in issues] == ["app.yaml"]
