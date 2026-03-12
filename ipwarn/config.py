"""Configuration file parser for ipwarn.

This module provides backward-compatible parsing of shell-like configuration files,
as used by the original Bash version of ipwarn.
"""

import re
from pathlib import Path


class ConfigError(Exception):
    """Configuration error exception."""


class Config:
    """Configuration parser for shell-like config files."""

    def __init__(self, config_path: str = "/etc/ipwarn/ipwarn.conf"):
        """Initialize configuration.

        Args:
            config_path: Path to the configuration file.
        """
        self.config_path = Path(config_path)
        self._values: dict[str, str] = {}
        self._parse()

    def _parse(self) -> None:
        """Parse the configuration file."""
        if not self.config_path.exists():
            raise ConfigError(f"Config file not found: {self.config_path}")

        with open(self.config_path, encoding="utf-8") as f:
            for _line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse KEY=VALUE format
                match = re.match(r"^([A-Z_]+)=(.*)$", line)
                if not match:
                    continue

                key, value = match.groups()

                # Remove quotes if present (both single and double)
                if (value.startswith('"') and value.endswith('"')) or (
                    value.startswith("'") and value.endswith("'")
                ):
                    value = value[1:-1]

                self._values[key] = value

    def get(self, key: str, default: str = "") -> str:
        """Get a configuration value.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            The configuration value or default.
        """
        return self._values.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get a boolean configuration value.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            True if value is "true" (case-insensitive), False otherwise.
        """
        value = self.get(key, str(default)).lower()
        return value == "true"

    def get_int(self, key: str, default: int = 0) -> int:
        """Get an integer configuration value.

        Args:
            key: Configuration key.
            default: Default value if key not found or invalid.

        Returns:
            The integer value or default.
        """
        value = self.get(key, str(default))
        try:
            return int(value)
        except ValueError:
            return default

    def get_list(self, key: str, default: str = "") -> list[str]:
        """Get a comma-separated list from configuration.

        Args:
            key: Configuration key.
            default: Default value if key not found.

        Returns:
            List of values, split by comma.
        """
        value = self.get(key, default)
        return [item.strip() for item in value.split(",") if item.strip()]

    @property
    def interval(self) -> int:
        """Get check interval in seconds."""
        return self.get_int("INTERVAL", 30)

    @property
    def ip_checkers(self) -> list[str]:
        """Get list of IP checker services."""
        return self.get_list("IP_CHECKERS", "icanhazip.com,ipify.org,ifconfig.me")

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get("LOG_LEVEL", "INFO").upper()

    @property
    def update_telegram(self) -> bool:
        """Check if Telegram updates are enabled."""
        return self.get_bool("UPDATE_TELEGRAM", False)

    @property
    def telegram_api_token(self) -> str:
        """Get Telegram API token."""
        return self.get("TEL_API_TOKEN", "")

    @property
    def telegram_api_id(self) -> str:
        """Get Telegram API ID."""
        return self.get("TEL_API_ID", "")

    @property
    def update_godaddy(self) -> bool:
        """Check if GoDaddy updates are enabled."""
        return self.get_bool("UPDATE_GODADDY", False)

    @property
    def godaddy_domain(self) -> str:
        """Get GoDaddy domain."""
        return self.get("GD_DOMAIN", "")

    @property
    def godaddy_record_name(self) -> str:
        """Get GoDaddy record name."""
        return self.get("GD_RECORD_NAME", "@")

    @property
    def godaddy_record_type(self) -> str:
        """Get GoDaddy record type."""
        return self.get("GD_RECORD_TYPE", "A")

    @property
    def godaddy_api_key(self) -> str:
        """Get GoDaddy API key."""
        return self.get("GD_API_KEY", "")

    @property
    def godaddy_api_secret(self) -> str:
        """Get GoDaddy API secret."""
        return self.get("GD_API_SECRET", "")

    @property
    def update_porkbun(self) -> bool:
        """Check if Porkbun updates are enabled."""
        return self.get_bool("UPDATE_PORKBUN", False)

    @property
    def porkbun_domain(self) -> str:
        """Get Porkbun domain."""
        return self.get("PB_DOMAIN", "")

    @property
    def porkbun_record_name(self) -> str:
        """Get Porkbun record name."""
        return self.get("PB_RECORD_NAME", "@")

    @property
    def porkbun_record_type(self) -> str:
        """Get Porkbun record type."""
        return self.get("PB_RECORD_TYPE", "A")

    @property
    def porkbun_api_key(self) -> str:
        """Get Porkbun API key."""
        return self.get("PB_API_KEY", "")

    @property
    def porkbun_secret_api_key(self) -> str:
        """Get Porkbun secret API key."""
        return self.get("PB_SECRET_API_KEY", "")

    @property
    def porkbun_ttl(self) -> int:
        """Get Porkbun TTL."""
        return self.get_int("PB_TTL", 600)
