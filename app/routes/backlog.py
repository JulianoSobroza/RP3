from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.services import backlog_services

backlog_bp = Blueprint('backlog', __name__)  # Corrigido nome do blueprint

@backlog_bp.route('/')
def index():
    return render_template('backlog.html')


@backlog_bp.route('/backlog/<int:produto_id>', methods=['GET'])
@login_required
def backlog(produto_id):
    backlog = backlog_services.listar_backlog_produto(produto_id)
    return render_template('backlog.html', backlog=backlog, produto_id=produto_id)


@backlog_bp.route('/backlog/<int:produto_id>', methods=['POST'])
@login_required
def gerar_backlog(produto_id):
    backlog_services.gerar_backlog(produto_id)
    return redirect(url_for('backlog.backlog', produto_id=produto_id))  # Corrigido nome do blueprint
