"""Base class for DNS providers."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DNSProviderError(Exception):
    """DNS provider error exception."""


class BaseDNSProvider(ABC):
    """Abstract base class for DNS providers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize DNS provider.

        Args:
            config: Provider-specific configuration.
        """
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """Validate provider-specific configuration.

        Raises:
            DNSProviderError: If configuration is invalid.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    def needs_update(self, domain: str, record_name: str, record_type: str, new_ip: str) -> bool:
        """Check if DNS record needs to be updated.

        Args:
            domain: Domain name.
            record_name: Record name.
            record_type: Record type.
            new_ip: New IP address to check.

        Returns:
            True if update is needed, False if IP is already correct.

        Raises:
            DNSProviderError: If unable to check current IP.
        """
        try:
            current_ip = self.get_current_ip(domain, record_name, record_type)
            return current_ip != new_ip
        except DNSProviderError as e:
            logger.warning(f"Failed to check current IP for {domain}: {e}")
            return True
