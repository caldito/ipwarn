# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-02-08

### Added
- Complete rewrite in Python 3.12+ for better maintainability
- Modular DNS provider architecture for easy extensibility
- Porkbun DNS provider support
- Multiple IP checker services with automatic failover:
  - icanhazip.com
  - ipify.org
  - ifconfig.me
- Structured logging with configurable log levels
- `--once` and `--dry-run` CLI flags for testing
- Comprehensive test suite with pytest
- Support for multiple DNS providers simultaneously
- Base classes for DNS providers and notifiers

### Changed
- Uses `requests` library for HTTP queries instead of curl
- Configuration file format extended (backward compatible with v1.x)
- Docker image now Python-based (smaller, more maintainable)
- Improved error handling and retry logic
- Better logging and debugging capabilities

### Deprecated
- Bash version is no longer maintained

### Removed
- Bash implementation (replaced by Python)

### Fixed
- Better handling of network failures and API errors
- More robust IP validation
- Cleaner separation of concerns between providers

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
