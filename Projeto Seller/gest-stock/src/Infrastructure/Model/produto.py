from src.config.data_base import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='ativo')
    imagem = db.Column(db.String(255), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "name": self.nome,
            "preco": self.preco,
            "price": self.preco,
            "quantidade_estoque": self.quantidade_estoque,
            "quantity": self.quantidade_estoque,
            "stock_quantity": self.quantidade_estoque,
            "stock": self.quantidade_estoque,
            "status": self.status,
            "imagem": self.imagem,
            "image": self.imagem,
            "seller_id": self.seller_id,
            "sellerId": self.seller_id
        }