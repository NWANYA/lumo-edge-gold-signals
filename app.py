import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@app.route("/")
def home():
    return jsonify({
        "bot": "Lumo Edge Gold Signals",
        "status": "online",
        "message": "Gold signals service is running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram credentials are not configured.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json().get("ok", False)

    except requests.RequestException as error:
        print(f"Telegram error: {error}")
        return False


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
