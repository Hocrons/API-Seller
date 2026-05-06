from src.Infrastructure.Model.user import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

class UserServiceLogin:

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            raise ValueError("Usuário não encontrado")

        if not check_password_hash(user.password, password):
            raise ValueError("Senha incorreta")
        
        if user.status != "ativo":
            raise ValueError("Usuário inativo. Verifique seu código de ativação")

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "email": user.email,
                "status": user.status
            }
        )

        return {
            "message": "Login realizado com sucesso",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "status": user.status
            }
        }, 200