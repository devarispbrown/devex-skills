"""Fixture streaming consumer stub. Deliberately has NO tests."""


def consume_batch(records):
    for record in records:
        yield record["value"]
