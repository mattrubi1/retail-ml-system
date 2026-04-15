import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_alert(message: str):

    print("🔔 Attempting Telegram send...")

    # =========================
    # CHECK CONFIG
    # =========================
    if not TOKEN:
        print("❌ BOT_TOKEN missing")
        return

    if not CHAT_ID:
        print("❌ CHAT_ID missing")
        return

    print("✅ Token + Chat ID found")

    # =========================
    # SPLIT SAFE
    # =========================
    chunks = [message[i:i+3500] for i in range(0, len(message), 3500)]

    for i, chunk in enumerate(chunks):

        payload = {
            "chat_id": CHAT_ID,
            "text": chunk
        }

        try:
            response = requests.post(BASE_URL, data=payload, timeout=10)

            print(f"📤 Sent chunk {i+1}/{len(chunks)}")
            print("Status:", response.status_code)
            print("Response:", response.text)

        except Exception as e:
            print("❌ Telegram request failed:", str(e))
