class ProdutoDomain:
    def __init__(self, id, nome, preco, quantidade_estoque, status, imagem, seller_id):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.status = status
        self.imagem = imagem
        self.seller_id = seller_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade_estoque": self.quantidade_estoque,
            "status": self.status,
            "imagem": self.imagem,
            "seller_id": self.seller_id,
        }