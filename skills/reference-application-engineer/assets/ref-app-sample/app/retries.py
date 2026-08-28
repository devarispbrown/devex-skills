"""Bounded retry helper with exponential backoff. Stdlib only."""
import time


def retry(times=3, base_delay=0.1):
    """Decorator: call a function up to `times` attempts, then raise the last error.

    Bounded by construction: `times` fixes the ceiling; backoff grows by 2^n.
    """

    def decorate(fn):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    time.sleep(base_delay * (2 ** attempt))
            raise last_error

        return wrapper

    return decorate
