import time
import subprocess
import requests
from datetime import datetime
from config import Config

def auto_alert(reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Send chat nofi telegram
    payload = {
        "event": "deployments_alert",
        "msg": f" [Server Alert - {timestamp}] {reason}"
    }
    
    try:
        requests.post(
            Config.OPENCLAW_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        print(f"Chat alert send successed : {reason}")
    except Exception as e:
        print("Failed to send OpenClaw notification:", e)


    # tracked on smart light home
    ligth_payload = {
        "status": "on",
        "color": "red",
        "brightness": 100
    }

    try:
        requests.post(
            Config.SMART_LIGHT_API_URL,
            json=ligth_payload,
            timeout=5
        )
        print(f"Smart light notification send successed : {reason}")
    except Exception as e:
        print("Failed to send smart light notification:", e)

def monitor_runners():
    print("Checking github-actions services and deployment status")
    
    result = subprocess.run(["sudo", "./svc.sh", "status"], cwd="/home/minipc/actions-runner", capture_output=True, text=True)
    
    if "active (running)" not in result.stdout:
        auto_alert("GitHub Actions runner service is stopped or inactive!")
    else:
        print("Runner service is healthy.")

if __name__ == "__main__":
    monitor_runners()