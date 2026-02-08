"""Tests for DNS providers."""

import pytest

from ipwarn.dns_providers.base import BaseDNSProvider, DNSProviderError
from ipwarn.dns_providers.godaddy import GoDaddyProvider
from ipwarn.dns_providers.porkbun import PorkbunProvider


def test_godaddy_provider_validation():
    """Test GoDaddy provider configuration validation."""
    with pytest.raises(DNSProviderError, match="API key is required"):
        GoDaddyProvider(api_key="", api_secret="secret")

    with pytest.raises(DNSProviderError, match="API secret is required"):
        GoDaddyProvider(api_key="key", api_secret="")


def test_godaddy_provider_valid():
    """Test GoDaddy provider with valid configuration."""
    provider = GoDaddyProvider(api_key="test_key", api_secret="test_secret")
    assert provider.config["api_key"] == "test_key"
    assert provider.config["api_secret"] == "test_secret"


def test_porkbun_provider_validation():
    """Test Porkbun provider configuration validation."""
    with pytest.raises(DNSProviderError, match="API key is required"):
        PorkbunProvider(api_key="", secret_api_key="secret")

    with pytest.raises(DNSProviderError, match="secret API key is required"):
        PorkbunProvider(api_key="key", secret_api_key="")


def test_porkbun_provider_valid():
    """Test Porkbun provider with valid configuration."""
    provider = PorkbunProvider(api_key="test_key", secret_api_key="test_secret")
    assert provider.config["api_key"] == "test_key"
    assert provider.config["secret_api_key"] == "test_secret"
    assert provider.config["ttl"] == 600


def test_porkbun_provider_custom_ttl():
    """Test Porkbun provider with custom TTL."""
    provider = PorkbunProvider(api_key="test_key", secret_api_key="test_secret", ttl=300)
    assert provider.config["ttl"] == 300


def test_base_provider_needs_update():
    """Test base provider needs_update method."""
    class MockProvider(BaseDNSProvider):
        def _validate_config(self):
            pass

        def get_current_ip(self, domain, record_name, record_type):
            return "192.168.1.1"

        def update_ip(self, domain, record_name, record_type, ip):
            return True

    provider = MockProvider({})
    assert provider.needs_update("example.com", "@", "A", "192.168.1.2") is True
    assert provider.needs_update("example.com", "@", "A", "192.168.1.1") is False
