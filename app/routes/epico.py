from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
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


# ===================================================================
#              <=== ROTA PARA GERAR ÉPICOS COM A LLM ===>
# ===================================================================
@epico_bp.route('/epicos/gerar', methods=['POST'])
def route_gerar_epicos_llm():
    """
    Recebe uma necessidade do usuário via JSON, usa a LLM para gerar um épico
    e retorna o resultado como JSON.
    """
    # 1. Obter os dados da requisição AJAX enviada pelo frontend
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'A mensagem não pode ser vazia.'}), 400

    # 2. Obter a chave da API a partir da configuração da aplicação Flask
    # Usamos 'current_app' em vez de 'app' dentro de um blueprint
    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({'error': 'A chave da API da OpenAI não foi configurada no servidor.'}), 500

    client = OpenAI(api_key=api_key)

    # 3. Chamar a API da OpenAI com o prompt otimizado
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        # === NOVO PROMPT PARA GERAR MÚLTIPLOS ÉPICOS ===
                        "Você é um Product Owner Sênior, especialista em decompor ideias de produtos em Épicos de alto nível. "
                        "Sua tarefa é analisar a descrição de um projeto e gerar uma lista de Épicos essenciais para sua construção. "
                        "Para cada Épico na lista, forneça um título e uma descrição no formato 'Como [persona], quero [objetivo], para que [benefício]'. "
                        "Separe cada épico completo (título e descrição) do próximo com '---' (três hifens). "
                        "Não inclua números, marcadores, introduções ou qualquer texto fora da lista formatada."
                        "Exemplo de formato de saída para 2 épicos:\n"
                        "Gestão de Contas de Usuário\n"
                        "Como um novo usuário, quero poder me cadastrar e fazer login de forma segura para acessar as funcionalidades do sistema.\n"
                        "---\n"
                        "Catálogo de Produtos\n"
                        "Como cliente, quero visualizar uma lista de produtos com fotos e preços para decidir o que comprar."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        answer = completion.choices[0].message.content.strip()
        return jsonify({'response': answer})

    except Exception as e:
        current_app.logger.error(f"Erro ao acessar OpenAI: {e}") # Loga o erro no console do Flask
        return jsonify({'error': 'Ocorreu um erro ao se comunicar com o serviço de IA.'}), 500

