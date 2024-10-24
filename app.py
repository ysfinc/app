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
        # Mesaj Gövdesi
        message = response.message("Lütfen aşağıdaki seçeneklerden birini yazın:\n"
                                   "1. Yapboz Sigortası\n"
                                   "2. Trafik Sigortası\n"
                                   "3. İş Yeri Sigortası\n"
                                   "4. Dask Sigortası\n"
                                   "5. Diğer İşlemler")

    return str(response)

if __name__ == "__main__":
    # Render'ın verdiği PORT numarasını kullanıyoruz
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
