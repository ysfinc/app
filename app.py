import requests
import sqlite3
from flask import Flask, request
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

# Mesajları Kaydetmek İçin Tablo Oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS messages (user TEXT, message TEXT)''')
conn.commit()

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
    if "menu" in incoming_msg:
        msg.body("Merhaba! Seçenekler:\n1. 🌦 Hava Durumu\n2. 💸 Döviz Kuru\n3. 🤖 Sohbet")
    elif "hava" in incoming_msg:
        weather_info = get_weather()
        msg.body(weather_info)
    elif "döviz" in incoming_msg:
        exchange_info = get_exchange_rate()
        msg.body(exchange_info)
    else:
        chat_response = chat_with_gpt(incoming_msg)
        msg.body(chat_response)

    return str(resp)

# Hava Durumu Fonksiyonu
def get_weather():
    """OpenWeatherMap API'den hava durumu bilgisi getirir."""
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
    """ExchangeRate API'den döviz kuru bilgisi getirir."""
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

# ChatGPT Yanıtı Fonksiyonu
def chat_with_gpt(user_message):
    """OpenAI API ile ChatGPT üzerinden akıllı yanıt döndürür."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Uygulamayı Başlatma
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
