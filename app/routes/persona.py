from datetime import datetime
from app.models.user import db

class Persona(db.Model):
    __tablename__ = 'personas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    caracteristicas = db.Column(db.Text)
    necessidades = db.Column(db.Text)
    objetivos = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    # Chave estrangeira
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

    def __repr__(self):
        return f'<Persona {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'caracteristicas': self.caracteristicas,
            'necessidades': self.necessidades,
            'objetivos': self.objetivos,
            'produto_id': self.produto_id,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }

