import requests
from config import TELEGRAM_ENABLED, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(msg):
    if not TELEGRAM_ENABLED:
        print(f"TELEGRAM (Disabled): {msg}")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        }, timeout=10)
    except Exception as e:
        print(f"Failed to send telegram message: {e}")
