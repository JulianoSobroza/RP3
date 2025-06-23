# app/routes/historia_usuario.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.historia_usuario import HistoriaUsuario
from app import db
from app.models.epico import Epico

historia_usuario_bp = Blueprint('historia_usuario', __name__)

@historia_usuario_bp.route('/historias')
def listar_historias():
    historias = HistoriaUsuario.query.all()
    return render_template('historia_usuario_list.html', historias=historias)

@historia_usuario_bp.route('/historias/nova', methods=['GET', 'POST'])
def criar_historia():
    epicos = Epico.query.all()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        epico_id = request.form['epico_id']
        nova_historia = HistoriaUsuario(titulo=titulo, descricao=descricao, epico_id=epico_id)
        db.session.add(nova_historia)
        db.session.commit()
        return redirect(url_for('historia_usuario.listar_historias'))
    return render_template('historia_usuario_form.html', epicos=epicos)

@historia_usuario_bp.route('/historias/<int:id>/editar', methods=['GET', 'POST'])
def editar_historia(id):
    historia = HistoriaUsuario.query.get_or_404(id)
    epicos = Epico.query.all()
    if request.method == 'POST':
        historia.titulo = request.form['titulo']
        historia.descricao = request.form['descricao']
        historia.epico_id = request.form['epico_id']
        db.session.commit()
        return redirect(url_for('historia_usuario.listar_historias'))
    return render_template('historia_usuario_form.html', historia=historia, epicos=epicos)

@historia_usuario_bp.route('/historias/<int:id>/deletar', methods=['POST'])
def deletar_historia(id):
    historia = HistoriaUsuario.query.get_or_404(id)
    db.session.delete(historia)
    db.session.commit()
    return redirect(url_for('historia_usuario.listar_historias'))