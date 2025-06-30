from typing import List, Optional
from app.models.user import db
from app.models.produto import Produto
from app.models.persona import Persona
from app.models.epico import Epico
from datetime import datetime

class ProdutoService:
    @staticmethod
    def criar_produto(nome: str, descricao: str = None, proposta_valor: str = None,
                      canais: str = None) -> Produto:
        """
        Cria um novo produto no sistema.

        Args:
            nome: Nome do produto (obrigatório)
            descricao: Descrição do produto
            proposta_valor: Proposta de valor do produto
            canais: Canais/plataformas do produto

        Returns:
            Produto: Instância do produto criado
        """
        produto = Produto(
            nome=nome,
            descricao=descricao,
            proposta_valor=proposta_valor,
            canais=canais
        )

        db.session.add(produto)
        db.session.commit()

        return produto

    @staticmethod
    def obter_produto_por_id(produto_id: int) -> Optional[Produto]:
        """
        Obtém um produto pelo ID.

        Args:
            produto_id: ID do produto

        Returns:
            Produto ou None se não encontrado
        """
        return Produto.query.get(produto_id)

    @staticmethod
    def listar_produtos() -> List[Produto]:
        """
        Lista todos os produtos do sistema.

        Returns:
            Lista de produtos
        """
        return Produto.query.order_by(Produto.criado_em.desc()).all()

    @staticmethod
    def atualizar_produto(produto_id: int, **kwargs) -> Optional[Produto]:
        """
        Atualiza um produto existente.

        Args:
            produto_id: ID do produto
            **kwargs: Campos a serem atualizados

        Returns:
            Produto atualizado ou None se não encontrado
        """
        produto = Produto.query.get(produto_id)
        if not produto:
            return None

        # Atualiza apenas os campos fornecidos
        for campo, valor in kwargs.items():
            if hasattr(produto, campo):
                setattr(produto, campo, valor)

        db.session.commit()
        return produto

    @staticmethod
    def excluir_produto(produto_id: int) -> bool:
        """
        Exclui um produto do sistema.

        Args:
            produto_id: ID do produto

        Returns:
            True se excluído com sucesso, False se não encontrado
        """
        produto = Produto.query.get(produto_id)
        if not produto:
            return False

        db.session.delete(produto)
        db.session.commit()
        return True

    @staticmethod
    def adicionar_persona(produto_id: int, nome: str, descricao: str = None,
                          caracteristicas: str = None, necessidades: str = None,
                          objetivos: str = None) -> Optional[Persona]:
        """
        Adiciona uma persona ao produto.

        Args:
            produto_id: ID do produto
            nome: Nome da persona
            descricao: Descrição da persona
            caracteristicas: Características da persona
            necessidades: Necessidades da persona
            objetivos: Objetivos da persona

        Returns:
            Persona criada ou None se produto não encontrado
        """
        produto = Produto.query.get(produto_id)
        if not produto:
            return None

        persona = Persona(
            nome=nome,
            descricao=descricao,
            caracteristicas=caracteristicas,
            necessidades=necessidades,
            objetivos=objetivos,
            produto_id=produto_id
        )

        db.session.add(persona)
        db.session.commit()

        return persona

    @staticmethod
    def obter_personas_produto(produto_id: int) -> List[Persona]:
        """
        Obtém todas as personas de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de personas do produto
        """
        return Persona.query.filter_by(produto_id=produto_id).all()

    @staticmethod
    def obter_epicos_produto(produto_id: int) -> List[Epico]:
        """
        Obtém todos os épicos de um produto.

        Args:
            produto_id: ID do produto

        Returns:
            Lista de épicos do produto
        """
        return Epico.query.filter_by(produto_id=produto_id).order_by(Epico.prioridade.desc()).all()

    @staticmethod
    def obter_estatisticas_produto(produto_id: int) -> dict:
        """
        Obtém estatísticas do produto.

        Args:
            produto_id: ID do produto

        Returns:
            Dicionário com estatísticas do produto
        """
        produto = Produto.query.get(produto_id)
        if not produto:
            return {}

        total_epicos = len(produto.epicos)
        total_personas = len(produto.personas)

        # Contar histórias de usuário através dos épicos
        total_historias = sum(len(epico.historias) for epico in produto.epicos)

        # Contar requisitos através das histórias
        total_requisitos = sum(
            len(historia.requisitos)
            for epico in produto.epicos
            for historia in epico.historias
        )

        return {
            'total_epicos': total_epicos,
            'total_personas': total_personas,
            'total_historias': total_historias,
            'total_requisitos': total_requisitos,
            'criado_em': produto.criado_em.isoformat() if produto.criado_em else None
        }
