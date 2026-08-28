"""Core parsing surface. No machine-readable schema accompanies this module."""


class ParseError(Exception):
    """Invalid-input result returned instead of raising."""


def parse(text):
    """Parse one line into a record, or return a ParseError result."""
    if not text.strip():
        return ParseError("empty line")
    parts = text.strip().split(",")
    return {"name": parts[0], "count": int(parts[1]) if len(parts) > 1 else 0}
