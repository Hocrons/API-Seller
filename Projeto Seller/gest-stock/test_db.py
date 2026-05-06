from run import app
from src.config.data_base import db
from src.Infrastructure.Model.user import User

with app.app_context():
    db.create_all()
    print("Tabelas criadas:", db.engine.table_names())