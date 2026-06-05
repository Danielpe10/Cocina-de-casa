from typing import Optional
from agents import menu as menu_mod


def check_low_stock(threshold: int = 3) -> Optional[str]:
    """Return an owner alert message if items are running low, else None."""
    low = menu_mod.get_low_stock(threshold)
    if not low:
        return None
    lines = ["⚠️ *Alerta de inventario bajo — Cocina de Casa*\n"]
    for name, info in low.items():
        lines.append(f"• {name}: {info['available']} restantes")
    lines.append("\n¿Quieres pausar algún plato?")
    return "\n".join(lines)


def urgency_message() -> Optional[str]:
    """Return a customer-facing urgency broadcast for low-stock items."""
    low = menu_mod.get_low_stock(threshold=4)
    if not low:
        return None
    items_es = ", ".join(low.keys())
    items_en = items_es
    msg = (
        f"🔥 *¡Se están agotando!* — {items_es}\n"
        f"Quedan poquitos — pide ahora antes de que se acaben 👇\n\n"
        f"🔥 *Selling out fast!* — {items_en}\n"
        f"Only a few left — order now before they're gone 👇"
    )
    return msg
