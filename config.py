import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENCLAW_WEBHOOK_URL = os.getenv("OPENCLAW_WEBHOOK_URL")
    SMART_LIGHT_API_URL = os.getenv("SMART_LIGHT_API_URL")
    OPENCLAW_HOOK_TOKEN = os.getenv("OPENCLAW_HOOK_TOKEN")
    MAX_DEPLOY_MINUTES = int(os.getenv("MAX_DEPLOY_MINUTES", 15))

    # Check if missing
    @staticmethod
    def validate():
        if not Config.OPENCLAW_WEBHOOK_URL:
            raise ValueError("Missing OPENCLAW_WEBHOOK_URL")
        if not Config.SMART_LIGHT_API_URL:
            raise ValueError("Missing SMART_LIGHT_API_URL")
        if not Config.OPENCLAW_HOOK_TOKEN:
            raise ValueError("Missing OPENCLAW_HOOK_TOKEN")
        
