import subprocess
import requests
from datetime import datetime
from config import Config

def send_alerts(reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[Server Alert - {timestamp}] {reason}"

    # Send chat notification to Telegram via OpenClaw
    if Config.OPENCLAW_WEBHOOK_URL and Config.OPENCLAW_HOOK_TOKEN:
        openclaw_payload = {
            "message": msg,
            "name": "DeploymentMonitoring",
            "deliver": True,
            "channel": "telegram"
        }

        headers = {
            "Authorization": f"Bearer {Config.OPENCLAW_HOOK_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                Config.OPENCLAW_WEBHOOK_URL,
                json=openclaw_payload,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            print(f"Chat alert sent to OpenClaw successfully: {reason}")
        except Exception as e:
            print("Failed to send OpenClaw notification:", e)

    # Direct Telegram Bot API fallback
    if Config.TELEGRAM_BOT_TOKEN and Config.TELEGRAM_CHAT_ID:
        telegram_url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
        tg_payload = {
            "chat_id": Config.TELEGRAM_CHAT_ID,
            "text": msg
        }
        try:
            tg_resp = requests.post(telegram_url, json=tg_payload, timeout=5)
            tg_resp.raise_for_status()
            print(f"Direct Telegram alert sent successed: {reason}")
        except Exception as e:
            print("Failed to send direct Telegram notification:", e)

    # Physical alert on home smart light / plug
    light_payload = {
        "status": "on",
        "color": "red",
        "brightness": 100
    }

    try:
        response = requests.post(
            Config.SMART_LIGHT_API_URL,
            json=light_payload,
            timeout=5
        )
        response.raise_for_status()
        print(f"Smart light notification sent successfully: {reason}")
    except Exception as e:
        print("Failed to send smart light notification:", e)

# Backward-compatibility alias
auto_alert = send_alerts

def monitor_runners():
    print("Checking GitHub Actions service and deployment status...")
    
    try:
        result = subprocess.run(
            ["sudo", "./svc.sh", "status"],
            cwd="/home/minipc/actions-runner", 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        if "active (running)" not in result.stdout:
            send_alerts("GitHub Actions runner service is stopped or inactive!")
        else:
            print("Runner service is healthy.")
    except Exception as e:
        error_msg = f"Failed to check GitHub Actions runner status: {e}"
        print(error_msg)
        send_alerts(error_msg)

if __name__ == "__main__":
    try:
        Config.validate()
        monitor_runners()
    except Exception as err:
        print(f"Initialization error: {err}")