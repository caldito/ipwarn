# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-13
[Full changelog](https://github.com/caldito/ipwarn/compare/v1.0.1...v2.0.0)
### Added
- Python 3.12+ rewrite with modular DNS provider architecture
- GoDaddy and Porkbun DNS provider support
- Multiple IP checker services with automatic failover
- Telegram notifications
- Configurable logging levels
- `--once` and `--dry-run` CLI flags
- Test suite with pytest
- GitHub Actions CI/CD with automated testing
- Multi-architecture Docker builds (AMD64, ARM64)
- Docker images published to GitHub Container Registry (GHCR)

### Changed
- Migrated from Bash to Python
- Uses `requests` library instead of curl
- Config file format extended (backward compatible)
- Improved error handling and retry logic
- Updated documentation

### Deprecated
- Bash version no longer maintained since the project has moved to python

## [v1.0.1] - 2022-12-29
[Full changelog](https://github.com/caldito/ipwarn/compare/v1.0.0...v1.0.1)
### Fixed
- Docker instructions in README.md
- Fix pipelines for releasing multi-arch docker images

## [v1.0.0] - 2022-12-28
[Full changelog](https://github.com/caldito/ipwarn/compare/v0.1.0...v1.0.0)
### Added
- Refactor to a design in which the program runs indefinitely in the background
- Release for amd64 and arm64 containers
- All options managed though the config file
- Posibility to override the config file directory
- Systemd service file
- Systemd easy install script
- Changelog

## [v0.1.0]
### Added
- Initial version
