import json
import os
from pathlib import Path
from typing import Optional

MENU_FILE = Path(__file__).parent.parent / "data" / "menu.json"


def load() -> dict:
    with open(MENU_FILE) as f:
        return json.load(f)


def save(menu: dict) -> None:
    with open(MENU_FILE, "w") as f:
        json.dump(menu, f, indent=2)


def reset_daily():
    """Restore each item to its default_qty at start of day."""
    menu = load()
    for item in menu.values():
        item["available"] = item["default_qty"]
    save(menu)


def decrement(item_name: str, qty: int = 1) -> bool:
    """Reduce available quantity. Returns False if not enough stock."""
    menu = load()
    # fuzzy match: allow partial name matching
    key = _find_key(menu, item_name)
    if key is None:
        return False
    if menu[key]["available"] < qty:
        return False
    menu[key]["available"] -= qty
    save(menu)
    return True


def get_available() -> dict:
    return {k: v for k, v in load().items() if v["available"] > 0}


def get_low_stock(threshold: int = 3) -> dict:
    return {k: v for k, v in load().items() if 0 < v["available"] <= threshold}


def format_menu_es() -> str:
    menu = get_available()
    lines = ["🍽️ *Menú del día — Cocina de Casa*\n"]
    for name, info in menu.items():
        lines.append(f"• {name} — ${info['price']:.0f}")
    lines.append("\n📍 Winston-Salem, NC | 📞 WhatsApp para pedir")
    return "\n".join(lines)


def format_menu_en() -> str:
    menu = get_available()
    lines = ["🍽️ *Today's Menu — Cocina de Casa*\n"]
    for name, info in menu.items():
        lines.append(f"• {name} — ${info['price']:.0f}")
    lines.append("\n📍 Winston-Salem, NC | 📞 WhatsApp to order")
    return "\n".join(lines)


def _find_key(menu: dict, name: str) -> Optional[str]:
    name_lower = name.lower()
    for key in menu:
        if key.lower() == name_lower or name_lower in key.lower():
            return key
    return None
