import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

import config
from agents.scheduler import build_scheduler
from webhook import app


def main():
    scheduler = build_scheduler()
    scheduler.start()
    logger.info("Scheduler started — 8 agents active (America/New_York)")
    logger.info("Starting webhook server on port %s", config.PORT)
    app.run(host="0.0.0.0", port=config.PORT)


if __name__ == "__main__":
    main()
