import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError, DatabaseError

db = SQLAlchemy()


def wait_for_db(max_retries=15, delay=2):
    """
    Aguarda o banco de dados ficar disponível antes de continuar.
    """
    for attempt in range(max_retries):
        try:
            db.engine.connect()
            print("✅ Banco conectado!")
            return
        except (OperationalError, DatabaseError) as e:
            print(f"⏳ Tentativa {attempt + 1}/{max_retries} - banco ainda não disponível...")
            time.sleep(delay)

    raise Exception("❌ Não foi possível conectar ao banco após várias tentativas")


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@db:3306/market_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        wait_for_db()
        db.create_all()