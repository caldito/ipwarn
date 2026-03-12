"""Porkbun DNS provider implementation."""

import logging

import requests

from ipwarn.dns_providers.base import BaseDNSProvider, DNSProviderError

logger = logging.getLogger(__name__)


class PorkbunProvider(BaseDNSProvider):
    """Porkbun DNS provider."""

    BASE_URL = "https://api.porkbun.com/api/json/v3"

    def __init__(self, api_key: str, secret_api_key: str, ttl: int = 600):
        """Initialize Porkbun provider.

        Args:
            api_key: Porkbun API key.
            secret_api_key: Porkbun secret API key.
            ttl: Time to live for DNS records (default: 600).
        """
        config = {
            "api_key": api_key,
            "secret_api_key": secret_api_key,
            "ttl": ttl,
        }
        super().__init__(config)

    def _validate_config(self) -> None:
        """Validate Porkbun configuration.

        Raises:
            DNSProviderError: If configuration is invalid.
        """
        if not self.config.get("api_key"):
            raise DNSProviderError("Porkbun API key is required")
        if not self.config.get("secret_api_key"):
            raise DNSProviderError("Porkbun secret API key is required")

    def _get_auth_payload(self) -> dict[str, str]:
        """Get authentication payload for requests.

        Returns:
            Dictionary with authentication credentials.
        """
        return {
            "apikey": self.config["api_key"],
            "secretapikey": self.config["secret_api_key"],
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
        # Build URL for retrieveByNameType endpoint
        # Format: /dns/retrieveByNameType/DOMAIN/TYPE/[SUBDOMAIN]
        subdomain_path = f"/{record_name}" if record_name != "@" else ""
        url = f"{self.BASE_URL}/dns/retrieveByNameType/{domain}/{record_type}{subdomain_path}"

        try:
            response = requests.post(url, json=self._get_auth_payload(), timeout=10)
            response.raise_for_status()

            result = response.json()

            if result.get("status") != "SUCCESS":
                raise DNSProviderError(f"Porkbun API error: {result}")

            records: list[dict[str, str | int]] = result.get("records", [])

            if not records:
                raise DNSProviderError(f"No {record_type} record found for {record_name}.{domain}")

            # Return IP from the first record
            content = records[0].get("content", "")
            if not content:
                raise DNSProviderError(f"No content in record for {record_name}.{domain}")
            return str(content)

        except requests.exceptions.RequestException as e:
            raise DNSProviderError(f"Failed to get current IP from Porkbun: {e}") from e

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
        # Build URL for editByNameType endpoint
        # Format: /dns/editByNameType/DOMAIN/TYPE/[SUBDOMAIN]
        subdomain_path = f"/{record_name}" if record_name != "@" else ""
        url = f"{self.BASE_URL}/dns/editByNameType/{domain}/{record_type}{subdomain_path}"

        payload = self._get_auth_payload()
        payload["content"] = ip
        payload["ttl"] = self.config["ttl"]

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()

            if result.get("status") != "SUCCESS":
                raise DNSProviderError(f"Porkbun API error: {result}")

            logger.info(f"Porkbun record updated: {record_name}.{domain} -> {ip}")
            return True

        except requests.exceptions.RequestException as e:
            raise DNSProviderError(f"Failed to update IP on Porkbun: {e}") from e
