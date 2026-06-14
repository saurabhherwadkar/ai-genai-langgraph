"""Unit tests for the configuration loader module."""

import os  # OS interface for environment variable manipulation
import tempfile  # Temporary file creation for test fixtures
from pathlib import Path  # Filesystem path handling

import pytest  # Test framework
import yaml  # YAML serialization for test fixtures

from src.utils.config_loader import load_settings  # Module under test


class TestLoadSettings:
    """Test suite for the load_settings function."""

    def test_load_default_settings_file(self) -> None:
        """Verify that the default settings file loads successfully."""
        # Load settings from the default project location
        settings = load_settings()

        # Assert that settings is a non-empty dictionary
        assert isinstance(settings, dict)
        assert len(settings) > 0

    def test_load_settings_contains_app_section(self) -> None:
        """Verify that the loaded settings contain the app section."""
        # Load settings from default location
        settings = load_settings()

        # Assert the app section exists with required keys
        assert "app" in settings
        assert "name" in settings["app"]

    def test_load_settings_contains_logging_section(self) -> None:
        """Verify that the loaded settings contain logging configuration."""
        # Load settings from default location
        settings = load_settings()

        # Assert logging section exists
        assert "logging" in settings
        assert "level" in settings["logging"]

    def test_load_settings_from_custom_path(self, tmp_path: Path) -> None:
        """Verify loading settings from a custom file path."""
        # Create a temporary YAML configuration file
        custom_config = {"app": {"name": "test-app", "version": "0.1.0"}}
        config_file = tmp_path / "custom_settings.yaml"
        config_file.write_text(yaml.dump(custom_config))

        # Load settings from the custom path
        settings = load_settings(str(config_file))

        # Assert the custom settings were loaded correctly
        assert settings["app"]["name"] == "test-app"
        assert settings["app"]["version"] == "0.1.0"

    def test_load_settings_file_not_found(self) -> None:
        """Verify FileNotFoundError is raised for missing config file."""
        # Attempt to load from a non-existent path
        with pytest.raises(FileNotFoundError):
            load_settings("/nonexistent/path/settings.yaml")

    def test_load_settings_empty_file(self, tmp_path: Path) -> None:
        """Verify that an empty config file returns an empty dict."""
        # Create an empty YAML file
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")

        # Load settings from the empty file
        settings = load_settings(str(empty_file))

        # Assert empty dictionary is returned
        assert settings == {}

    def test_load_settings_from_env_variable(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify loading settings from CONFIG_PATH environment variable."""
        # Create a test configuration file
        env_config = {"app": {"name": "env-app"}}
        config_file = tmp_path / "env_settings.yaml"
        config_file.write_text(yaml.dump(env_config))

        # Set the CONFIG_PATH environment variable
        monkeypatch.setenv("CONFIG_PATH", str(config_file))

        # Load settings without explicit path (should use env var)
        settings = load_settings()

        # Assert settings from env var path were loaded
        assert settings["app"]["name"] == "env-app"
