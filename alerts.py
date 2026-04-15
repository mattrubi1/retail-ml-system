import os
import requests

MAX_LENGTH = 4000  # Telegram limit safety


def send_alert(message):

    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    print("🔔 Attempting Telegram send...")

    if not bot_token:
        print("❌ BOT_TOKEN missing")
        return

    if not chat_id:
        print("❌ CHAT_ID missing")
        return

    print("✅ BOT_TOKEN loaded")
    print("✅ CHAT_ID loaded")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # =========================
    # SPLIT MESSAGE INTO CHUNKS
    # =========================
    chunks = []

    temp_message = message

    while len(temp_message) > MAX_LENGTH:
        split_index = temp_message[:MAX_LENGTH].rfind("\n")
        if split_index == -1:
            split_index = MAX_LENGTH

        chunks.append(temp_message[:split_index])
        temp_message = temp_message[split_index:]

    chunks.append(temp_message)

    print(f"DEBUG: Sending {len(chunks)} chunks")

    # =========================
    # SEND EACH CHUNK
    # =========================
    for i, chunk in enumerate(chunks):

        payload = {
            "chat_id": chat_id,
            "text": chunk
        }

        try:
            response = requests.post(url, data=payload)

            if response.status_code == 200:
                print(f"✅ Chunk {i+1}/{len(chunks)} sent")
            else:
                print("❌ Telegram failed:", response.text)

        except Exception as e:
            print("❌ Telegram error:", str(e))
