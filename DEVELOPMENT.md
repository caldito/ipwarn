# Development Guide

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

## Quick Start

```bash
# Clone the repository
git clone https://github.com/caldito/ipwarn.git
cd ipwarn

# Setup development environment (creates .venv and installs dependencies)
make setup

# Run tests
make test

# Format code
make format

# Run linters
make lint
```

## Architecture

### Project Structure

```
ipwarn/
├── ipwarn/
│   ├── __init__.py
│   ├── __main__.py              # CLI entry point and main application loop
│   ├── config.py                # Configuration file parser
│   ├── ip_checkers.py           # IP detection with failover
│   ├── logger.py                # Logging configuration
│   ├── dns_providers/           # DNS provider implementations
│   │   ├── base.py              # Abstract base class
│   │   ├── godaddy.py           # GoDaddy provider
│   │   └── porkbun.py           # Porkbun provider
│   └── notifiers/               # Notification handlers
│       ├── base.py              # Abstract base class
│       └── telegram.py          # Telegram notifier
├── tests/                       # Test suite
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_dns_providers.py
│   └── test_ip_checkers.py
└── pyproject.toml               # Project configuration
```

### Core Components

#### Configuration Parser (`config.py`)
- Parses shell-like `.conf` files
- Supports quoted values and comments
- Provides type-safe access methods: `get()`, `get_bool()`, `get_int()`, `get_list()`

#### IP Checker (`ip_checkers.py`)
- Tries multiple IP checking services with automatic failover
- Validates IPv4 addresses
- Configurable timeout per service

#### DNS Providers (`dns_providers/`)
- Abstract `BaseDNSProvider` class for extensibility
- Check if update is needed before making API calls
- Proper error handling and logging

#### Notifiers (`notifiers/`)
- Abstract `BaseNotifier` class for extensibility
- Send notifications on successful IP updates

## Adding a New DNS Provider

1. Create a new file in `ipwarn/dns_providers/` (e.g., `cloudflare.py`)

2. Inherit from `BaseDNSProvider` and implement required methods:

```python
from ipwarn.dns_providers.base import BaseDNSProvider, DNSProviderError

class CloudflareProvider(BaseDNSProvider):
    def _validate_config(self) -> None:
        """Validate provider-specific configuration."""
        if not self.config.get("CF_API_TOKEN"):
            raise DNSProviderError("Cloudflare API token is required")

    def get_current_ip(self, domain: str, record_name: str, record_type: str) -> str:
        """Get current IP for a DNS record."""
        # Implement API call to get current IP
        pass

    def update_ip(self, domain: str, record_name: str, record_type: str, ip: str) -> bool:
        """Update DNS record with new IP."""
        # Implement API call to update IP
        pass
```

3. Add configuration options to `config.py` (if needed)

4. Update `__main__.py` to instantiate your provider when enabled

## Adding a New Notifier

1. Create a new file in `ipwarn/notifiers/` (e.g., `email.py`)

2. Inherit from `BaseNotifier` and implement required methods:

```python
from ipwarn.notifiers.base import BaseNotifier, NotifierError

class EmailNotifier(BaseNotifier):
    def _validate_config(self) -> None:
        """Validate notifier-specific configuration."""
        if not self.config.get("EMAIL_TO"):
            raise NotifierError("Email recipient is required")

    def send(self, message: str) -> None:
        """Send notification message."""
        # Implement email sending logic
        pass
```

3. Add configuration options to `config.py`

4. Update `__main__.py` to instantiate your notifier when enabled

## Running Tests

```bash
# Run all tests
make test

# Run specific test file
.venv/bin/pytest tests/test_config.py -v

# Run with coverage
.venv/bin/pytest --cov=ipwarn tests/
```

## Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Auto-fix linting issues where possible
.venv/bin/ruff check --fix ipwarn/ tests/
```

## Testing Locally

```bash
# Run once with dry-run (no actual updates)
make run-once

# Run with custom config
.venv/bin/python -m ipwarn --config path/to/config.conf --dry-run --once
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Tag the release: `git tag v2.0.1`
4. Push tag: `git push origin v2.0.1`
5. Build Docker images: `make build-docker-multi`
6. Push to registry: `make push-docker`
