from app.models.historia_usuario import HistoriaUsuario
from app import db

def listar_historias():
    return HistoriaUsuario.query.all()

def criar_historia(titulo, descricao, epico_id):
    nova = HistoriaUsuario(titulo=titulo, descricao=descricao, epico_id=epico_id)
    db.session.add(nova)
    db.session.commit()
    return nova

def buscar_historia(id):
    return HistoriaUsuario.query.get_or_404(id)

def editar_historia(id, titulo, descricao, epico_id):
    historia = buscar_historia(id)
    historia.titulo = titulo
    historia.descricao = descricao
    historia.epico_id = epico_id
    db.session.commit()
    return historia

def deletar_historia(id):
    historia = buscar_historia(id)
    db.session.delete(historia)
    db.session.commit()