from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from src.config.data_base import db
from src.Infrastructure.Model.user import User

token_blacklist = set()

def add_token_to_blacklist(jti):
    token_blacklist.add(jti)

def is_token_revoked(jwt_payload):
    jti = jwt_payload.get('jti')
    return jti in token_blacklist

def jwt_error_handler(error):
    return make_response(jsonify({
        "erro": "Token inválido ou expirado",
        "detalhes": str(error)
    }), 401)

def jwt_required_with_validation(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            
            if is_token_revoked(claims):
                return make_response(jsonify({
                    "erro": "Token foi revogado"
                }), 401)
            
            seller_id = int(get_jwt_identity())
            user = User.query.filter_by(id=seller_id).first()
            
            if not user:
                return make_response(jsonify({
                    "erro": "Usuário não encontrado"
                }), 404)
            
            if user.status != 'ativo':
                return make_response(jsonify({
                    "erro": "Usuário inativo"
                }), 403)
            
            return fn(*args, **kwargs)
        except Exception as e:
            return make_response(jsonify({
                "erro": "Erro na validação do token"
            }), 401)
    
    return wrapper

def validate_seller_id(seller_id):
    user = User.query.filter_by(id=seller_id).first()
    if not user:
        return False, "Usuário não encontrado"
    if user.status != 'ativo':
        return False, "Usuário inativo"
    return True, None

def standardize_error_response(error_message, status_code=400):
    return make_response(jsonify({"erro": error_message}), status_code)

def standardize_success_response(data=None, message="Operação realizada com sucesso", status_code=200):
    response = {"mensagem": message}
    if data:
        response.update(data)
    return make_response(jsonify(response), status_code)