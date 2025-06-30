from datetime import datetime
from app.models.user import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    proposta_valor = db.Column(db.Text)
    canais = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.now)

    # Relacionamentos
    personas = db.relationship('Persona', backref='produto', cascade='all, delete-orphan')
    epicos = db.relationship('Epico', backref='produto', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Produto {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'proposta_valor': self.proposta_valor,
            'canais': self.canais,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'personas': [persona.to_dict() for persona in self.personas],
            'epicos': [epico.to_dict() for epico in self.epicos]
        }

