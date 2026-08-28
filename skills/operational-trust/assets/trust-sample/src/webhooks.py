"""Sample outbound delivery worker used by the trust-sample fixture.

Shows the retry pattern the trust scanner looks for in code.
"""

import time

MAX_ATTEMPTS = 5


def deliver(event_id, url, attempts=MAX_ATTEMPTS):
    for attempt in range(attempts):
        try:
            resp = http_post(url, payload(event_id))
            if resp.status < 500:
                return resp
        except NetworkError:
            pass
        time.sleep(backoff_with_jitter(attempt))
    enqueue_dead_letter(event_id)
    return None


def backoff_with_jitter(attempt):
    base = min(2 ** attempt, 60)
    return base + (hash(time.time_ns()) % base)


def payload(event_id):
    return {"event_id": event_id}


def http_post(url, body):
    raise NotImplementedError


class NetworkError(Exception):
    pass


def enqueue_dead_letter(event_id):
    print(f"dead letter: {event_id}")
