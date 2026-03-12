"""Main entry point for ipwarn."""

import argparse
import logging
import sys
import time

from ipwarn import __version__
from ipwarn.config import Config, ConfigError
from ipwarn.dns_providers.base import BaseDNSProvider, DNSProviderError
from ipwarn.dns_providers.godaddy import GoDaddyProvider
from ipwarn.dns_providers.porkbun import PorkbunProvider
from ipwarn.ip_checkers import IPChecker, IPCheckerError
from ipwarn.logger import setup_logging
from ipwarn.notifiers.base import BaseNotifier, NotifierError
from ipwarn.notifiers.telegram import TelegramNotifier

logger = logging.getLogger(__name__)


class IPWarn:
    """Main ipwarn application."""

    def __init__(
        self,
        config: Config,
        dry_run: bool = False,
    ):
        """Initialize ipwarn application.

        Args:
            config: Configuration instance.
            dry_run: If True, don't actually update DNS records.
        """
        self.config = config
        self.dry_run = dry_run
        self.ip_checker = IPChecker(checkers=config.ip_checkers)
        self.providers: list[tuple[str, BaseDNSProvider]] = []
        self.notifiers: list[tuple[str, BaseNotifier]] = []
        self._last_ip: str | None = None

        self._setup_providers()
        self._setup_notifiers()

    def _setup_providers(self) -> None:
        """Set up DNS providers based on configuration."""
        if self.config.update_godaddy:
            godaddy_provider = GoDaddyProvider(
                api_key=self.config.godaddy_api_key,
                api_secret=self.config.godaddy_api_secret,
            )
            self.providers.append(("GoDaddy", godaddy_provider))
            logger.info("GoDaddy provider enabled")

        if self.config.update_porkbun:
            porkbun_provider = PorkbunProvider(
                api_key=self.config.porkbun_api_key,
                secret_api_key=self.config.porkbun_secret_api_key,
                ttl=self.config.porkbun_ttl,
            )
            self.providers.append(("Porkbun", porkbun_provider))
            logger.info("Porkbun provider enabled")

        if not self.providers:
            logger.warning("No DNS providers enabled")

    def _setup_notifiers(self) -> None:
        """Set up notification handlers based on configuration."""
        if self.config.update_telegram:
            notifier = TelegramNotifier(
                api_token=self.config.telegram_api_token,
                api_id=self.config.telegram_api_id,
            )
            self.notifiers.append(("Telegram", notifier))
            logger.info("Telegram notifier enabled")

    def _send_notification(self, message: str) -> None:
        """Send notification to all enabled notifiers.

        Args:
            message: Message to send.
        """
        for name, notifier in self.notifiers:
            try:
                notifier.send(message)
                logger.debug(f"Notification sent via {name}")
            except NotifierError as e:
                logger.error(f"Failed to send notification via {name}: {e}")

    def _update_dns_providers(self, new_ip: str) -> None:
        """Update DNS records for all enabled providers.

        Args:
            new_ip: New IP address to update to.
        """
        for name, provider in self.providers:
            try:
                domain = (
                    self.config.godaddy_domain if name == "GoDaddy" else self.config.porkbun_domain
                )
                record_name = (
                    self.config.godaddy_record_name
                    if name == "GoDaddy"
                    else self.config.porkbun_record_name
                )
                record_type = (
                    self.config.godaddy_record_type
                    if name == "GoDaddy"
                    else self.config.porkbun_record_type
                )

                if provider.needs_update(domain, record_name, record_type, new_ip):
                    if self.dry_run:
                        logger.info(
                            f"[DRY RUN] Would update {name} record: {record_name}.{domain} -> {new_ip}"
                        )
                    else:
                        provider.update_ip(domain, record_name, record_type, new_ip)
                        logger.info(f"Updated {name} record: {record_name}.{domain} -> {new_ip}")
                else:
                    logger.info(f"{name} record already correct: {new_ip}")

            except DNSProviderError as e:
                logger.error(f"Failed to update {name} DNS record: {e}")

    def check_and_update(self) -> str | None:
        """Check IP and update DNS if changed.

        Returns:
            New IP address if changed, None otherwise.
        """
        try:
            new_ip = self.ip_checker.get_ip()
            logger.info(f"Current IP: {new_ip}")

            if not hasattr(self, "_last_ip") or self._last_ip != new_ip:
                logger.info(f"IP changed from {getattr(self, '_last_ip', 'unknown')} to {new_ip}")

                self._update_dns_providers(new_ip)
                self._send_notification(f"New IP address: {new_ip}")

                self._last_ip = new_ip
                return new_ip
            else:
                logger.debug("IP unchanged")
                return None

        except IPCheckerError as e:
            logger.error(f"Failed to get IP address: {e}")
            return None

    def run_once(self) -> None:
        """Run a single check and update."""
        logger.info("Running once")
        self.check_and_update()

    def run_forever(self) -> None:
        """Run continuous monitoring loop."""
        logger.info(f"Starting ipwarn v{__version__}")
        logger.info(f"Checking IP every {self.config.interval} seconds")

        try:
            while True:
                self.check_and_update()
                time.sleep(self.config.interval)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            sys.exit(0)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Dynamic DNS update client with modular provider support"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"ipwarn v{__version__}",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="/etc/ipwarn/ipwarn.conf",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (useful for testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't actually update DNS records",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    try:
        config = Config(args.config)

        setup_logging(config.log_level)

        app = IPWarn(config, dry_run=args.dry_run)

        if args.once:
            app.run_once()
        else:
            app.run_forever()

    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
