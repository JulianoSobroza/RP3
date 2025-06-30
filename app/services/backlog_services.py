from app import db
from app.models.produto import Produto
from app.models.historia_usuario import HistoriaUsuario
from app.models.requisito import Requisito
from app.models.backlog import Backlog
from app.models.revisao import Revisao

def gerar_backlog(produto_id):
    """
    Gera backlog para um produto a partir das histórias e requisitos aprovados.
    """
    historias = HistoriaUsuario.query.filter_by(epico_id=None, aprovada=True).all()
    historias += HistoriaUsuario.query.join(Produto, Produto.id == produto_id).filter(HistoriaUsuario.aprovada == True).all()
    requisitos = Requisito.query.join(HistoriaUsuario).filter(HistoriaUsuario.aprovada == True).all()

    ordem = 1
    for historia in historias:
        if not Backlog.query.filter_by(produto_id=produto_id, historia_id=historia.id).first():
            backlog_item = Backlog(produto_id=produto_id, historia_id=historia.id, ordem=ordem)
            db.session.add(backlog_item)
            ordem += 1

    for requisito in requisitos:
        if not Backlog.query.filter_by(produto_id=produto_id, requisito_id=requisito.id).first():
            backlog_item = Backlog(produto_id=produto_id, requisito_id=requisito.id, ordem=ordem)
            db.session.add(backlog_item)
            ordem += 1

    db.session.commit()

def sugerir_revisao_backlog(backlog_id, conteudo_antigo, conteudo_novo, motivo):
    """
    Permite sugerir uma revisão/melhoria para um item do backlog.
    """
    revisao = Revisao(
        tipo='backlog',
        conteudo_antigo=conteudo_antigo,
        conteudo_novo=conteudo_novo,
        motivo=motivo,
        # Associações podem ser feitas conforme necessário
    )
    db.session.add(revisao)
    db.session.commit()
    return revisao

def listar_backlog_produto(produto_id):
    """
    Lista o backlog de um produto, ordenado.
    """
    return Backlog.query.filter_by(produto_id=produto_id).order_by(Backlog.ordem).all()
