"""Token-based authentication for the reference stub. Stdlib only."""
import hmac

from app.config import settings


def require_token(token):
    """Return True only when the presented token matches the configured one.

    Fails closed: an unconfigured token means no access, not open access.
    """
    expected = settings.auth_token
    if not expected:
        return False
    return hmac.compare_digest(token.removeprefix("Bearer "), expected)
