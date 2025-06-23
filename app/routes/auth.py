from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService, token_required, get_current_user
from app.services.llm_log_service import LLMLogService
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Realiza login do usuário.

    Body JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    dados = request.get_json()

    if not dados or 'username' not in dados:
        return jsonify({'erro': 'Username é obrigatório'}), 400

    # Por simplicidade, não verificamos senha nesta versão de demonstração
    resultado = AuthService.login(dados['username'], dados.get('password', ''))

    return jsonify(resultado), 200

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verificar_token():
    """Verifica se o token é válido."""
    user = get_current_user()
    return jsonify({
        'valido': True,
        'user': user.to_dict()
    })

@auth_bp.route('/logs/llm', methods=['GET'])
@token_required
def obter_logs_llm():
    """
    Obtém logs de LLM do usuário atual.

    Query params:
    - limite: número máximo de logs (padrão: 50)
    - produto_id: filtrar por produto específico
    - tipo_operacao: filtrar por tipo de operação
    """
    user = get_current_user()
    limite = request.args.get('limite', 50, type=int)
    produto_id = request.args.get('produto_id', type=int)
    tipo_operacao = request.args.get('tipo_operacao')

    if produto_id:
        logs = LLMLogService.obter_logs_produto(produto_id, limite)
    elif tipo_operacao:
        logs = LLMLogService.obter_logs_por_tipo(tipo_operacao, limite)
    else:
        logs = LLMLogService.obter_logs_usuario(user.id, limite)

    return jsonify({
        'logs': [log.to_dict() for log in logs]
    })

@auth_bp.route('/logs/llm/estatisticas', methods=['GET'])
@token_required
def obter_estatisticas_llm():
    """
    Obtém estatísticas de uso do LLM.

    Query params:
    - produto_id: filtrar por produto específico
    - data_inicio: data de início (formato: YYYY-MM-DD)
    - data_fim: data de fim (formato: YYYY-MM-DD)
    """
    user = get_current_user()
    produto_id = request.args.get('produto_id', type=int)
    data_inicio_str = request.args.get('data_inicio')
    data_fim_str = request.args.get('data_fim')

    data_inicio = None
    data_fim = None

    try:
        if data_inicio_str:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
        if data_fim_str:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

    estatisticas = LLMLogService.obter_estatisticas_uso(
        usuario_id=user.id,
        produto_id=produto_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

    return jsonify({
        'estatisticas': estatisticas
    })

