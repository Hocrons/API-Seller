from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.config.data_base import db
from src.utils.validators import ValidadorProduto


class ProdutoService:

    @staticmethod
    def create_produto(nome, preco, quantidade_estoque, status, imagem, seller_id):
        try:
            ValidadorProduto.validar_campos_criar(
                nome,
                preco,
                quantidade_estoque
            )

            if status not in ['ativo', 'inativo']:
                raise ValueError("Status deve ser 'ativo' ou 'inativo'")

            produto = Produto(
                nome=nome.strip(),
                preco=preco,
                quantidade_estoque=quantidade_estoque,
                status=status,
                imagem=imagem,
                seller_id=seller_id
            )

            db.session.add(produto)
            db.session.commit()

            return ProdutoDomain(
                produto.id,
                produto.nome,
                produto.preco,
                produto.quantidade_estoque,
                produto.status,
                produto.imagem,
                produto.seller_id
            )

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_produtos_by_seller(seller_id):
        try:
            produtos = Produto.query.filter_by(
                seller_id=seller_id
            ).all()

            return [
                ProdutoDomain(
                    produto.id,
                    produto.nome,
                    produto.preco,
                    produto.quantidade_estoque,
                    produto.status,
                    produto.imagem,
                    produto.seller_id
                )
                for produto in produtos
            ]

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_produto_by_id(produto_id, seller_id):
        produto = Produto.query.filter_by(
            id=produto_id,
            seller_id=seller_id
        ).first()

        if not produto:
            return None

        return ProdutoDomain(
            produto.id,
            produto.nome,
            produto.preco,
            produto.quantidade_estoque,
            produto.status,
            produto.imagem,
            produto.seller_id
        )

    @staticmethod
    def update_produto(
        produto_id,
        seller_id,
        nome=None,
        preco=None,
        quantidade_estoque=None,
        status=None,
        imagem=None
    ):
        produto = Produto.query.filter_by(
            id=produto_id,
            seller_id=seller_id
        ).first()

        if not produto:
            raise ValueError("Produto não encontrado")

        if nome is not None:
            if not isinstance(nome, str) or len(nome.strip()) == 0:
                raise ValueError("Nome deve ser uma string não vazia")

            produto.nome = nome.strip()

        if preco is not None:
            if not isinstance(preco, (int, float)) or preco < 0:
                raise ValueError("Preço deve ser um número positivo")

            produto.preco = preco

        if quantidade_estoque is not None:
            if not isinstance(quantidade_estoque, int) or quantidade_estoque < 0:
                raise ValueError(
                    "Quantidade em estoque deve ser um inteiro não negativo"
                )

            produto.quantidade_estoque = quantidade_estoque

        if status is not None:
            if status not in ['ativo', 'inativo']:
                raise ValueError("Status deve ser 'ativo' ou 'inativo'")

            produto.status = status

        if imagem is not None:
            produto.imagem = imagem

        db.session.commit()

        return ProdutoDomain(
            produto.id,
            produto.nome,
            produto.preco,
            produto.quantidade_estoque,
            produto.status,
            produto.imagem,
            produto.seller_id
        )

    @staticmethod
    def inativar_produto(produto_id, seller_id):
        try:
            produto = Produto.query.filter_by(
                id=produto_id,
                seller_id=seller_id
            ).first()

            if not produto:
                raise ValueError("Produto não encontrado")

            produto.status = 'inativo'

            db.session.commit()

            return ProdutoDomain(
                produto.id,
                produto.nome,
                produto.preco,
                produto.quantidade_estoque,
                produto.status,
                produto.imagem,
                produto.seller_id
            )

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def ativar_produto(produto_id, seller_id):
        try:
            produto = Produto.query.filter_by(
                id=produto_id,
                seller_id=seller_id
            ).first()

            if not produto:
                raise ValueError("Produto não encontrado")

            produto.status = "ativo"

            db.session.commit()

            return ProdutoDomain(
                produto.id,
                produto.nome,
                produto.preco,
                produto.quantidade_estoque,
                produto.status,
                produto.imagem,
                produto.seller_id
            )

        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e))