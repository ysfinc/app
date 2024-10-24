from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Twilio kimlik bilgileri (Render üzerinde environment variables olarak ayarlanabilir)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio WhatsApp iş numaranız

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()

    if incoming_msg:
        message = response.message("Lütfen aşağıdaki seçeneklerden birini seçin:")
        message.media("https://example.com/sigorta-banner.jpg")  # İsteğe bağlı resim ekleme
        
        # Etkileşimli butonlar
        message.body("")
        message.action({
            "type": "quick_reply",  # Kullanıcının seçim yapabileceği butonlar
            "options": [
                {"label": "Yapboz Sigortası", "value": "yapboz"},
                {"label": "Trafik Sigortası", "value": "trafik"},
                {"label": "İş Yeri Sigortası", "value": "is_yeri"},
                {"label": "Dask Sigortası", "value": "dask"},
                {"label": "Diğer İşlemler", "value": "diger"}
            ]
        })
    
    return str(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
