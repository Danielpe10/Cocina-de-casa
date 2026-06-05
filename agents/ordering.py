import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict
from agents import llm, menu as menu_mod, whatsapp

ORDERS_FILE = Path(__file__).parent.parent / "data" / "orders.json"

# In-memory conversation state: phone -> {stage, pending_order}
_sessions: Dict[str, dict] = {}


def _load_orders() -> dict:
    with open(ORDERS_FILE) as f:
        return json.load(f)


def _save_orders(data: dict) -> None:
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _next_order_id() -> str:
    data = _load_orders()
    data["counter"] += 1
    _save_orders(data)
    return f"CDC-{data['counter']:03d}"


def _save_order(order: dict) -> None:
    data = _load_orders()
    data["orders"].append(order)
    _save_orders(data)


def handle_message(from_phone: str, message_body: str) -> str:
    """Process an inbound WhatsApp message and return the reply text."""
    from agents import broadcast as bc_mod
    bc_mod.add_customer(from_phone, is_regular=False)

    session = _sessions.get(from_phone, {"stage": "idle"})
    body = message_body.strip()

    available = menu_mod.get_available()
    available_str = ", ".join(
        f"{k} (${v['price']:.0f})" for k, v in available.items()
    )

    # Parse intent with Gemini
    parse_prompt = (
        f"El cliente envió: '{body}'\n"
        f"Menú disponible: {available_str}\n\n"
        f"Analiza el mensaje y responde con JSON:\n"
        f'{{"intent": "order"|"inquiry"|"greeting"|"other", '
        f'"items": [{{"name": "...", "qty": 1}}], '
        f'"delivery_time": "...", "address": "...", "payment": "..."}}\n'
        f"Solo JSON, sin texto adicional."
    )
    raw = llm.ask(parse_prompt)
    try:
        # Extract JSON from the response
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        parsed = json.loads(json_match.group()) if json_match else {}
    except Exception:
        parsed = {}

    intent = parsed.get("intent", "other")

    if intent == "greeting":
        _sessions[from_phone] = {"stage": "idle"}
        return (
            f"¡Hola! 👋 Bienvenido a *Cocina de Casa* — Winston-Salem, NC 🇨🇴\n\n"
            f"{menu_mod.format_menu_es()}\n\n"
            f"¿Qué te provoca hoy? Dime qué quieres pedir 😊"
        )

    if intent == "inquiry":
        reply_prompt = (
            f"Responde la pregunta del cliente: '{body}'\n"
            f"Información: Cocina de Casa, Winston-Salem NC. "
            f"Menú disponible: {available_str}. "
            f"Entregamos a domicilio. Pagos: Zelle, efectivo. "
            f"Responde en el mismo idioma del cliente. Máximo 3 oraciones."
        )
        return llm.ask(reply_prompt, system=llm.SYSTEM_VOICE)

    if intent == "order":
        items = parsed.get("items", [])
        if not items:
            return (
                "¿Qué te gustaría pedir? Dime el plato y la cantidad 🍽️\n"
                "Ejemplo: 'Una bandeja paisa y dos jugos'"
            )

        # Validate and deduct stock
        confirmed_items = []
        unavailable = []
        for item_req in items:
            name = item_req.get("name", "")
            qty = int(item_req.get("qty", 1))
            if menu_mod.decrement(name, qty):
                # Find the canonical name and price
                menu = menu_mod.load()
                from agents.menu import _find_key
                key = _find_key(menu, name)
                price = menu[key]["price"] if key else 0
                confirmed_items.append({"name": key or name, "qty": qty, "price": price})
            else:
                unavailable.append(name)

        if unavailable:
            return (
                f"Lo siento, ya no tenemos: {', '.join(unavailable)} 😔\n"
                f"¿Quieres pedir algo más del menú?"
            )

        # Build order
        address = parsed.get("address", "")
        delivery_time = parsed.get("delivery_time", "")
        payment = parsed.get("payment", "")

        if not address or not delivery_time:
            # Store partial order and ask for missing info
            _sessions[from_phone] = {
                "stage": "awaiting_details",
                "pending_items": confirmed_items,
            }
            return (
                "¡Perfecto! Tengo tu pedido 📝\n"
                "Para confirmar, necesito:\n"
                "1️⃣ Dirección de entrega\n"
                "2️⃣ Hora de entrega\n"
                "3️⃣ Método de pago (Zelle o efectivo)"
            )

        return _finalize_order(from_phone, confirmed_items, address, delivery_time, payment)

    # Awaiting delivery details
    if session.get("stage") == "awaiting_details":
        pending_items = session.get("pending_items", [])
        detail_prompt = (
            f"El cliente respondió: '{body}'\n"
            f"Extrae del texto: dirección, hora de entrega, método de pago.\n"
            f'Responde solo JSON: {{"address": "...", "delivery_time": "...", "payment": "..."}}'
        )
        raw2 = llm.ask(detail_prompt)
        try:
            json_match2 = re.search(r'\{.*\}', raw2, re.DOTALL)
            details = json.loads(json_match2.group()) if json_match2 else {}
        except Exception:
            details = {}

        address = details.get("address", body)
        delivery_time = details.get("delivery_time", "lo antes posible")
        payment = details.get("payment", "no especificado")

        _sessions[from_phone] = {"stage": "idle"}
        return _finalize_order(from_phone, pending_items, address, delivery_time, payment)

    # Default fallback
    return (
        f"¡Hola! Soy el asistente de *Cocina de Casa* 🍽️\n"
        f"Escríbeme qué quieres pedir o responde 'Menú' para ver lo disponible hoy."
    )


