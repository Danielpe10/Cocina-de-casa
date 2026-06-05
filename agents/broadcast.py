import json
from pathlib import Path
from typing import List
from agents import whatsapp, menu as menu_mod

CUSTOMERS_FILE = Path(__file__).parent.parent / "data" / "customers.json"


def load_customers() -> dict:
    with open(CUSTOMERS_FILE) as f:
        return json.load(f)


def add_customer(phone: str, is_regular: bool = False) -> None:
    customers = load_customers()
    list_key = "regulars" if is_regular else "new_leads"
    if phone not in customers[list_key]:
        customers[list_key].append(phone)
        with open(CUSTOMERS_FILE, "w") as f:
            json.dump(customers, f, indent=2)


def broadcast_to(phones: List[str], message: str) -> dict:
    results = {}
    for phone in phones:
        try:
            whatsapp.send_text(phone, message)
            results[phone] = "sent"
        except Exception as e:
            results[phone] = f"error: {e}"
    return results


def morning_broadcast_regulars():
    """09:30 — Send daily menu to regular customers."""
    customers = load_customers()
    if not customers["regulars"]:
        return
    msg = menu_mod.format_menu_es()
    broadcast_to(customers["regulars"], msg)


def afternoon_broadcast_new():
    """16:00 — Afternoon promo to new leads."""
    customers = load_customers()
    if not customers["new_leads"]:
        return
    available = menu_mod.get_available()
    if not available:
        return
    highlight = list(available.items())[0]
    name, info = highlight
    msg = (
        f"🍴 *Cocina de Casa — Winston-Salem, NC*\n\n"
        f"¡Aún tenemos {name} por ${info['price']:.0f}! 🔥\n"
        f"Escríbenos para pedir — entregamos a domicilio.\n\n"
        f"Still have {name} for ${info['price']:.0f}! DM us to order 🏠"
    )
    broadcast_to(customers["new_leads"], msg)


def last_orders_broadcast():
    """19:30 — Last call for orders."""
    customers = load_customers()
    all_phones = customers["regulars"] + customers["new_leads"]
    if not all_phones:
        return
    msg = (
        "🕰️ *¡Últimos pedidos del día!* — Cocina de Casa\n"
        "La cocina cierra pronto. ¿Quieres cenar rico esta noche?\n"
        "Escríbenos YA y pedimos tu domicilio 🛵\n\n"
        "🕰️ *Last orders tonight!* — Cocina de Casa\n"
        "Kitchen closes soon. Message us now to order delivery 🛵"
    )
    broadcast_to(all_phones, msg)
