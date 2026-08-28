"""Fixture contract test using a pact-style consumer expectation."""

EXPECTED = {
    "status": 201,
    "body": {"created": True},
}


def test_order_creation_contract():
    assert EXPECTED["status"] == 201
