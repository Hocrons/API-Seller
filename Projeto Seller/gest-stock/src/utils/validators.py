from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.user import User

class ValidadorProduto:
    @staticmethod
    def validar_campos_criar(nome, preco, quantidade_estoque):
        if not nome or not isinstance(nome, str) or len(nome.strip()) == 0:
            raise ValueError("Nome é obrigatório e deve ser uma string não vazia")
        
        if preco is None or not isinstance(preco, (int, float)) or preco < 0:
            raise ValueError("Preço deve ser um número maior ou igual a zero")
        
        if quantidade_estoque is None or not isinstance(quantidade_estoque, int) or quantidade_estoque < 0:
            raise ValueError("Quantidade em estoque deve ser um inteiro maior ou igual a zero")
        
        return True
    
    @staticmethod
    def validar_campos_editar(nome=None, preco=None, quantidade_estoque=None):
        if nome is not None and (not isinstance(nome, str) or len(nome.strip()) == 0):
            raise ValueError("Nome deve ser uma string não vazia")
        
        if preco is not None and (not isinstance(preco, (int, float)) or preco < 0):
            raise ValueError("Preço deve ser um número maior ou igual a zero")
        
        if quantidade_estoque is not None and (not isinstance(quantidade_estoque, int) or quantidade_estoque < 0):
            raise ValueError("Quantidade em estoque deve ser um inteiro maior ou igual a zero")
        
        return True
    
    @staticmethod
    def validar_produto_existe(produto_id, seller_id):
        produto = Produto.query.filter_by(id=produto_id, seller_id=seller_id).first()
        if not produto:
            raise ValueError("Produto não encontrado")
        return produto
    
    @staticmethod
    def validar_produto_ativo(produto):
        if produto.status != 'ativo':
            raise ValueError("Produto não está ativo")
        return True

class ValidadorVenda:
    @staticmethod
    def validar_campos_criar(produto_id, quantidade):
        if not produto_id or not quantidade:
            raise ValueError("Campos obrigatórios: produto_id, quantidade")
        
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade deve ser um número inteiro maior que zero")
        
        return True
    
    @staticmethod
    def validar_estoque(produto, quantidade):
        if quantidade > produto.quantidade_estoque:
            raise ValueError(f"Quantidade insuficiente em estoque. Disponível: {produto.quantidade_estoque}")
        return True
    
    @staticmethod
    def validar_seller_ativo(seller_id):
        user = User.query.filter_by(id=seller_id).first()
        if not user:
            raise ValueError("Seller não encontrado")
        if user.status != 'ativo':
            raise ValueError("Seller inativo não pode vender")
        return True

class ValidadorUsuario:
    @staticmethod
    def validar_campos_registro(name, email, password, celular, cnpj):
        if not name or not isinstance(name, str):
            raise ValueError("Nome é obrigatório")
        
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        if not password or len(password) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        
        if not celular:
            raise ValueError("Celular é obrigatório")
        
        if not cnpj or len(cnpj) != 14:
            raise ValueError("CNPJ inválido")
        
        return True
    
    @staticmethod
    def validar_email_unico(email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValueError("Email já cadastrado")
        return True