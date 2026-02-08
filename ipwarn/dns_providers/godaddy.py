"""GoDaddy DNS provider implementation."""

import logging
from typing import Any, Dict

import requests

from ipwarn.dns_providers.base import BaseDNSProvider, DNSProviderError

logger = logging.getLogger(__name__)


class GoDaddyProvider(BaseDNSProvider):
    """GoDaddy DNS provider."""

    BASE_URL = "https://api.godaddy.com/v1"

    def __init__(self, api_key: str, api_secret: str):
        """Initialize GoDaddy provider.

        Args:
            api_key: GoDaddy API key.
            api_secret: GoDaddy API secret.
        """
        config = {
            "api_key": api_key,
            "api_secret": api_secret,
        }
        super().__init__(config)

    def _validate_config(self) -> None:
        """Validate GoDaddy configuration.

        Raises:
            DNSProviderError: If configuration is invalid.
        """
        if not self.config.get("api_key"):
            raise DNSProviderError("GoDaddy API key is required")
        if not self.config.get("api_secret"):
            raise DNSProviderError("GoDaddy API secret is required")

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication.

        Returns:
            Dictionary of headers.
        """
        return {
            "Authorization": f"sso-key {self.config['api_key']}:{self.config['api_secret']}",
            "Content-Type": "application/json",
        }

    def get_current_ip(self, domain: str, record_name: str, record_type: str) -> str:
        """Get current IP address for a DNS record.

        Args:
            domain: Domain name.
            record_name: Record name (e.g., '@' for root, 'www' for subdomain).
            record_type: Record type (e.g., 'A', 'AAAA').

        Returns:
            Current IP address.

        Raises:
            DNSProviderError: If unable to retrieve current IP.
        """
        url = f"{self.BASE_URL}/domains/{domain}/records/{record_type}/{record_name}"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()

            records = response.json()

            if not records:
                raise DNSProviderError(f"No {record_type} record found for {record_name}.{domain}")

            return records[0]["data"]

        except requests.exceptions.RequestException as e:
            raise DNSProviderError(f"Failed to get current IP from GoDaddy: {e}")

    def update_ip(self, domain: str, record_name: str, record_type: str, ip: str) -> bool:
        """Update IP address for a DNS record.

        Args:
            domain: Domain name.
            record_name: Record name (e.g., '@' for root, 'www' for subdomain).
            record_type: Record type (e.g., 'A', 'AAAA').
            ip: New IP address.

        Returns:
            True if update was successful, False otherwise.

        Raises:
            DNSProviderError: If update fails.
        """
        url = f"{self.BASE_URL}/domains/{domain}/records/{record_type}/{record_name}"

        data = [{"data": ip}]

        try:
            response = requests.put(url, headers=self._get_headers(), json=data, timeout=10)
            response.raise_for_status()

            logger.info(f"GoDaddy record updated: {record_name}.{domain} -> {ip}")
            return True

        except requests.exceptions.RequestException as e:
            raise DNSProviderError(f"Failed to update IP on GoDaddy: {e}")
