from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.services.produto_service import ProdutoService
from functools import wraps

produto_bp = Blueprint('produto', __name__)  # Certifique-se de não usar url_prefix

def handle_errors(f):
    """Decorator para tratamento de erros."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
    return decorated_function

@produto_bp.route('/produtos', methods=['POST'])
@handle_errors
def criar_produto():
    """
    Cria um novo produto.
    Aceita JSON (API) ou formulário HTML.
    """
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form

    if not dados or 'nome' not in dados:
        if request.is_json:
            return jsonify({'erro': 'Nome do produto é obrigatório'}), 400
        flash('Nome do produto é obrigatório', 'danger')
        return render_template('criar_novo_produto.html')

    produto = ProdutoService.criar_produto(
        nome=dados['nome'],
        descricao=dados.get('descricao'),
        proposta_valor=dados.get('proposta_valor'),
        canais=dados.get('canais')
    )

    if request.is_json:
        return jsonify({
            'mensagem': 'Produto criado com sucesso',
            'produto': produto.to_dict()
        }), 201
    flash('Produto criado com sucesso!', 'success')
    return redirect(url_for('dashboard.dashboard'))

@produto_bp.route('/produtos', methods=['GET'])
@handle_errors
def listar_produtos():
    """Lista todos os produtos."""
    produtos = ProdutoService.listar_produtos()
    return jsonify({
        'produtos': [produto.to_dict() for produto in produtos]
    })

@produto_bp.route('/produtos/<int:produto_id>', methods=['GET'])
@handle_errors
def obter_produto(produto_id):
    """Obtém um produto específico pelo ID."""
    produto = ProdutoService.obter_produto_por_id(produto_id)

    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify({
        'produto': produto.to_dict()
    })

@produto_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
@handle_errors
def atualizar_produto(produto_id):
    """
    Atualiza um produto existente.

    Body JSON:
    {
        "nome": "string (opcional)",
        "descricao": "string (opcional)",
        "proposta_valor": "string (opcional)",
        "canais": "string (opcional)"
    }
    """
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Dados não fornecidos'}), 400

    produto = ProdutoService.atualizar_produto(produto_id, **dados)

    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify({
        'mensagem': 'Produto atualizado com sucesso',
        'produto': produto.to_dict()
    })

@produto_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
@handle_errors
def excluir_produto(produto_id):
    """Exclui um produto."""
    sucesso = ProdutoService.excluir_produto(produto_id)

    if not sucesso:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify({
        'mensagem': 'Produto excluído com sucesso'
    })

@produto_bp.route('/produtos/<int:produto_id>/personas', methods=['POST'])
@handle_errors
def adicionar_persona(produto_id):
    """
    Adiciona uma persona ao produto.

    Body JSON:
    {
        "nome": "string (obrigatório)",
        "descricao": "string (opcional)",
        "caracteristicas": "string (opcional)",
        "necessidades": "string (opcional)",
        "objetivos": "string (opcional)"
    }
    """
    dados = request.get_json()

    if not dados or 'nome' not in dados:
        return jsonify({'erro': 'Nome da persona é obrigatório'}), 400

    persona = ProdutoService.adicionar_persona(
        produto_id=produto_id,
        nome=dados['nome'],
        descricao=dados.get('descricao'),
        caracteristicas=dados.get('caracteristicas'),
        necessidades=dados.get('necessidades'),
        objetivos=dados.get('objetivos')
    )

    if not persona:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify({
        'mensagem': 'Persona adicionada com sucesso',
        'persona': persona.to_dict()
    }), 201

@produto_bp.route('/produtos/<int:produto_id>/personas', methods=['GET'])
@handle_errors
def listar_personas_produto(produto_id):
    """Lista todas as personas de um produto."""
    personas = ProdutoService.obter_personas_produto(produto_id)
    return jsonify({
        'personas': [persona.to_dict() for persona in personas]
    })

@produto_bp.route('/produtos/<int:produto_id>/epicos', methods=['GET'])
@handle_errors
def listar_epicos_produto(produto_id):
    """Lista todos os épicos de um produto."""
    epicos = ProdutoService.obter_epicos_produto(produto_id)
    return jsonify({
        'epicos': [epico.to_dict() for epico in epicos]
    })

@produto_bp.route('/produtos/<int:produto_id>/estatisticas', methods=['GET'])
@handle_errors
def obter_estatisticas_produto(produto_id):
    """Obtém estatísticas do produto."""
    estatisticas = ProdutoService.obter_estatisticas_produto(produto_id)

    if not estatisticas:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    return jsonify({
        'estatisticas': estatisticas
    })

@produto_bp.route('/criar_produto', methods=['GET'])
def criar_produto_form():
    return render_template('criar_novo_produto.html')
