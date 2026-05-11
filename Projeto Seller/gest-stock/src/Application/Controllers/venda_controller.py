from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.venda_service import VendaService

class VendaController:
    @staticmethod
    @jwt_required()
    def create_venda():
        data = request.get_json()
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade')
        seller_id = int(get_jwt_identity())

        if not produto_id or not quantidade:
            return make_response(jsonify({"erro": "Campos obrigatórios: produto_id, quantidade"}), 400)

        if quantidade <= 0:
            return make_response(jsonify({"erro": "Quantidade deve ser maior que zero"}), 400)

        try:
            venda = VendaService.create_venda(produto_id, quantidade, seller_id)
            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "venda": venda.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_vendas():
        seller_id = int(get_jwt_identity())

        try:
            vendas = VendaService.get_vendas_by_seller(seller_id)
            vendas_data = [venda.to_dict() for venda in vendas]
            return make_response(jsonify({
                "vendas": vendas_data,
                "sales": vendas_data
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_venda_by_id(venda_id):
        seller_id = int(get_jwt_identity())

        try:
            venda = VendaService.get_venda_by_id(venda_id, seller_id)
            if not venda:
                return make_response(jsonify({"erro": "Venda não encontrada"}), 404)
            return make_response(jsonify({
                "venda": venda.to_dict()
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)