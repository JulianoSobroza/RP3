from flask import Blueprint, request, jsonify
from app import db
from app.models.requisito import Requisito

requisitos_bp = Blueprint('requisitos', __name__)

@requisitos_bp.route('/requisitos', methods=['POST'])
def criar_requisito():
    data = request.get_json()
    novo = Requisito(
        descricao=data['descricao'],
        historia_id=data['historia_id'],
        prioridade=data.get('prioridade', 2)
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Requisito criado com sucesso!'}), 201

@requisitos_bp.route('/requisitos', methods=['GET'])
def listar_requisitos():
    requisitos = Requisito.query.all()
    return jsonify([
        {
            'id': r.id,
            'descricao': r.descricao,
            'historia_id': r.historia_id,
            'prioridade': r.prioridade
        } for r in requisitos
    ])

@requisitos_bp.route('/requisitos/<int:id>', methods=['PUT'])
def atualizar_requisito(id):
    requisito = Requisito.query.get_or_404(id)
    data = request.get_json()
    requisito.descricao = data.get('descricao', requisito.descricao)
    requisito.historia_id = data.get('historia_id', requisito.historia_id)
    requisito.prioridade = data.get('prioridade', requisito.prioridade)
    db.session.commit()
    return jsonify({'message': 'Requisito atualizado com sucesso!'})

@requisitos_bp.route('/requisitos/<int:id>', methods=['DELETE'])
def deletar_requisito(id):
    requisito = Requisito.query.get_or_404(id)
    db.session.delete(requisito)
    db.session.commit()
    return jsonify({'message': 'Requisito deletado com sucesso!'})
