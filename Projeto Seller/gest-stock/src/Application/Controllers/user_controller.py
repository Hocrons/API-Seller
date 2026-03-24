from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from src.Infrastructure.Model.user import User

class UserController:

    @staticmethod
    def register_user():
        data = request.get_json(force=True)
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
        data = request.get_json(force=True)

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
    def login():
        data = request.get_json(force=True)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)

        if not check_password_hash(user.password, password):
            return make_response(jsonify({"erro": "Senha inválida"}), 401)

        if user.status != "ativo":
            return make_response(jsonify({"erro": "Conta não ativada"}), 403)

        token = create_access_token(identity=user.id)

        return make_response(jsonify({
            "access_token": token,
            "user_id": user.id
        }), 200)