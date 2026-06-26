from pathlib import Path
import copy

try:
    import yaml
except ImportError:
    yaml = None


DEFAULT_CONFIG = {
    "project": {
        "default_path": "sample_projects/calculator_app",
    },
    "reports": {
        "format": "all",
        "output_dir": "reports",
    },
    "analysis": {
        "skip_ai": False,
        "skip_tests": False,
        "track_history": True,
        "track_issue_trends": True,
    },
    "rules": {
        "max_function_lines": 30,
        "max_arguments": 5,
        "check_security": True,
        "allow_http_urls": False,
        "check_dependencies": True,
        "require_pinned_dependencies": True,
        "allow_editable_installs": False,
        "allow_http_dependencies": False,
    },
    "ignore": {
        "folders": [
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "generated_tests",
            "reports",
            "node_modules",
            "dist",
            "build",
        ],
        "files": [],
    },
}


def deep_merge(default_config, user_config):
    """
    Recursively merges user config into default config.

    Values from user_config override values from default_config.
    """

    merged = copy.deepcopy(default_config)

    for key, value in user_config.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value

    return merged


def load_yaml_file(config_path):
    """
    Loads a YAML config file.
    """

    config_path = Path(config_path)

    if not config_path.exists():
        return {}

    if yaml is None:
        raise ImportError(
            "PyYAML is required for config file support. "
            "Install it using: python -m pip install PyYAML"
        )

    with open(config_path, "r", encoding="utf-8") as file:
        loaded_config = yaml.safe_load(file)

    if loaded_config is None:
        return {}

    if not isinstance(loaded_config, dict):
        raise ValueError("Config file must contain a YAML dictionary/object.")

    return loaded_config


def load_config(config_path="codelens.yml"):
    """
    Loads CodeLens AI config.

    If the config file does not exist, default config is used.
    """

    config_path = Path(config_path)

    user_config = load_yaml_file(config_path)

    return deep_merge(DEFAULT_CONFIG, user_config)


def get_config_value(config, section, key, default=None):
    """
    Safely gets a config value.
    """

    return config.get(section, {}).get(key, default)


def normalize_report_format(report_format):
    """
    Normalizes report format aliases.
    """

    if report_format == "md":
        return "markdown"

    return report_format


def validate_list_config(config, section, key):
    """
    Validates that a config value is a list.
    """

    value = get_config_value(config, section, key, [])

    if value is None:
        return True

    if not isinstance(value, list):
        raise ValueError(f"{section}.{key} must be a list.")

    return True


def validate_config(config):
    """
    Validates important config values.
    """

    valid_formats = {"all", "markdown", "md", "json", "html"}

    report_format = get_config_value(config, "reports", "format", "all")

    if report_format not in valid_formats:
        raise ValueError(
            "Invalid reports.format in codelens.yml. "
            "Allowed values: all, markdown, md, json, html"
        )

    max_function_lines = get_config_value(
        config,
        "rules",
        "max_function_lines",
        30,
    )

    max_arguments = get_config_value(
        config,
        "rules",
        "max_arguments",
        5,
    )

    if not isinstance(max_function_lines, int) or max_function_lines <= 0:
        raise ValueError("rules.max_function_lines must be a positive integer.")

    if not isinstance(max_arguments, int) or max_arguments <= 0:
        raise ValueError("rules.max_arguments must be a positive integer.")

    validate_list_config(config, "ignore", "folders")
    validate_list_config(config, "ignore", "files")

    return True