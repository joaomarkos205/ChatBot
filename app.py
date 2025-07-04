from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
app = Flask(__name__)

# Configura o token da Hugging Face

load_dotenv()

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")
    print(f"[WhatsApp] Mensagem recebida de {sender}: {incoming_msg}")

    # Envia mensagem para a IA com instrução para responder em português
    prompt = f"Responda em português: {incoming_msg}"
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_reply = response.choices[0].message["content"]

    # Resposta para o WhatsApp via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(ai_reply)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
