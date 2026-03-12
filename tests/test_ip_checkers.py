"""Tests for IP checkers."""

from ipwarn.ip_checkers import IPChecker


def test_ip_checker_initialization():
    """Test IP checker initialization."""
    checker = IPChecker()
    assert checker.checkers == ["icanhazip.com", "ipify.org", "ifconfig.me"]
    assert checker.timeout == 5

    custom_checker = IPChecker(checkers=["icanhazip.com"], timeout=10)
    assert custom_checker.checkers == ["icanhazip.com"]
    assert custom_checker.timeout == 10


def test_ip_checker_invalid_ip():
    """Test IP validation."""
    assert IPChecker._is_valid_ip("192.168.1.1") is True
    assert IPChecker._is_valid_ip("0.0.0.0") is True
    assert IPChecker._is_valid_ip("255.255.255.255") is True
    assert IPChecker._is_valid_ip("invalid") is False
    assert IPChecker._is_valid_ip("192.168.1") is False
    assert IPChecker._is_valid_ip("192.168.1.256") is False
    assert IPChecker._is_valid_ip("") is False
