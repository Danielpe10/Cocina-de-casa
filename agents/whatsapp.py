import requests
import config


def send_text(to: str, body: str) -> dict:
    """Send a plain text WhatsApp message via Meta Cloud API."""
    headers = {
        "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": body},
    }
    resp = requests.post(config.WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def send_template(to: str, template_name: str, lang: str = "es", components: list = None) -> dict:
    """Send an approved template message (required for outbound outside 24h window)."""
    headers = {
        "Authorization": f"Bearer {config.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    template = {
        "name": template_name,
        "language": {"code": lang},
    }
    if components:
        template["components"] = components

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": template,
    }
    resp = requests.post(config.WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def notify_owner(body: str) -> dict:
    return send_text(config.OWNER_WHATSAPP, body)
