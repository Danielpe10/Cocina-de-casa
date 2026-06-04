import requests
import config
from agents import menu as menu_mod, llm


def _graph(endpoint: str, payload: dict) -> dict:
    url = f"{config.GRAPH_BASE}/{endpoint}"
    payload["access_token"] = config.META_PAGE_ACCESS_TOKEN
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def post_facebook(message: str) -> dict:
    return _graph(f"{config.FACEBOOK_PAGE_ID}/feed", {"message": message})


def post_instagram(caption: str, image_url: str = None) -> dict:
    """Two-step Instagram publish: create container then publish."""
    if not config.INSTAGRAM_BUSINESS_ACCOUNT_ID:
        return {"skipped": "no instagram account configured"}

    ig_id = config.INSTAGRAM_BUSINESS_ACCOUNT_ID
    container_payload = {"caption": caption}
    if image_url:
        container_payload["image_url"] = image_url
    else:
        # Text-only is not supported by IG; skip gracefully
        return {"skipped": "instagram requires an image"}

    container = _graph(f"{ig_id}/media", container_payload)
    creation_id = container.get("id")
    if not creation_id:
        return {"error": "failed to create container", "detail": container}

    return _graph(f"{ig_id}/media_publish", {"creation_id": creation_id})


def generate_daily_special_post() -> str:
    available = menu_mod.get_available()
    if not available:
        return ""

    items_list = ", ".join(
        f"{name} (${info['price']:.0f})" for name, info in available.items()
    )
    prompt = (
        f"Escribe un post bilingüe (español + inglés) para Facebook/Instagram "
        f"anunciando el menú del día de '{config.RESTAURANT_NAME}' en {config.RESTAURANT_CITY}. "
        f"Platos disponibles: {items_list}. "
        f"Máximo 150 palabras total. Incluye emojis. "
        f"Termina invitando a escribir por WhatsApp para pedir."
    )
    return llm.ask(prompt, system=llm.SYSTEM_VOICE)


def publish_daily_special():
    caption = generate_daily_special_post()
    if not caption:
        return

    fb_result = post_facebook(caption)
    return {"facebook": fb_result, "caption": caption}
