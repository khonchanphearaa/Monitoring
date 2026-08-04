import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENCLAW_WEBHOOK_URL = os.getenv("OPENCLAW_WEBHOOK_URL", "http://localhost:18789/hooks/agent")
    SMART_LIGHT_API_URL = os.getenv("SMART_LIGHT_API_URL")
    OPENCLAW_HOOK_TOKEN = os.getenv("OPENCLAW_HOOK_TOKEN")
    MAX_DEPLOY_MINUTES = int(os.getenv("MAX_DEPLOY_MINUTES", 15))
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # Check if missing
    @staticmethod
    def validate():
        if not Config.SMART_LIGHT_API_URL:
            raise ValueError("Missing SMART_LIGHT_API_URL in environment configuration.")


