"""Tests for configuration parser."""

import tempfile

import pytest

from ipwarn.config import Config, ConfigError


def test_config_parse(sample_config):
    """Test basic configuration parsing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
        for key, value in sample_config.items():
            f.write(f"{key}={value}\n")
        f.flush()

        config = Config(f.name)
        assert config.interval == 30
        assert config.ip_checkers == ["icanhazip.com", "ipify.org", "ifconfig.me"]
        assert config.update_telegram is True
        assert config.update_godaddy is True
        assert config.update_porkbun is True
        assert config.log_level == "INFO"


def test_config_bool_values():
    """Test boolean configuration values."""
    config_text = """
UPDATE_TELEGRAM=true
UPDATE_GODADDY=false
UPDATE_PORKBUN=true
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
        f.write(config_text)
        f.flush()

        config = Config(f.name)
        assert config.update_telegram is True
        assert config.update_godaddy is False
        assert config.update_porkbun is True


def test_config_with_comments_and_empty_lines():
    """Test parsing config with comments and empty lines."""
    config_text = """
# This is a comment
INTERVAL=60

# Another comment
UPDATE_TELEGRAM=false
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
        f.write(config_text)
        f.flush()

        config = Config(f.name)
        assert config.interval == 60
        assert config.update_telegram is False


def test_config_quoted_values():
    """Test parsing quoted values."""
    config_text = """
GD_RECORD_TYPE="A"
GD_DOMAIN='example.com'
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
        f.write(config_text)
        f.flush()

        config = Config(f.name)
        assert config.godaddy_record_type == "A"
        assert config.godaddy_domain == "example.com"


def test_config_file_not_found():
    """Test error when config file doesn't exist."""
    with pytest.raises(ConfigError, match="Config file not found"):
        Config("/nonexistent/path/ipwarn.conf")


def test_config_get_with_default():
    """Test getting values with defaults."""
    config_text = """
INTERVAL=30
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".conf") as f:
        f.write(config_text)
        f.flush()

        config = Config(f.name)
        assert config.get("NONEXISTENT_KEY", "default") == "default"
        assert config.get_bool("NONEXISTENT_BOOL", True) is True
        assert config.get_int("NONEXISTENT_INT", 42) == 42
