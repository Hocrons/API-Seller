from flask import Flask
from src.routes import init_routes
from src.config.jwt_config import init_jwt
from src.config.data_base import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

init_jwt(app)
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)