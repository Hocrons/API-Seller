from src.Domain.venda import VendaDomain
from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.venda import Venda
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.utils.validators import ValidadorVenda, ValidadorProduto
from datetime import datetime

class VendaService:

    @staticmethod
    def create_venda(produto_id, quantidade, seller_id):
        try:
            ValidadorVenda.validar_campos_criar(produto_id, quantidade)
            ValidadorVenda.validar_seller_ativo(seller_id)
            
            produto = ValidadorProduto.validar_produto_existe(produto_id, seller_id)
            ValidadorProduto.validar_produto_ativo(produto)
            ValidadorVenda.validar_estoque(produto, quantidade)
            
            if produto.preco < 0:
                raise ValueError("Preço do produto não pode ser negativo")
            
            preco_unitario = produto.preco
            valor_total = preco_unitario * quantidade
            
            if valor_total < 0:
                raise ValueError("Valor total da venda não pode ser negativo")
            
            venda = Venda(
                produto_id=produto_id,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                valor_total=valor_total,
                seller_id=seller_id
            )
            
            produto.quantidade_estoque -= quantidade
            
            if produto.quantidade_estoque < 0:
                db.session.rollback()
                raise ValueError("Erro na redução do estoque")
            
            db.session.add(venda)
            db.session.commit()
            
            return VendaDomain(
                venda.id,
                venda.produto_id,
                venda.quantidade,
                venda.preco_unitario,
                venda.valor_total,
                venda.seller_id,
                venda.created_at
            )
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_vendas_by_seller(seller_id):
        try:
            ValidadorVenda.validar_seller_ativo(seller_id)
            
            vendas = Venda.query.filter_by(seller_id=seller_id).order_by(Venda.created_at.desc()).all()

            return [
                VendaDomain(
                    venda.id,
                    venda.produto_id,
                    venda.quantidade,
                    venda.preco_unitario,
                    venda.valor_total,
                    venda.seller_id,
                    venda.created_at
                )
                for venda in vendas
            ]
        except Exception as e:
            raise e

    @staticmethod
    def get_all_vendas():
        try:
            vendas = Venda.query.order_by(Venda.created_at.desc()).all()

            return [
                VendaDomain(
                    venda.id,
                    venda.produto_id,
                    venda.quantidade,
                    venda.preco_unitario,
                    venda.valor_total,
                    venda.seller_id,
                    venda.created_at
                )
                for venda in vendas
            ]
        except Exception as e:
            raise e

    @staticmethod
    def get_venda_by_id(venda_id, seller_id):
        try:
            ValidadorVenda.validar_seller_ativo(seller_id)
            
            venda = Venda.query.filter_by(id=venda_id, seller_id=seller_id).first()
            if not venda:
                return None
            return VendaDomain(
                venda.id,
                venda.produto_id,
                venda.quantidade,
                venda.preco_unitario,
                venda.valor_total,
                venda.seller_id,
                venda.created_at
            )
        except Exception as e:
            raise e