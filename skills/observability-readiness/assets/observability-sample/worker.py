# worker.py — sample background worker with structured logging and a counter.
import logging

from prometheus_client import Counter

logger = logging.getLogger("worker")
jobsDone = Counter("jobs_done_total", "Jobs completed")


def drain(queue):
    logger.info("draining queue %s", queue.name)
    jobsDone.inc()
