from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.config.data_base import db 

class ProdutoService:
    @staticmethod
    def create_product(name, preco, quantidade, status, img, user_id):
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            raise ValueError("Preço inválido")

        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("Quantidade inválida")

        if preco < 0:
            raise ValueError("Preço não pode ser negativo")

        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        
        if status not in ["Ativo", "Inativo"]:
            raise ValueError("Status inválido")

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
    def update_product(data, id, user_id):
        produto = Produto.query.filter_by(id=id, user_id=user_id).first()
        
        if not produto:
            raise ValueError("Produto não encontrado")

        name = data.get('name')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        status = data.get('status')
        img = data.get('img')

        if name is not None:
            produto.name = name

        if preco is not None:
            try:
                preco = float(preco)
            except (TypeError, ValueError):
                raise ValueError("Preço inválido")

            if preco < 0:
                raise ValueError("Preço não pode ser negativo")

            produto.preco = preco

        if quantidade is not None:
            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                raise ValueError("Quantidade inválida")

            if quantidade < 0:
                raise ValueError("Quantidade não pode ser negativa")

            produto.quantidade = quantidade

        if status is not None:
            if status not in ["Ativo", "Inativo"]:
                raise ValueError("Status inválido")
            produto.status = status

        if img is not None:
            produto.img = img

        db.session.commit()

        return {"mensagem": "Produto atualizado com sucesso"}

    @staticmethod
    def inactivate_product(id):
        pass