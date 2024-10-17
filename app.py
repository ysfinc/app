from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "merhaba" in incoming_msg:
        msg.body("Merhaba! Size nasıl yardımcı olabilirim?")
    elif "nasılsın" in incoming_msg:
        msg.body("Ben bir botum, ama harikayım! 🙂")
    else:
        msg.body("Üzgünüm, bu mesajı anlayamadım.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
