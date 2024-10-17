import requests
import sqlite3
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse, Message
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

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    resp = MessagingResponse()
    
    # Mesajı Veritabanına Kaydetme
    c.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (from_number, incoming_msg))
    conn.commit()

    if "menu" in incoming_msg:
        # Kullanıcıya interaktif butonlar gönder
        send_interactive_menu(resp)
    elif "hava" in incoming_msg:
        weather_info = get_weather()
        resp.message(weather_info)
    elif "döviz" in incoming_msg:
        exchange_info = get_exchange_rate()
        resp.message(exchange_info)
    else:
        chat_response = chat_with_gpt(incoming_msg)
        resp.message(chat_response)

    return str(resp)

def send_interactive_menu(resp):
    """Kullanıcıya interaktif menü gönderir."""
    msg = Message()
    msg.body("Merhaba! Aşağıdaki seçeneklerden birini seçin:")
    
    # Interaktif Butonlar
    msg.add_button("Hava Durumu", "hava")
    msg.add_button("Döviz Kuru", "döviz")
    msg.add_button("ChatGPT ile Sohbet", "sohbet")

    resp.append(msg)

def get_weather():
    """OpenWeatherMap API'den hava durumu bilgisi getirir."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Ankara&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        return "Hava durumu bilgisine ulaşılamadı."
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"Ankara'da hava {description}, sıcaklık {temp}°C."

def get_exchange_rate():
    """ExchangeRate API'den döviz kuru bilgisi getirir."""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/USD"
    response = requests.get(url)
    data = response.json()
    if data["result"] != "success":
        return "Döviz kuru bilgisine ulaşılamadı."
    try:
        tl_rate = data["conversion_rates"]["TRY"]
        return f"1 USD = {tl_rate} TL"
    except KeyError:
        return "Döviz kuru bilgisi bulunamadı."

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
