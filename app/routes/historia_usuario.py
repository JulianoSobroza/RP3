# app/routes/historia_usuario.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.epico import Epico
from app.services.historia_usuario_services import (
    listar_historias, criar_historia, buscar_historia, editar_historia, deletar_historia
)

historia_usuario_bp = Blueprint('historia_usuario', __name__)

@historia_usuario_bp.route('/historias')
def route_listar_historias():
    historias = listar_historias()
    return render_template('historia_usuario_list.html', historias=historias)

@historia_usuario_bp.route('/historias/nova', methods=['GET', 'POST'])
def route_criar_historia():
    epicos = Epico.query.all()
    if request.method == 'POST':
        criar_historia(
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            epico_id=request.form['epico_id']
        )
        return redirect(url_for('historia_usuario.route_listar_historias'))
    return render_template('historia_usuario_form.html', epicos=epicos)

@historia_usuario_bp.route('/historias/<int:id>/editar', methods=['GET', 'POST'])
def route_editar_historia(id):
    historia = buscar_historia(id)
    epicos = Epico.query.all()
    if request.method == 'POST':
        editar_historia(
            id,
            titulo=request.form['titulo'],
            descricao=request.form['descricao'],
            epico_id=request.form['epico_id']
        )
        return redirect(url_for('historia_usuario.route_listar_historias'))
    return render_template('historia_usuario_form.html', historia=historia, epicos=epicos)

@historia_usuario_bp.route('/historias/<int:id>/deletar', methods=['POST'])
def route_deletar_historia(id):
    deletar_historia(id)
    return redirect(url_for('historia_usuario.route_listar_historias'))