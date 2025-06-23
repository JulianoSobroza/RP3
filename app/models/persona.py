from app import db


class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)