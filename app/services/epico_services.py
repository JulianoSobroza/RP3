from app.models.epico import Epico
from app import db

# Retorna todos os épicos cadastrados no banco
def listar_epicos():
    return Epico.query.all()

# Cria um novo épico e salva no banco
def criar_epico(titulo, descricao, produto_id):
    novo = Epico(titulo=titulo, descricao=descricao, produto_id=produto_id)
    db.session.add(novo)
    db.session.commit()
    return novo

# Busca um épico pelo ID ou retorna 404 se não existir
def buscar_epico(id):
    return Epico.query.get_or_404(id)

# Edita um épico existente e salva as alterações no banco
def editar_epico(id, titulo, descricao, produto_id):
    epico = buscar_epico(id)
    epico.titulo = titulo
    epico.descricao = descricao
    epico.produto_id = produto_id
    db.session.commit()
    return epico

# Deleta um épico pelo ID e salva as alterações no banco
def deletar_epico(id):
    epico = buscar_epico(id)
    db.session.delete(epico)
    db.session.commit()