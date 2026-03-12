"""IP checker module with multiple services and failover support."""

import logging
import re

import requests

logger = logging.getLogger(__name__)


class IPCheckerError(Exception):
    """IP checker error exception."""


class IPChecker:
    """IP checker with multiple services and failover."""

    CHECKERS = {
        "icanhazip.com": "https://icanhazip.com",
        "ipify.org": "https://api.ipify.org",
        "ifconfig.me": "https://ifconfig.me/ip",
    }

    def __init__(self, checkers: list[str] | None = None, timeout: int = 5):
        """Initialize IP checker.

        Args:
            checkers: List of checker names (order matters for failover).
            timeout: Timeout in seconds for each checker.
        """
        self.checkers = checkers or list(self.CHECKERS.keys())
        self.timeout = timeout

    def get_ip(self) -> str:
        """Get current IP address with failover.

        Returns:
            The current IP address.

        Raises:
            IPCheckerError: If all checkers fail.
        """
        last_error = None

        for checker in self.checkers:
            url = self.CHECKERS.get(checker)
            if not url:
                logger.warning(f"Unknown IP checker: {checker}")
                continue

            try:
                ip = self._check_ip(url)
                logger.debug(f"Got IP {ip} from {checker}")
                return ip
            except IPCheckerError as e:
                logger.warning(f"Failed to get IP from {checker}: {e}")
                last_error = e
                continue

        raise IPCheckerError(f"All IP checkers failed. Last error: {last_error}")

    def _check_ip(self, url: str) -> str:
        """Check IP from a single service.

        Args:
            url: URL to check IP from.

        Returns:
            The IP address.

        Raises:
            IPCheckerError: If the check fails.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            ip = response.text.strip()

            # Validate IP address format
            if not self._is_valid_ip(ip):
                raise IPCheckerError(f"Invalid IP address: {ip}")

            return ip

        except requests.exceptions.Timeout:
            raise IPCheckerError(f"Timeout checking IP from {url}") from None
        except requests.exceptions.RequestException as e:
            raise IPCheckerError(f"Request failed: {e}") from e

    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IP address format (IPv4 only for now).

        Args:
            ip: IP address string.

        Returns:
            True if valid IPv4 address, False otherwise.
        """
        # Simple IPv4 validation
        ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(ipv4_pattern, ip))