def _finalize_order(
    phone: str, items: list, address: str, delivery_time: str, payment: str
) -> str:
    order_id = _next_order_id()
    total = sum(i["price"] * i["qty"] for i in items)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    order = {
        "id": order_id,
        "phone": phone,
        "items": items,
        "address": address,
        "delivery_time": delivery_time,
        "payment": payment,
        "total": total,
        "timestamp": now,
        "status": "confirmed",
    }
    _save_order(order)

    items_str = "\n".join(
        f"  • {i['qty']}x {i['name']} — ${i['price'] * i['qty']:.0f}" for i in items
    )

    # Customer confirmation
    customer_msg = (
        f"✅ *Pedido confirmado — {order_id}*\n\n"
        f"{items_str}\n\n"
        f"💰 Total: ${total:.0f}\n"
        f"📍 Entrega: {address}\n"
        f"🕐 Hora: {delivery_time}\n"
        f"💳 Pago: {payment}\n\n"
        f"¡Gracias! Te avisamos cuando salga tu pedido 🛵\n"
        f"— Cocina de Casa, Winston-Salem NC"
    )

    # Owner notification
    owner_msg = (
        f"🔔 *NUEVO PEDIDO — {order_id}*\n\n"
        f"{items_str}\n\n"
        f"💰 Total: ${total:.0f}\n"
        f"📞 Cliente: +{phone}\n"
        f"📍 Dirección: {address}\n"
        f"🕐 Entrega: {delivery_time}\n"
        f"💳 Pago: {payment}\n"
        f"🕒 Recibido: {now}"
    )
    whatsapp.notify_owner(owner_msg)

    _sessions[phone] = {"stage": "idle"}
    return customer_msg


def daily_summary() -> str:
    """20:30 — Build and send day summary to owner."""
    data = _load_orders()
    today = datetime.now().strftime("%Y-%m-%d")
    today_orders = [o for o in data["orders"] if o["timestamp"].startswith(today)]

    total_revenue = sum(o["total"] for o in today_orders)
    count = len(today_orders)

    if count == 0:
        summary = (
            f"📊 *Resumen del día — Cocina de Casa*\n"
            f"Fecha: {today}\n\n"
            f"Sin pedidos hoy 😔\n"
            f"Mañana será mejor! 💪"
        )
    else:
        item_counts: Dict[str, int] = {}
        for o in today_orders:
            for i in o["items"]:
                item_counts[i["name"]] = item_counts.get(i["name"], 0) + i["qty"]

        top_items = sorted(item_counts.items(), key=lambda x: -x[1])
        top_str = "\n".join(f"  • {name}: {qty}x" for name, qty in top_items[:5])

        summary = (
            f"📊 *Resumen del día — Cocina de Casa*\n"
            f"Fecha: {today}\n\n"
            f"✅ Pedidos: {count}\n"
            f"💰 Recaudado: ${total_revenue:.0f}\n\n"
            f"🏆 Más vendidos:\n{top_str}\n\n"
            f"¡Buen trabajo papá! 🎉"
        )

    whatsapp.notify_owner(summary)
    return summary
