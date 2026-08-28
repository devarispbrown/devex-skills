"""Fixture: a metrics/dashboard consumer."""
from prometheus_client import Counter

ORDERS_TOTAL = Counter("orders_total", "Total orders processed")
LATENCY = Summary("request_latency_seconds", "Request latency")


def record_order():
    ORDERS_TOTAL.inc()
