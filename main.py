import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Telegram Bot ma'lumotlari
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    return "CHoCH Bot Serveri Ishlamoqda!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Ma'lumot topilmadi"}), 400

    pair = data.get("pair", "Noma'lum")
    tf = data.get("timeframe", "M15")
    event = data.get("event", "CHoCH Signal")
    price = data.get("price", "-")

    msg = (
        f"🚨 **{event}**\n\n"
        f"📌 **Juftlik:** `{pair}`\n"
        f"⏱ **Taymfreym:** `{tf}`\n"
        f"💰 **Narx:** `{price}`"
    )

    send_telegram_message(msg)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
