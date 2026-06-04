import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

import config

logger = logging.getLogger(__name__)
_tz = pytz.timezone(config.TIMEZONE)


def _job(name: str, fn):
    def wrapper():
        try:
            logger.info("▶ Running scheduled job: %s", name)
            fn()
            logger.info("✓ Finished: %s", name)
        except Exception as e:
            logger.error("✗ Error in %s: %s", name, e)
    wrapper.__name__ = name
    return wrapper


def build_scheduler() -> BackgroundScheduler:
    from agents import menu as menu_mod, inventory, broadcast, ordering, social

    scheduler = BackgroundScheduler(timezone=_tz)

    # 09:00 — Reset daily menu quantities
    scheduler.add_job(
        _job("menu_reset", menu_mod.reset_daily),
        CronTrigger(hour=9, minute=0, timezone=_tz),
        id="menu_reset",
    )

    # 09:15 — Post daily special to Facebook/Instagram
    scheduler.add_job(
        _job("social_post", social.publish_daily_special),
        CronTrigger(hour=9, minute=15, timezone=_tz),
        id="social_post",
    )

    # 09:30 — WhatsApp broadcast to regular customers
    scheduler.add_job(
        _job("broadcast_regulars", broadcast.morning_broadcast_regulars),
        CronTrigger(hour=9, minute=30, timezone=_tz),
        id="broadcast_regulars",
    )

    # 11:00 — Inventory low-stock alert to owner
    def inventory_alert():
        from agents import whatsapp as wa
        msg = inventory.check_low_stock()
        if msg:
            wa.notify_owner(msg)

    scheduler.add_job(
        _job("inventory_alert", inventory_alert),
        CronTrigger(hour=11, minute=0, timezone=_tz),
        id="inventory_alert",
    )

    # 14:00 — "Se está agotando" urgency broadcast
    def urgency_broadcast():
        from agents import whatsapp as wa, broadcast as bc
        msg = inventory.urgency_message()
        if msg:
            customers = bc.load_customers()
            all_phones = customers["regulars"] + customers["new_leads"]
            bc.broadcast_to(all_phones, msg)

    scheduler.add_job(
        _job("urgency_broadcast", urgency_broadcast),
        CronTrigger(hour=14, minute=0, timezone=_tz),
        id="urgency_broadcast",
    )

    # 16:00 — Afternoon broadcast to new leads
    scheduler.add_job(
        _job("broadcast_new", broadcast.afternoon_broadcast_new),
        CronTrigger(hour=16, minute=0, timezone=_tz),
        id="broadcast_new",
    )

    # 19:30 — Last orders of the day
    scheduler.add_job(
        _job("last_orders", broadcast.last_orders_broadcast),
        CronTrigger(hour=19, minute=30, timezone=_tz),
        id="last_orders",
    )

    # 20:30 — Daily summary to owner
    scheduler.add_job(
        _job("daily_summary", ordering.daily_summary),
        CronTrigger(hour=20, minute=30, timezone=_tz),
        id="daily_summary",
    )

    return scheduler
