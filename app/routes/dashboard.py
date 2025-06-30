from flask import Blueprint, render_template
from flask_login import login_required
from app.services.produto_service import ProdutoService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    return render_template('index.html')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    produtos = ProdutoService.listar_produtos()
    return render_template('dashboard/dashboard_inicial.html', produtos=produtos)

@dashboard_bp.route('/inicio_produto/<int:produto_id>')
@login_required
def inicio_produto(produto_id):
    produto = ProdutoService.obter_produto_por_id(produto_id)
    return render_template('dashboard/0base_produto.html', produto=produto)


@dashboard_bp.route('/criar_produto')
@login_required
def criar_produto():
    # Apenas renderiza o formulário, o POST é tratado pelo produto_bp
    return render_template('dashboard/criar_novo_produto.html')