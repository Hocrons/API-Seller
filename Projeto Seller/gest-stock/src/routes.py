from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.produto_controller import ProdutoController
from src.Application.Controllers.venda_controller import VendaController
from src.Application.Controllers.dashboard_controller import DashboardController
from flask import jsonify, make_response

def init_routes(app): 

    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/api/users', methods=['GET'])
    def get_users():
        return UserController.get_users()

    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/user/verify', methods=['POST'])
    def verify_user():
        return UserController.verify_user()
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return UserController.login()

    @app.route('/api/produtos', methods=['POST'])
    def create_produto():
        return ProdutoController.create_produto()

    @app.route('/products', methods=['POST'])
    def create_product_alias():
        return create_produto()

    @app.route('/api/produtos', methods=['GET'])
    def get_produtos():
        return ProdutoController.get_produtos()

    @app.route('/products', methods=['GET'])
    def get_products_alias():
        return get_produtos()

    @app.route('/api/produtos/<int:produto_id>', methods=['GET'])
    def get_produto_by_id(produto_id):
        return ProdutoController.get_produto_by_id(produto_id)

    @app.route('/products/<int:produto_id>', methods=['GET'])
    def get_product_by_id_alias(produto_id):
        return get_produto_by_id(produto_id)

    @app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
    def update_produto(produto_id):
        return ProdutoController.update_produto(produto_id)

    @app.route('/products/<int:produto_id>', methods=['PUT'])
    def update_product_alias(produto_id):
        return update_produto(produto_id)

    @app.route('/api/produtos/<int:produto_id>/inativar', methods=['PATCH'])
    def inativar_produto(produto_id):
        return ProdutoController.inativar_produto(produto_id)

    @app.route('/api/produtos/<int:produto_id>/ativar', methods=['PATCH'])
    def ativar_produto(produto_id):
        return ProdutoController.ativar_produto(produto_id)

    @app.route('/api/vendas', methods=['POST'])
    def create_venda():
        return VendaController.create_venda()

    @app.route('/sales', methods=['POST'])
    def create_sale_alias():
        return create_venda()

    @app.route('/api/vendas', methods=['GET'])
    def get_vendas():
        return VendaController.get_vendas()

    @app.route('/sales', methods=['GET'])
    def get_sales_alias():
        return get_vendas()

    @app.route('/api/vendas/<int:venda_id>', methods=['GET'])
    def get_venda_by_id(venda_id):
        return VendaController.get_venda_by_id(venda_id)

    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard():
        return DashboardController.get_dashboard()

    @app.route('/dashboard', methods=['GET'])
    def get_dashboard_alias():
        return get_dashboard()

    @app.route('/api/relatorios/estoque', methods=['GET'])
    def get_relatorio_estoque():
        return DashboardController.get_relatorio_estoque()

    @app.route('/api/relatorios/vendas', methods=['GET'])
    def get_relatorio_vendas():
        return DashboardController.get_relatorio_vendas()