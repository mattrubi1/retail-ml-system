import os
import requests


def send_alert(message):

    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    print("🔔 Attempting Telegram send...")

    # =========================
    # DEBUG CHECK
    # =========================
    if not bot_token:
        print("❌ BOT_TOKEN missing")
        return

    if not chat_id:
        print("❌ CHAT_ID missing")
        return

    print("✅ BOT_TOKEN loaded")
    print("✅ CHAT_ID loaded")

    # =========================
    # SEND MESSAGE
    # =========================
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("✅ Telegram sent successfully")
        else:
            print("❌ Telegram failed:", response.text)

    except Exception as e:
        print("❌ Telegram error:", str(e))
