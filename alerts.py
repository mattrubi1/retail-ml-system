import requests
import os
import time

# =========================
# TELEGRAM CONFIG
# =========================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# =========================
# SAFETY CHECK
# =========================
if not TOKEN or not CHAT_ID:
    print("❌ Missing BOT_TOKEN or CHAT_ID environment variables")


# =========================
# MESSAGE SENDER
# =========================
def send_alert(message: str):

    if not TOKEN or not CHAT_ID:
        print("❌ Telegram not configured properly")
        return

    # Telegram hard limit ~4096 chars → we stay safe under it
    MAX_CHUNK = 3500

    chunks = [
        message[i:i + MAX_CHUNK]
        for i in range(0, len(message), MAX_CHUNK)
    ]

    for chunk in chunks:

        payload = {
            "chat_id": CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(BASE_URL, data=payload, timeout=10)

            if response.status_code != 200:
                print("❌ Telegram Error:", response.text)

            time.sleep(0.3)  # prevents rate limits

        except Exception as e:
            print("❌ Telegram Exception:", str(e))
