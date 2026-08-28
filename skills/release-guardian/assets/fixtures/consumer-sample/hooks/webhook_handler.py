"""Fixture: a webhook handler consumer."""
import hashlib
import hmac
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/hooks/order_events", methods=["POST"])
def handle_order_event():
    signature = request.headers.get("X-Hub-Signature", "")
    payload = json.loads(request.data)
    expected = hmac.new(b"<secret>", request.data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return "bad signature", 401
    if payload["event_type"] == "order.created":
        print("order created:", payload["order"]["id"])
    return "ok", 200
