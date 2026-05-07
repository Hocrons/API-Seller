from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.config.data_base import db
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.venda import Venda
from sqlalchemy import func

class DashboardController:
    @staticmethod
    @jwt_required()
    def get_dashboard():
        seller_id = int(get_jwt_identity())

    @staticmethod
    @jwt_required()
    def get_dashboard():
        seller_id = int(get_jwt_identity())

        try:
            produtos_total = Produto.query.filter_by(seller_id=seller_id).count()
            produtos_ativos = Produto.query.filter_by(seller_id=seller_id, status='ativo').count()
            produtos_inativos = Produto.query.filter_by(seller_id=seller_id, status='inativo').count()

            estoque_result = db.session.query(func.sum(Produto.quantidade_estoque)).filter_by(seller_id=seller_id).scalar()
            estoque_total = estoque_result if estoque_result else 0

            vendas_total = Venda.query.filter_by(seller_id=seller_id).count()

            valor_result = db.session.query(func.sum(Venda.valor_total)).filter_by(seller_id=seller_id).scalar()
            valor_total_vendido = valor_result if valor_result else 0.0

            produto_mais_vendido_result = db.session.query(
                Produto.nome,
                func.sum(Venda.quantidade).label('total_vendido')
            ).join(Venda, Produto.id == Venda.produto_id)\
             .filter(Produto.seller_id == seller_id)\
             .group_by(Produto.id, Produto.nome)\
             .order_by(func.sum(Venda.quantidade).desc())\
             .first()

            produto_mais_vendido = produto_mais_vendido_result[0] if produto_mais_vendido_result else None

            return make_response(jsonify({
                "produtos_total": produtos_total,
                "produtos_ativos": produtos_ativos,
                "produtos_inativos": produtos_inativos,
                "estoque_total": estoque_total,
                "vendas_total": vendas_total,
                "valor_total_vendido": valor_total_vendido,
                "produto_mais_vendido": produto_mais_vendido
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_relatorio_estoque():
        seller_id = int(get_jwt_identity())

        try:
            produtos = Produto.query.filter_by(seller_id=seller_id).all()

            relatorio = [
                {
                    "nome": produto.nome,
                    "quantidade_estoque": produto.quantidade_estoque,
                    "status": produto.status,
                    "preco": produto.preco
                }
                for produto in produtos
            ]

            return make_response(jsonify({
                "relatorio_estoque": relatorio
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_relatorio_vendas():
        seller_id = int(get_jwt_identity())

        try:
            relatorio_result = db.session.query(
                Produto.nome,
                func.sum(Venda.quantidade).label('quantidade_vendida'),
                func.sum(Venda.valor_total).label('valor_arrecadado')
            ).join(Venda, Produto.id == Venda.produto_id)\
             .filter(Produto.seller_id == seller_id)\
             .group_by(Produto.id, Produto.nome)\
             .all()

            relatorio = [
                {
                    "produto": row[0],
                    "quantidade_vendida": row[1],
                    "valor_arrecadado": row[2]
                }
                for row in relatorio_result
            ]

            return make_response(jsonify({
                "relatorio_vendas": relatorio
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)