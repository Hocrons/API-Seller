from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response

def init_routes(app):

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/api/users', methods=['GET'])
    def get_users():
        return UserController.get_users()

    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/user/verify', methods=['POST'])
    def verify_user():
        return UserController.verify_user()

    app.add_url_rule("/api/auth/login", "login", UserController.login, methods=["POST"])