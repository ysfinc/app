import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Müşteri temsilcisi API URL'leri (örnek URL'ler)
YAPBOZ_ENDPOINT = "https://example.com/api/yapboz"
TRAFIK_ENDPOINT = "https://example.com/api/trafik"
IS_YERI_ENDPOINT = "https://example.com/api/is_yeri"
DASK_ENDPOINT = "https://example.com/api/dask"

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()

    # Kullanıcıdan gelen mesajlara göre yanıtlar
    if '1' in incoming_msg or 'yapboz' in incoming_msg:
        response.message("🧩 Yapboz Sigortası, evinizdeki riskleri kapsamaktadır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)\nMüşteri temsilcisine bağlanmak ister misiniz? (Evet/Hayır)")
    elif '2' in incoming_msg or 'trafik' in incoming_msg:
        response.message("🚗 Trafik Sigortası, araç kazaları ve hasarlar için zorunlu bir sigortadır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)\nMüşteri temsilcisine bağlanmak ister misiniz? (Evet/Hayır)")
    elif '3' in incoming_msg or 'iş yeri' in incoming_msg:
        response.message("🏢 İş Yeri Sigortası, iş yerinizi çeşitli risklere karşı güvence altına alır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)\nMüşteri temsilcisine bağlanmak ister misiniz? (Evet/Hayır)")
    elif '4' in incoming_msg or 'dask' in incoming_msg:
        response.message("🌍 DASK Sigortası, doğal afetlere karşı zorunlu deprem sigortasıdır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)\nMüşteri temsilcisine bağlanmak ister misiniz? (Evet/Hayır)")
    elif 'evet' in incoming_msg:
        # Müşteri temsilcisine bağlanma isteği varsa uygun API'ye yönlendir
        if 'yapboz' in incoming_msg:
            requests.post(YAPBOZ_ENDPOINT, json={"message": "Yeni Yapboz Sigortası talebi alındı.", "customer": request.values.get('From')})
        elif 'trafik' in incoming_msg:
            requests.post(TRAFIK_ENDPOINT, json={"message": "Yeni Trafik Sigortası talebi alındı.", "customer": request.values.get('From')})
        elif 'iş yeri' in incoming_msg:
            requests.post(IS_YERI_ENDPOINT, json={"message": "Yeni İş Yeri Sigortası talebi alındı.", "customer": request.values.get('From')})
        elif 'dask' in incoming_msg:
            requests.post(DASK_ENDPOINT, json={"message": "Yeni DASK Sigortası talebi alındı.", "customer": request.values.get('From')})

        response.message("📄 Lütfen gerekli belgeleri hazırlayın ve bizimle iletişime geçin. Ana menüye dönmek için 'Ana Menü' yazabilirsiniz.")
    elif 'hayır' in incoming_msg:
        response.message("Teşekkürler! Başka bir konuda yardımcı olabilir miyim? Ana menüye dönmek için 'Ana Menü' yazabilirsiniz.")
    elif 'ana menü' in incoming_msg:
        response.message("Lütfen aşağıdaki seçeneklerden birini yazın:\n"
                         "1. 🧩 Yapboz Sigortası\n"
                         "2. 🚗 Trafik Sigortası\n"
                         "3. 🏢 İş Yeri Sigortası\n"
                         "4. 🌍 Dask Sigortası\n"
                         "5. Diğer İşlemler")
    else:
        response.message("Lütfen aşağıdaki seçeneklerden birini yazın:\n"
                         "1. 🧩 Yapboz Sigortası\n"
                         "2. 🚗 Trafik Sigortası\n"
                         "3. 🏢 İş Yeri Sigortası\n"
                         "4. 🌍 Dask Sigortası\n"
                         "5. Diğer İşlemler")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
