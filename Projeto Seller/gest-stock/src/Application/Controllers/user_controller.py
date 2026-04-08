from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        celular = data.get('celular')
        cnpj = data.get('cnpj')
        password = data.get('password')

        if not name or not email or not password or not celular or not cnpj:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password, celular, cnpj)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    @staticmethod
    def get_users():
        users = UserService.get_users()

        return make_response(jsonify({
                "usuarios": [user.to_dict() for user in users]
            }), 200)
    
    @staticmethod
    def verify_user():
        data = request.get_json()

        celular = data.get('celular')
        code = data.get('code')

        if not celular or not code:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        try:
            UserService.verify_code(celular, code)

            return make_response(jsonify({
                "mensagem": "Usuário ativado com sucesso"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
    
    @staticmethod
    def update_user(user_id):
        data = request.get_json()

        try:
            updated_user = UserService.update_user(user_id, **data)
            return make_response(jsonify({
                "mensagem": "Usuário atualizado com sucesso",
                "usuario": updated_user.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
