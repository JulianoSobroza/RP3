from flask import Blueprint, render_template, request, jsonify, current_app
from openai import OpenAI


gpt_bp = Blueprint('gpt', __name__)

@gpt_bp.route('/gpt', methods=['GET'])
def gpt_page():
    return render_template('gpt.html')

@gpt_bp.route("/mensagem", methods=["POST"])
def mensagem():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'response': 'Mensagem vazia.'}), 400

    api_key = current_app.config.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um especialista em metodologias ágeis e engenharia de requisitos. "
                        "Seu trabalho é analisar informações de projeto e gerar uma hierarquia clara e coerente de Épicos. "
                        "Os Épicos devem refletir objetivos estratégicos do produto, cobrir áreas funcionais importantes, "
                        "e permitir que histórias de usuário sejam organizadas sob eles. Responda com uma estrutura hierárquica numerada ou indentada."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({'response': f'Erro ao acessar OpenAI: {e}'}), 500

    return jsonify({'response': answer})