from app import db


class Epico(db.Model):
    __tablename__ = 'epicos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

    historias = db.relationship('HistoriaUsuario', backref='epico', cascade='all, delete-orphan')
    revisoes = db.relationship('Revisao', backref='epico', cascade='all, delete-orphan')
