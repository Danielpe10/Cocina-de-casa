import logging
from flask import Flask, request, jsonify
import config
from agents import ordering

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.get("/webhook")
def verify_webhook():
    """Meta webhook verification handshake."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == config.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return challenge, 200

    logger.warning("Webhook verification failed")
    return "Forbidden", 403


@app.post("/webhook")
def receive_webhook():
    """Process inbound WhatsApp messages from Meta."""
    data = request.get_json(silent=True) or {}

    try:
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return jsonify({"status": "no_message"}), 200

        msg = messages[0]
        from_phone = msg.get("from", "")
        msg_type = msg.get("type", "")

        if msg_type != "text":
            return jsonify({"status": "ignored_non_text"}), 200

        body = msg["text"]["body"]
        logger.info("Inbound from %s: %s", from_phone, body[:80])

        reply = ordering.handle_message(from_phone, body)

        from agents import whatsapp as wa
        wa.send_text(from_phone, reply)

    except Exception as e:
        logger.error("Webhook processing error: %s", e)

    return jsonify({"status": "ok"}), 200


@app.get("/health")
def health():
    return jsonify({"status": "running", "restaurant": config.RESTAURANT_NAME}), 200


@app.get("/menu")
def show_menu():
    from agents import menu as menu_mod
    return jsonify(menu_mod.load()), 200


@app.get("/orders")
def show_orders():
    import json
    from pathlib import Path
    data = json.loads((Path(__file__).parent / "data" / "orders.json").read_text())
    return jsonify(data), 200
