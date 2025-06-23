from app import db


class Requisito(db.Model):
    __tablename__ = 'requisitos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    historia_id = db.Column(db.Integer, db.ForeignKey('historias_usuario.id'), nullable=False)
    prioridade = db.Column(db.Integer)  # 1-Alta, 2-Media, 3-Baixa