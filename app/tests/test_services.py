import pytest
from app import create_app, db
from app.services import epico_services, historia_usuario_services

#criar e limpar banco de dados para cada testes
@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

# testa ciração e listagem de épico
def test_criar_listar_epico(app_context):
    epico = epico_services.criar_epico('Título', 'Descrição', 1)
    assert epico.titulo == 'Título'# verifica se o título está correto
    epicos = epico_services.listar_epicos() # lista todos os épicos
    assert len(epicos) == 1 # verifica se há apenas um épico

# testa editar epico
def test_editar_epico(app_context):
    epico = epico_services.criar_epico('A', 'B', 1) # cria um épico para edição
    epico_editado = epico_services.editar_epico(epico.id, 'Novo', 'Desc', 2) # verifica se o épico foi editado corretamente
    assert epico_editado.titulo == 'Novo'

# testa deletar epico
def test_deletar_epico(app_context):
    epico = epico_services.criar_epico('A', 'B', 1)
    epico_services.deletar_epico(epico.id)
    assert len(epico_services.listar_epicos()) == 0

# testa criação e listagem de história de usuário
def test_criar_listar_historia_usuario(app_context):
    epico = epico_services.criar_epico('Epico', 'Desc', 1)
    historia = historia_usuario_services.criar_historia('Hist', 'Desc', epico.id)
    assert historia.titulo == 'Hist'
    historias = historia_usuario_services.listar_historias()
    assert len(historias) == 1

# testa edição de história de usuário
def test_editar_historia_usuario(app_context):
    epico = epico_services.criar_epico('Epico', 'Desc', 1)
    historia = historia_usuario_services.criar_historia('A', 'B', epico.id)
    historia_editada = historia_usuario_services.editar_historia(historia.id, 'Novo', 'Desc', epico.id)
    assert historia_editada.titulo == 'Novo'

# testa exclusão de história de usuário
def test_deletar_historia_usuario(app_context):
    epico = epico_services.criar_epico('Epico', 'Desc', 1)
    historia = historia_usuario_services.criar_historia('A', 'B', epico.id)
    historia_usuario_services.deletar_historia(historia.id)
    assert len(historia_usuario_services.listar_historias()) == 0