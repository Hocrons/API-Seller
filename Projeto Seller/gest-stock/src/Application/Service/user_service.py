from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
from src.Infrastructure.http.whats_app import WhatsApp
import random

class UserService:

    @staticmethod
    def __generate_code():
        return str(random.randint(1000, 9999))
    
    @staticmethod
    def create_user(name, email, password, celular, cnpj):   

        if User.query.filter_by(email=email).first():
            raise ValueError("Email já cadastrado")

        if User.query.filter_by(celular=celular).first():
            raise ValueError("Celular já cadastrado")

        if User.query.filter_by(cnpj=cnpj).first():
            raise ValueError("CNPJ já cadastrado")

        code = UserService.__generate_code()

        user = User(
            name=name,
            email=email, 
            celular=celular, 
            cnpj=cnpj, 
            password=password,
            code = code
        )        

        db.session.add(user)
        db.session.commit()    

        WhatsApp.send_code(celular, code)  
         
        return UserDomain(user.id, user.name, user.email, user.password, user.status, user.celular, user.cnpj)
    
    @staticmethod
    def get_users():
        users = User.query.all()

        return [
            UserDomain(
                user.id,
                user.name,
                user.email,
                user.password,
                user.status,
                user.celular,
                user.cnpj
            )
            for user in users
        ]


    @staticmethod
    def verify_code(celular, code):
        user = User.query.filter_by(celular=celular).first()

        if not user:
            raise ValueError("Usuário não encontrado")

        if user.code != code:
            raise ValueError("Código inválido")

        user.status = "ativo"
        user.code = None

        db.session.commit()

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)

        if not user:
            raise ValueError("Usuário não encontrado")

        if user.status != "ativo":
            raise ValueError("Usuário deve estar ativo para ser atualizado")

        allowed_fields = ['name', 'email', 'celular', 'cnpj']

        for field, value in kwargs.items():
            if field in allowed_fields:
                
                if field == 'email' and User.query.filter_by(email=value).first() and value != user.email:
                    raise ValueError("Email já cadastrado")
                if field == 'celular' and User.query.filter_by(celular=value).first() and value != user.celular:
                    raise ValueError("Celular já cadastrado")
                if field == 'cnpj' and User.query.filter_by(cnpj=value).first() and value != user.cnpj:
                    raise ValueError("CNPJ já cadastrado")

                setattr(user, field, value)

        db.session.commit()

        return UserDomain(user.id, user.name, user.email, user.password, user.status, user.celular, user.cnpj)