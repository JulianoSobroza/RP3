from flask import Blueprint, render_template
from flask_login import login_required
from app.models.produto import Produto

dashboard_bp = Blueprint('main', __name__)

@dashboard_bp.route('/')
def index():
    return render_template('index.html')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():

    produto = Produto.query.first()
    produto_id = produto.id if produto else None

    logs = []
    return render_template('dashboard/0dashboard.html', logs=logs, produto_id=produto_id)

