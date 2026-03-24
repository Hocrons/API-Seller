from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def criar_produto():
    seller_id = get_jwt_identity()