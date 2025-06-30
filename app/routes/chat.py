from flask import Blueprint, render_template, request, jsonify
from gpt4all import GPT4All
import os
import requests

chat_bp = Blueprint('chat', __name__)

MODEL_PATH = "orca-mini-3b.ggmlv3.q4_0.bin"
MODEL_URL = "https://gpt4all.io/models/orca-mini-3b.ggmlv3.q4_0.bin"

if not os.path.exists(MODEL_PATH):
    print("Modelo não encontrado, baixando...")
    with requests.get(MODEL_URL, stream=True) as r:
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

model = None
if os.path.exists(MODEL_PATH):
    model = GPT4All(MODEL_PATH)
else:
    model = None

@chat_bp.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html', model_loaded=(model is not None))

@chat_bp.route('/chat_api', methods=['POST'])
def chat_api():
    if model is None:
        return jsonify({'response': 'Modelo de IA não encontrado no servidor. Contate o administrador.'}), 500
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'response': 'Mensagem vazia.'}), 400
    # Gera resposta do modelo
    response = model.generate(user_message, max_tokens=128)
    return jsonify({'response': response})
