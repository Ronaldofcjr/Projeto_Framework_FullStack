from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.config.data_base import db 

class ProdutoService:
    @staticmethod
    def create_product(name, preco, quantidade, status, img, user_id):
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")

        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")

        produto = Produto(
            name=name,
            preco=preco,
            quantidade=quantidade,
            status=status,
            img=img,
            user_id=user_id
        )

        db.session.add(produto)
        db.session.commit()

        return ProdutoDomain(produto.id, produto.name, produto.preco, produto.quantidade, produto.status, produto.img, produto.user_id)

    @staticmethod
    def list_products():
        pass

    @staticmethod
    def list_product(id):
        pass

    @staticmethod
    def update_product():
        pass
    
    @staticmethod
    def inactivate_product():
        pass