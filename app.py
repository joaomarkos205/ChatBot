from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)

# Pega o token da Hugging Face via variável de ambiente
hf_token = os.getenv("HF_TOKEN")

# Inicializa o cliente da IA
client = InferenceClient(api_key=hf_token)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")
    print(f"[WhatsApp] Mensagem recebida de {sender}: {incoming_msg}")

    # Envia mensagem para a IA com instrução em português
    prompt = f"Responda em português: {incoming_msg}"
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_reply = response.choices[0].message["content"]

    # Cria resposta via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(ai_reply)

    return str(twilio_response)

# Endpoint opcional para health check
@app.route("/healthz")
def healthz():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
