"""Logging and metrics export setup. Stdlib only."""
import logging


def configure_logging(level):
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


COUNTERS = {}


def count(name):
    COUNTERS[name] = COUNTERS.get(name, 0) + 1
    return COUNTERS[name]


def export():
    """Dump counters to the log; wire a real exporter in production."""
    logging.getLogger("metrics").info("counters: %s", COUNTERS)
