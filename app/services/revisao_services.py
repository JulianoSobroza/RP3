from flask import Blueprint, request, jsonify
from app import db
from app.models.revisao import Revisao

revisoes_bp = Blueprint('revisoes', __name__)

@revisoes_bp.route('/revisoes', methods=['POST'])
def criar_revisao():
    data = request.get_json()
    nova = Revisao(
        tipo=data['tipo'],
        conteudo_antigo=data.get('conteudo_antigo'),
        conteudo_novo=data.get('conteudo_novo'),
        motivo=data.get('motivo'),
        epico_id=data.get('epico_id'),
        historia_id=data.get('historia_id')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'message': 'Revisão criada com sucesso!'}), 201

@revisoes_bp.route('/revisoes', methods=['GET'])
def listar_revisoes():
    revisoes = Revisao.query.all()
    return jsonify([
        {
            'id': r.id,
            'tipo': r.tipo,
            'conteudo_antigo': r.conteudo_antigo,
            'conteudo_novo': r.conteudo_novo,
            'motivo': r.motivo,
            'criado_em': r.criado_em.isoformat(),
            'epico_id': r.epico_id,
            'historia_id': r.historia_id
        } for r in revisoes
    ])

@revisoes_bp.route('/revisoes/<int:id>', methods=['PUT'])
def atualizar_revisao(id):
    revisao = Revisao.query.get_or_404(id)
    data = request.get_json()
    revisao.tipo = data.get('tipo', revisao.tipo)
    revisao.conteudo_antigo = data.get('conteudo_antigo', revisao.conteudo_antigo)
    revisao.conteudo_novo = data.get('conteudo_novo', revisao.conteudo_novo)
    revisao.motivo = data.get('motivo', revisao.motivo)
    revisao.epico_id = data.get('epico_id', revisao.epico_id)
    revisao.historia_id = data.get('historia_id', revisao.historia_id)
    db.session.commit()
    return jsonify({'message': 'Revisão atualizada com sucesso!'})

@revisoes_bp.route('/revisoes/<int:id>', methods=['DELETE'])
def deletar_revisao(id):
    revisao = Revisao.query.get_or_404(id)
    db.session.delete(revisao)
    db.session.commit()
    return jsonify({'message': 'Revisão deletada com sucesso!'})
