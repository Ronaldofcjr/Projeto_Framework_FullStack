class VendasDomain:
    def __init__ (self, id, produto_id, quantidade, preco_unitario):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario
        }
