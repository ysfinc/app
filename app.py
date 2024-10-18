import requests
import sqlite3
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai

# API Anahtarları
OPENWEATHER_API_KEY = "your_openweather_api_key"
EXCHANGERATE_API_KEY = "your_exchangerate_api_key"
openai.api_key = "your_openai_api_key"

app = Flask(__name__)

# SQLite Veritabanı Bağlantısı
conn = sqlite3.connect("messages.db", check_same_thread=False)
c = conn.cursor()

# Ana Sayfa Rotası (http://127.0.0.1:5000/)
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

# WhatsApp Rotası
@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    # Mesajı Veritabanına Kaydetme
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (from_number, incoming_msg))
    conn.commit()

    # Kullanıcıdan gelen mesajlara göre yanıt
    if incoming_msg == "1":
        msg.body(get_weather())
    elif incoming_msg == "2":
        msg.body(get_exchange_rate())
    elif incoming_msg == "3":
        msg.body("Sohbet etmek istediğiniz konuyu yazın:")
    else:
        msg.body(
            "Lütfen bir seçenek seçin:\n"
            "1. 🌦 Hava Durumu\n"
            "2. 💸 Döviz Kuru\n"
            "3. 🤖 Sohbet\n"
            "Yanıt olarak 1, 2 veya 3 yazabilirsiniz."
        )

    return str(resp)

# Hava Durumu Fonksiyonu
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Ankara&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return "Hava durumu bilgisine ulaşılamadı."
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"Ankara'da hava {description}, sıcaklık {temp}°C."

# Döviz Kuru Fonksiyonu
def get_exchange_rate():
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/USD"
    response = requests.get(url)
    data = response.json()
    if data.get("result") != "success":
        return "Döviz kuru bilgisine ulaşılamadı."
    try:
        tl_rate = data["conversion_rates"]["TRY"]
        return f"1 USD = {tl_rate} TL"
    except KeyError:
        return "Döviz kuru bilgisi bulunamadı."

# Uygulamayı Başlatma
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
