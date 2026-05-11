from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.produto_service import ProdutoService

class ProdutoController:
    @staticmethod
    @jwt_required()
    def create_produto():
        data = request.get_json() or {}
        nome = data.get('nome') or data.get('name')
        preco = data.get('preco', data.get('price'))
        quantidade_estoque = data.get('quantidade_estoque') or data.get('quantity') or data.get('stock_quantity') or data.get('stock')
        status = data.get('status') or data.get('status_text') or 'ativo'
        if isinstance(status, str) and status.lower() in ['active', 'ativo']:
            status = 'ativo'
        elif isinstance(status, str) and status.lower() in ['inactive', 'inativo']:
            status = 'inativo'

        imagem = data.get('imagem') or data.get('image')

        seller_id = int(get_jwt_identity())

        if isinstance(preco, str) and preco.strip() != '':
            try:
                preco = float(preco) if '.' in preco else int(preco)
            except ValueError:
                return make_response(jsonify({"erro": "Preço deve ser um número"}), 400)

        if isinstance(quantidade_estoque, str) and quantidade_estoque.strip() != '':
            try:
                quantidade_estoque = int(quantidade_estoque)
            except ValueError:
                return make_response(jsonify({"erro": "Quantidade em estoque deve ser um número inteiro"}), 400)

        if not nome or preco is None or quantidade_estoque is None:
            return make_response(jsonify({"erro": "Campos obrigatórios: nome, preco, quantidade_estoque"}), 400)

        try:
            produto = ProdutoService.create_produto(nome, preco, quantidade_estoque, status, imagem, seller_id)
            produto_data = produto.to_dict()
            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": produto_data,
                "product": produto_data
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
            produtos_data = [produto.to_dict() for produto in produtos]
            return make_response(jsonify({
                "produtos": produtos_data,
                "products": produtos_data
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def get_produto_by_id(produto_id):
        seller_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.get_produto_by_id(produto_id, seller_id)
            if not produto:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)
            produto_data = produto.to_dict()
            return make_response(jsonify({
                "produto": produto_data,
                "product": produto_data
            }), 200)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def update_produto(produto_id):
        data = request.get_json() or {}
        seller_id = int(get_jwt_identity())

        nome = data.get('nome') or data.get('name')
        preco = data.get('preco', data.get('price'))
        quantidade_estoque = data.get('quantidade_estoque') or data.get('quantity') or data.get('stock_quantity') or data.get('stock')
        status = data.get('status') or data.get('status_text')
        if isinstance(status, str) and status.lower() in ['active', 'ativo']:
            status = 'ativo'
        elif isinstance(status, str) and status.lower() in ['inactive', 'inativo']:
            status = 'inativo'
        imagem = data.get('imagem') or data.get('image')

        if isinstance(preco, str) and preco.strip() != '':
            try:
                preco = float(preco) if '.' in preco else int(preco)
            except ValueError:
                return make_response(jsonify({"erro": "Preço deve ser um número"}), 400)

        if isinstance(quantidade_estoque, str) and quantidade_estoque.strip() != '':
            try:
                quantidade_estoque = int(quantidade_estoque)
            except ValueError:
                return make_response(jsonify({"erro": "Quantidade em estoque deve ser um número inteiro"}), 400)

        try:
            produto = ProdutoService.update_produto(produto_id, seller_id, nome, preco, quantidade_estoque, status, imagem)
            produto_data = produto.to_dict()
            return make_response(jsonify({
                "mensagem": "Produto atualizado com sucesso",
                "produto": produto_data,
                "product": produto_data
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def inativar_produto(produto_id):
        seller_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.inativar_produto(produto_id, seller_id)
            return make_response(jsonify({
                "mensagem": "Produto inativado com sucesso",
                "produto": produto.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)

    @staticmethod
    @jwt_required()
    def ativar_produto(produto_id):
        seller_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.ativar_produto(produto_id, seller_id)
            return make_response(jsonify({
                "mensagem": "Produto ativado com sucesso",
                "produto": produto.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": "Erro interno do servidor"}), 500)