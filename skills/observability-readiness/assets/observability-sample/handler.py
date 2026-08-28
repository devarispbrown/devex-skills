# handler.py — sample request handler that logs but assigns no correlation ID.
import json
import logging

logger = logging.getLogger("api.handler")


def handle(event, context):
    logger.info("handling event for user %s", event.get("user_id"))
    body = json.dumps({"ok": True})
    return {"statusCode": 200, "body": body}
