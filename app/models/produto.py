from app import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    proposta_valor = db.Column(db.Text)
    canais = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.now)

    personas = db.relationship('Persona', backref='produto', cascade='all, delete-orphan')
    epicos = db.relationship('Epico', backref='produto', cascade='all, delete-orphan')
