from app import db
from datetime import datetime

class Revisao(db.Model):
    __tablename__ = 'revisoes'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))  # 'epico' ou 'historia'
    conteudo_antigo = db.Column(db.Text)
    conteudo_novo = db.Column(db.Text)
    motivo = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.now)

    epico_id = db.Column(db.Integer, db.ForeignKey('epicos.id'), nullable=True)
    historia_id = db.Column(db.Integer, db.ForeignKey('historias_usuario.id'), nullable=True)