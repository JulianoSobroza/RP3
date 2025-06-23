from app import db


class HistoriaUsuario(db.Model):
    __tablename__ = 'historias_usuario'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    epico_id = db.Column(db.Integer, db.ForeignKey('epicos.id'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=True)
    prioridade = db.Column(db.Integer)  # 1-Alta, 2-Média, 3-Baixa
    aprovada = db.Column(db.Boolean, default=False)

    requisitos = db.relationship('Requisito', backref='historia', cascade='all, delete-orphan')
    revisoes = db.relationship('Revisao', backref='historia', cascade='all, delete-orphan')
