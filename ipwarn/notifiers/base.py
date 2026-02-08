"""Base class for notifiers."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

logger = logging.getLogger(__name__)


class NotifierError(Exception):
    """Notifier error exception."""


class BaseNotifier(ABC):
    """Abstract base class for notifiers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize notifier.

        Args:
            config: Notifier-specific configuration.
        """
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """Validate notifier-specific configuration.

        Raises:
            NotifierError: If configuration is invalid.
        """
        pass

    @abstractmethod
    def send(self, message: str) -> bool:
        """Send a notification message.

        Args:
            message: Message to send.

        Returns:
            True if notification was sent successfully, False otherwise.

        Raises:
            NotifierError: If notification fails.
        """
        pass
