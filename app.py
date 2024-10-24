import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Müşteri temsilcisi WhatsApp grup numaraları (ornek grup numaraları)
YAPBOZ_WHATSAPP_GROUP = "whatsapp:+12345678901"
TRAFIK_WHATSAPP_GROUP = "whatsapp:+12345678902"
IS_YERI_WHATSAPP_GROUP = "whatsapp:+12345678903"
DASK_WHATSAPP_GROUP = "whatsapp:+12345678904"

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    gelen_mesaj = request.values.get('Body', '').lower()
    yanit = MessagingResponse()
    musteri_numarasi = request.values.get('From')

    # Kullanıcıdan gelen mesajlara göre yanıtlar ve müşteri temsilcisine yönlendirme
    if '1' in gelen_mesaj or 'yapboz' in gelen_mesaj:
        yanit.message("✨ *Yapboz Sigortası*
Evinizdeki riskleri kapsar. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '2' in gelen_mesaj or 'trafik' in gelen_mesaj:
        yanit.message("🚗 *Trafik Sigortası*
Araç kazaları ve hasarlar için zorunlu bir sigortadır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '3' in gelen_mesaj or 'ış yeri' in gelen_mesaj:
        yanit.message("🏢 *İş Yeri Sigortası*
İş yerinizi çeşitli risklere karşı güvence altına alır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif '4' in gelen_mesaj or 'dask' in gelen_mesaj:
        yanit.message("🌍 *DASK Sigortası*
Doğal afetlere karşı zorunlu deprem sigortasıdır. Daha fazla bilgi almak ister misiniz? (Evet/Hayır)")
    elif 'evet' in gelen_mesaj:
        yanit.message("📄 Lütfen gerekli belgeleri hazırlayın:
- Kimlik fotokopisi
- Fatura belgesi
- Sigorta poliçesi

Müşteri temsilcisine bağlanıyor..." )
        yanit.message("Merhaba, ben müşteri temsilcisi Ahmet. Size nasıl yardımcı olabilirim?")
        # Belgeleri ilgili WhatsApp grubuna iletme ve müşteri hizmetlerine bağlama
        if 'yapboz' in gelen_mesaj:
            belgeyi_gruba_gonder(YAPBOZ_WHATSAPP_GROUP, musteri_numarasi, "Müşteriden gelen belgeler: ...")
        elif 'trafik' in gelen_mesaj:
            belgeyi_gruba_gonder(TRAFIK_WHATSAPP_GROUP, musteri_numarasi, "Müşteriden gelen belgeler: ...")
        elif 'ış yeri' in gelen_mesaj:
            belgeyi_gruba_gonder(IS_YERI_WHATSAPP_GROUP, musteri_numarasi, "Müşteriden gelen belgeler: ...")
        elif 'dask' in gelen_mesaj:
            belgeyi_gruba_gonder(DASK_WHATSAPP_GROUP, musteri_numarasi, "Müşteriden gelen belgeler: ...")
    elif 'hayır' in gelen_mesaj:
        yanit.message("Teşekkürler! Başka bir konuda yardımcı olabilir miyim? Ana menüye dönmek için 'Ana Menü' yazabilirsiniz.")
    elif 'ana menü' in gelen_mesaj:
        yanit.message("Lütfen aşağıdaki seçeneklerden birini yazın:\n"
                      "1. 🧩 *Yapboz Sigortası*\n"
                      "2. 🚗 *Trafik Sigortası*\n"
                      "3. 🏢 *İş Yeri Sigortası*\n"
                      "4. 🌍 *DASK Sigortası*\n"
                      "5. *Diğer İşlemler*")
    elif 'değerlendir' in gelen_mesaj:
        yanit.message("Müşteri temsilcimizi 1 ile 5 arasında değerlendirmenizi rica ederiz. (1: Çok Kötü, 5: Mükemmel)")
    elif gelen_mesaj in ['1', '2', '3', '4', '5']:
        yanit.message("Teşekkürler! Değerlendirmeniz bizim için çok değerli.")
    else:
        yanit.message("Lütfen aşağıdaki seçeneklerden birini yazın:\n"
                      "1. 🧩 *Yapboz Sigortası*\n"
                      "2. 🚗 *Trafik Sigortası*\n"
                      "3. 🏢 *İş Yeri Sigortası*\n"
                      "4. 🌍 *DASK Sigortası*\n"
                      "5. *Diğer İşlemler*")

    return str(yanit)


def belgeyi_gruba_gonder(grup_numarasi, musteri_numarasi, mesaj):
    try:
        requests.post(
            "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(os.getenv("TWILIO_ACCOUNT_SID")),
            data={"To": grup_numarasi, "From": musteri_numarasi, "Body": mesaj},
            auth=(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        )
    except requests.RequestException as e:
        print(f"Mesaj gönderme hatası: {e}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
