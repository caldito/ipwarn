"""Telegram notifier implementation."""

import logging

import requests

from ipwarn.notifiers.base import BaseNotifier, NotifierError

logger = logging.getLogger(__name__)


class TelegramNotifier(BaseNotifier):
    """Telegram bot notifier."""

    BASE_URL = "https://api.telegram.org"

    def __init__(self, api_token: str, api_id: str):
        """Initialize Telegram notifier.

        Args:
            api_token: Telegram bot API token.
            api_id: Telegram chat ID to send notifications to.
        """
        config = {
            "api_token": api_token,
            "api_id": api_id,
        }
        super().__init__(config)

    def _validate_config(self) -> None:
        """Validate Telegram configuration.

        Raises:
            NotifierError: If configuration is invalid.
        """
        if not self.config.get("api_token"):
            raise NotifierError("Telegram API token is required")
        if not self.config.get("api_id"):
            raise NotifierError("Telegram API ID is required")

    def send(self, message: str) -> bool:
        """Send a notification message.

        Args:
            message: Message to send.

        Returns:
            True if notification was sent successfully, False otherwise.

        Raises:
            NotifierError: If notification fails.
        """
        url = f"{self.BASE_URL}/bot{self.config['api_token']}/sendMessage"

        payload = {
            "chat_id": self.config["api_id"],
            "text": message,
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            result = response.json()

            if not result.get("ok"):
                raise NotifierError(f"Telegram API error: {result}")

            logger.debug("Telegram notification sent successfully")
            return True

        except requests.exceptions.RequestException as e:
            raise NotifierError(f"Failed to send Telegram notification: {e}") from e
