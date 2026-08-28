"""Tests for app.core."""

from app.core import parse


def test_parse_valid_line():
    assert parse("widget,3") == {"name": "widget", "count": 3}


def test_parse_empty_line_returns_error():
    result = parse("  ")
    assert isinstance(result, ParseError)
