# app/routes/epico.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.epico import Epico
from app.models.produto import Produto
from app import db

epico_bp = Blueprint('epico', __name__)

@epico_bp.route('/epicos')
def listar_epicos():
    epicos = Epico.query.all()
    return render_template('epico_list.html', epicos=epicos)

@epico_bp.route('/epicos/novo', methods=['GET', 'POST'])
def criar_epico():
    produtos = Produto.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        produto_id = request.form['produto_id']
        novo_epico = Epico(titulo=titulo, descricao=descricao, produto_id=produto_id)
        db.session.add(novo_epico)
        db.session.commit()
        return redirect(url_for('epico.listar_epicos'))
    return render_template('epico_form.html', produtos=produtos)

@epico_bp.route('/epicos/<int:id>/editar', methods=['GET', 'POST'])
def editar_epico(id):
    epico = Epico.query.get_or_404(id)
    produtos = Produto.query.all()
    if request.method == 'POST':
        epico.titulo = request.form['titulo']
        epico.descricao = request.form['descricao']
        epico.produto_id = request.form['produto_id']
        db.session.commit()
        return redirect(url_for('epico.listar_epicos'))
    return render_template('epico_form.html', epico=epico, produtos=produtos)

@epico_bp.route('/epicos/<int:id>/deletar', methods=['POST'])
def deletar_epico(id):
    epico = Epico.query.get_or_404(id)
    db.session.delete(epico)
    db.session.commit()
    return redirect(url_for('epico.listar_epicos'))