import os
from dotenv import load_dotenv

load_dotenv()

# Meta WhatsApp Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "cdc_verify_token_secret")

# Meta Graph API (Facebook + Instagram)
META_PAGE_ACCESS_TOKEN = os.getenv("META_PAGE_ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")

# Fireworks AI (Gemma, hosted on AMD hardware)
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY", "")
FIREWORKS_MODEL = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/gemma-3-27b-it")
FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"

# Owner WhatsApp (digits only, no +)
OWNER_WHATSAPP = os.getenv("OWNER_WHATSAPP", "")

PORT = int(os.getenv("PORT", "8080"))

RESTAURANT_NAME = "Cocina de Casa"
RESTAURANT_CITY = "Winston-Salem, NC"
TIMEZONE = "America/New_York"

META_API_VERSION = "v19.0"
GRAPH_BASE = f"https://graph.facebook.com/{META_API_VERSION}"
WHATSAPP_API_URL = f"{GRAPH_BASE}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
