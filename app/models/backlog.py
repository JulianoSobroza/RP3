from app import db


class Backlog(db.Model):
    __tablename__ = 'backlogs'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    historia_id = db.Column(db.Integer, db.ForeignKey('historias_usuario.id'), nullable=True)
    requisito_id = db.Column(db.Integer, db.ForeignKey('requisitos.id'), nullable=True)
    ordem = db.Column(db.Integer, nullable=False)  # posição no backlog

    produto = db.relationship('Produto', backref='backlog')
    historia = db.relationship('HistoriaUsuario', backref='no_backlog')
    requisito = db.relationship('Requisito', backref='no_backlog')