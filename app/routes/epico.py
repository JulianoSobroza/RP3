from flask import Blueprint, render_template, request, redirect, url_for
from app.models.produto import Produto
from app.services.epico_services import (
    listar_epicos, criar_epico, buscar_epico, editar_epico, deletar_epico
)

from openai import OpenAI


# Cria um Blueprint para as rotas de épico
epico_bp = Blueprint('epico', __name__)

# <===Rota para listar todos os épicos ===>
@epico_bp.route('/epicos')
def route_listar_epicos():
    epicos = listar_epicos()  # Chama o service para buscar todos os épicos
    return render_template('epico_list.html', epicos=epicos)  # Renderiza o template de listagem

# <===Rota para criar um novo épico ===>
@epico_bp.route('/epicos/novo', methods=['GET', 'POST'])
def route_criar_epico():
    produtos = Produto.query.all()
    if request.method == 'POST':
        criar_epico(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            produto_id=request.form['produto_id']
        )
        return redirect(url_for('epico.route_listar_epicos'))
    return render_template('epico_form.html', produtos=produtos)

# <=== Rota para editar um épico existente ===>
@epico_bp.route('/epicos/<int:id>/editar', methods=['GET', 'POST'])
def route_editar_epico(id):
    epico = buscar_epico(id)  # Busca o épico pelo ID usando o service
    produtos = Produto.query.all()  # Busca todos os produtos para o formulário
    if request.method == 'POST':
        # Chama o service para editar o épico com os novos dados
        editar_epico(
            id,
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            produto_id=request.form['produto_id']
        )
        return redirect(url_for('epico.route_listar_epicos'))  # Redireciona após editar
    return render_template('epico_form.html', epico=epico, produtos=produtos)  # Exibe o formulário preenchido

# <=== Rota para deletar um épico===>
@epico_bp.route('/epicos/<int:id>/deletar', methods=['POST'])
def route_deletar_epico(id):
    deletar_epico(id)
    return redirect(url_for('epico.route_listar_epicos'))

@epico_bp.route("/mensagem", methods=["POST"])
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
            messages=[{"role": "user", "content": user_message}]
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({'response': f'Erro ao acessar OpenAI: {e}'}), 500

    return jsonify({'response': answer})
