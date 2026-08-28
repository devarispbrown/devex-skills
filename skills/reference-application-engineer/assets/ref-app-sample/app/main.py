"""Entrypoint: wires routes, auth, and the HTTP server. Stdlib only."""
import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from app.auth import require_token
from app.config import settings
from app.errors import error_response
from app.observability import configure_logging
from app.security import security_headers


class Handler(BaseHTTPRequestHandler):
    def _handle(self):
        token = self.headers.get("Authorization", "")
        if not require_token(token):
            error_response(self, 401, "unauthorized")
            return
        path = self.path.split("?")[0]
        if path == "/v1/health":
            self._json(200, {"status": "ok"})
        elif path == "/v1/echo" and self.command == "POST":
            self._json(200, {"echo": {"ok": True}})
        else:
            error_response(self, 404, "not found")

    def _json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        for key, value in security_headers().items():
            self.send_header(key, value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    do_GET = do_POST = _handle

    def log_message(self, fmt, *args):
        logging.getLogger("http").info(fmt % args)


def serve():
    configure_logging(settings.log_level)
    server = ThreadingHTTPServer((settings.host, settings.port), Handler)
    print(f"listening on {settings.host}:{settings.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    serve()
