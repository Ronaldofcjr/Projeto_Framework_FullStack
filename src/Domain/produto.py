class ProdutoDomain:
    def __init__(self, id, name, preco, quantidade, status, img, user_id):
        self.id = id
        self.name = name
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.img = img
        self.user_id = user_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "img": self.img,
            "user_id": self.user_id
        }