"""Fixture API surface for assess_test_suite.py. Not a real application."""
from http.server import BaseHTTPRequestHandler


class OrderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"orders": []}')

    def do_POST(self):
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b'{"created": true}')
