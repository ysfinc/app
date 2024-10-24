import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Müşteri temsilcisi WhatsApp grup numaraları (örnek grup numaraları)
YAPBOZ_WHATSAPP_GROUP = "whatsapp:+12345678901"
TRAFIK_WHATSAPP_GROUP = "whatsapp:+12345678902"
IS_YERI_WHATSAPP_GROUP = "whatsapp:+12345678903"
DASK_WHATSAPP_GROUP = "whatsapp:+12345678904"

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    customer_number = request.values.get('From')

    # Kullanıcıdan gelen mesajlara göre yanıtlar ve müşteri temsilcisine yönlendirme
    if '1' in incoming_msg or 'yapboz' in incoming_msg:
        response.message("🧩 Yapboz Sigortası, evinizdeki riskleri kapsamaktadır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '2' in incoming_msg or 'trafik' in incoming_msg:
        response.message("🚗 Trafik Sigortası, araç kazaları ve hasarlar için zorunlu bir sigortadır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '3' in incoming_msg or 'iş yeri' in incoming_msg:
        response.message("🏢 İş Yeri Sigortası, iş yerinizi çeşitli risklere karşı güvence altına alır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '4' in incoming_msg or 'dask' in incoming_msg:
        response.message("🌍 DASK Sigortası, doğal afetlere karşı zorunlu deprem sigortasıdır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif 'evet' in incoming_msg:
        response.message("📄 Lütfen gerekli belgeleri hazırlayın ve bizimle iletişime geçin. Ana menüye dönmek için 'Ana Menü' yazabilirsiniz.")
        # Belgeleri ilgili WhatsApp grubuna iletme
        if 'yapboz' in incoming_msg:
            requests.post("https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.getenv("TWILIO_ACCOUNT_SID")),
                          data={"To": YAPBOZ_WHATSAPP_GROUP, "From": customer_number, "Body": "Müşteriden gelen belgeler: ..."},
                          auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
        elif 'trafik' in incoming_msg:
            requests.post("https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.getenv("TWILIO_ACCOUNT_SID")),
                          data={"To": TRAFIK_WHATSAPP_GROUP, "From": customer_number, "Body": "Müşteriden gelen belgeler: ..."},
                          auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
        elif 'iş yeri' in incoming_msg:
            requests.post("https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.getenv("TWILIO_ACCOUNT_SID")),
                          data={"To": IS_YERI_WHATSAPP_GROUP, "From": customer_number, "Body": "Müşteriden gelen belgeler: ..."},
                          auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
        elif 'dask' in incoming_msg:
            requests.post("https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.getenv("TWILIO_ACCOUNT_SID")),
                          data={"To": DASK_WHATSAPP_GROUP, "From": customer_number, "Body": "Müşteriden gelen belgeler: ..."},
                          auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")))
    elif 'hayır' in incoming_msg:
        response.message("Teşekkürler! Başka bir konuda yardımcı olabilir miyim? Ana menüye dönmek için 'Ana Menü' yazabilirsiniz.")
    elif 'ana menü' in incoming_msg:
        response.message("Lütfen aşağıdaki seçeneklerden birini yazın:
"
                         "1. 🧩 Yapboz Sigortası
"
                         "2. 🚗 Trafik Sigortası
"
                         "3. 🏢 İş Yeri Sigortası
"
                         "4. 🌍 Dask Sigortası
"
                         "5. Diğer İşlemler
"
                         "6. Görüşmeyi Sonlandır")
    elif 'görüşmeyi sonlandır' in incoming_msg:
        response.message("Görüşmeyi sonlandırdınız. Müşteri temsilcimizi 1 ile 5 arasında değerlendirmenizi rica ederiz. (1: Çok Kötü, 5: Mükemmel)")
    elif incoming_msg in ['1', '2', '3', '4', '5']:
        response.message("Teşekkürler! Değerlendirmeniz bizim için çok değerli.")
    else:
        response.message("Lütfen aşağıdaki seçeneklerden birini yazın:
"
                         "1. 🧩 Yapboz Sigortası
"
                         "2. 🚗 Trafik Sigortası
"
                         "3. 🏢 İş Yeri Sigortası
"
                         "4. 🌍 Dask Sigortası
"
                         "5. Diğer İşlemler
"
                         "6. Görüşmeyi Sonlandır")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
