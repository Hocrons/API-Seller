from flask import request, jsonify
from src.Application.Service.user_service_login import UserServiceLogin

class UserLoginController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"}), 400
        response, status_code = UserServiceLogin.login(email, password)
        return jsonify(response), status_code