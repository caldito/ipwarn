# ipwarn

A simple Dynamic DNS Update Client that automatically updates your DNS records when your IP changes.

## Features

- **Multiple DNS Providers**: Update records on GoDaddy and Porkbun
- **Automatic IP Detection**: Checks your public IP with automatic failover between multiple services
- **Telegram Notifications**: Get notified instantly when your IP changes
- **Easy Configuration**: Simple config file with sensible defaults
- **Production Ready**: Docker and systemd support for 24/7 operation
- **Test Once**: Run in dry-run mode to verify your setup before going live

## Quick Start

### Docker (Recommended)

```bash
# Build the image
docker build -t ipwarn:2.0.0 .

# Run with your config file
docker run -d \
  --name ipwarn \
  --mount type=bind,source=$(pwd)/ipwarn.conf,target=/etc/ipwarn/ipwarn.conf \
  pablogcaldito/ipwarn:2.0.0
```

### Systemd Service

```bash
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn-systemd-easy-install.sh
sudo bash ./ipwarn-systemd-easy-install.sh
```

After installation, configure `/etc/ipwarn/ipwarn.conf` and restart:
```bash
sudo systemctl restart ipwarn.service
```

## Configuration

Create or edit `/etc/ipwarn/ipwarn.conf` with your settings:

```bash
# Check interval in seconds (default: 30)
INTERVAL=30

# IP checking services (comma-separated, in order)
IP_CHECKERS=icanhazip.com,ipify.org,ifconfig.me

# Telegram Notifications
UPDATE_TELEGRAM=false
TEL_API_TOKEN=your_bot_token
TEL_CHAT_ID=your_chat_id

# GoDaddy DNS
UPDATE_GODADDY=false
GD_DOMAIN=example.com
GD_RECORD_NAME="@"              # Use "@" for root domain or "www" for subdomain
GD_RECORD_TYPE="A"
GD_API_KEY=your_api_key
GD_API_SECRET=your_api_secret

# Porkbun DNS
UPDATE_PORKBUN=false
PB_DOMAIN=example.com
PB_RECORD_NAME="@"              # Use "@" for root domain or "www" for subdomain
PB_RECORD_TYPE="A"
PB_API_KEY=your_api_key
PB_SECRET_API_KEY=your_secret_api_key
PB_TTL=600                        # Time to live in seconds

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

**Tip**: Test your configuration first with `--dry-run` flag:
```bash
docker run --rm \
  --mount type=bind,source=ipwarn.conf,target=/etc/ipwarn/ipwarn.conf \
  pablogcaldito/ipwarn:2.0.0 --dry-run --once
```

## CLI Options

```bash
ipwarn [-h] [--version] [-c CONFIG] [--once] [--dry-run]

Options:
  -h, --help            Show help message
  -v, --version         Show version
  -c, --config CONFIG   Path to config file (default: /etc/ipwarn/ipwarn.conf)
  --once                Run once and exit (for testing)
  --dry-run             Don't actually update DNS records (for testing)
```

## Getting API Keys

### GoDaddy
1. Go to [developer.godaddy.com](https://developer.godaddy.com/)
2. Sign in and go to Keys & Credentials
3. Create a new API key
4. Select Production and copy your Key and Secret

### Porkbun
1. Log in to [porkbun.com](https://porkbun.com/)
2. Go to Account → API Access
3. Create a new API key
4. Copy your API Key and Secret API Key

### Telegram Bot
1. Open Telegram and start a chat with [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy your bot token
4. To get your chat ID, send a message to your bot and visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`

## Development

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/caldito/ipwarn.git
cd ipwarn

# Setup development environment with uv
make setup

# Run tests
make test

# Format code
make format

# Run linters
make lint

# Run locally for testing
make run-once
```

### Development Commands

```bash
make setup          # Setup venv with uv
make test           # Run tests
make lint           # Run linters (ruff, mypy)
make format         # Format code (black, ruff)
make run            # Run continuously
make run-once       # Run once for testing
make clean          # Clean build artifacts
```

## License

MIT License - see the [LICENSE](https://github.com/caldito/ipwarn/blob/master/LICENSE) file for details
