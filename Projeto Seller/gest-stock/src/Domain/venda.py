class VendaDomain:
    def __init__(self, id, produto_id, quantidade, preco_unitario, valor_total, seller_id, created_at):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.valor_total = valor_total
        self.seller_id = seller_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "valor_total": self.valor_total,
            "seller_id": self.seller_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }