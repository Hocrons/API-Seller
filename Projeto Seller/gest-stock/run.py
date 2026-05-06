from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, make_response
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db
from src.routes import init_routes
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    jwt_secret = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["JWT_SECRET_KEY"] = jwt_secret

    JWTManager(app)

    # ✅ CORS AQUI (ANTES DE TUDO)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # ✅ PRE-FLIGHT HANDLER
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            return response

    # ✅ HEADERS EM TODAS RESPOSTAS
    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return response

    init_db(app)
    init_routes(app)

    return app

app = create_app()

from src.Infrastructure.Model.user import User

if __name__ == '__main__':
    app.run(debug=True)