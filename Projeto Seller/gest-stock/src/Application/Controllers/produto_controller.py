from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.produto_service import ProdutoService

class ProdutoController:
    @staticmethod
    @jwt_required()
    def create_produto():
        data = request.get_json()
        nome = data.get('nome')
        preco = data.get('preco')
        quantidade_estoque = data.get('quantidade_estoque')
        status = data.get('status', 'ativo')
        imagem = data.get('imagem')

        seller_id = int(get_jwt_identity())

        if not nome or preco is None or quantidade_estoque is None:
            return make_response(jsonify({"erro": "Campos obrigatórios: nome, preco, quantidade_estoque"}), 400)

        try:
            produto = ProdutoService.create_produto(nome, preco, quantidade_estoque, status, imagem, seller_id)
            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": produto.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_produtos():
        seller_id = int(get_jwt_identity())

        try:
            produtos = ProdutoService.get_produtos_by_seller(seller_id)
            return make_response(jsonify({
                "produtos": [produto.to_dict() for produto in produtos]
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)