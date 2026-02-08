"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "INTERVAL": "30",
        "IP_CHECKERS": "icanhazip.com,ipify.org,ifconfig.me",
        "UPDATE_TELEGRAM": "true",
        "TEL_API_TOKEN": "test_token",
        "TEL_API_ID": "test_id",
        "UPDATE_GODADDY": "true",
        "GD_DOMAIN": "example.com",
        "GD_RECORD_NAME": "@",
        "GD_RECORD_TYPE": "A",
        "GD_API_KEY": "test_key",
        "GD_API_SECRET": "test_secret",
        "UPDATE_PORKBUN": "true",
        "PB_DOMAIN": "example.com",
        "PB_RECORD_NAME": "@",
        "PB_RECORD_TYPE": "A",
        "PB_API_KEY": "test_key",
        "PB_SECRET_API_KEY": "test_secret",
        "PB_TTL": "600",
        "LOG_LEVEL": "INFO",
    }
