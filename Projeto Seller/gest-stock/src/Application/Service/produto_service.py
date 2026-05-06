from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.config.data_base import db

class ProdutoService:

    @staticmethod
    def create_produto(nome, preco, quantidade_estoque, status, imagem, seller_id):
        if not nome or not isinstance(nome, str) or len(nome.strip()) == 0:
            raise ValueError("Nome é obrigatório e deve ser uma string não vazia")

        if preco is None or not isinstance(preco, (int, float)) or preco < 0:
            raise ValueError("Preço é obrigatório e deve ser um número positivo")

        if quantidade_estoque is None or not isinstance(quantidade_estoque, int) or quantidade_estoque < 0:
            raise ValueError("Quantidade em estoque é obrigatória e deve ser um inteiro não negativo")

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

    @staticmethod
    def get_produtos_by_seller(seller_id):
        produtos = Produto.query.filter_by(seller_id=seller_id).all()

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