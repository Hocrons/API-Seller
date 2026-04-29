from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.data_base import init_db
from src.routes import init_routes
import os

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    
    # Carrega JWT_SECRET_KEY do .env, ou usa padrão para desenvolvimento
    jwt_secret = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["JWT_SECRET_KEY"] = jwt_secret
    
    jwt = JWTManager(app)

    init_db(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)