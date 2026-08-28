"""Security defaults: secrets from the environment, safe response headers."""
import os


def security_headers():
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Cache-Control": "no-store",
    }


def read_secret(name):
    """Secrets are read from the environment, never hardcoded or logged."""
    value = os.getenv(name, "")
    if not value:
        raise RuntimeError(f"missing required secret {name}")
    return value
