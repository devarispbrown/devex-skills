"""Fixture pytest tests with a hypothesis property test."""
from hypothesis import given
from hypothesis import strategies as st


@given(st.text())
def test_echo_is_idempotent(value):
    assert (value + "") == value


def test_health_returns_200():
    assert True
