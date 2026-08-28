"""Typed error surface with status codes. Stdlib only."""
import json


class AppError(Exception):
    """Application error carrying a status code and a caller-safe message."""

    def __init__(self, message, status=500):
        super().__init__(message)
        self.message = message
        self.status = status


def error_response(handler, status, message):
    body = json.dumps({"error": {"status": status, "message": message}}).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
