from flask_jwt_extended import JWTManager

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

    jwt = JWTManager(app)
    return jwt