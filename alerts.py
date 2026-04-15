import requests

TOKEN = "8264216833:AAHFFfTVju6fY5ogTuenSUDQ5SutUs9DxN4"
CHAT_ID = "7938644912"

def send_alert(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": message
    })
