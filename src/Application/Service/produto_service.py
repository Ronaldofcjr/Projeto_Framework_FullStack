from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.produto import Produto
from src.config.data_base import db 
from src.Domain.exceptions import NotFoundError, ValidationError

class ProdutoService:
    @staticmethod
    def create_product(name, preco, quantidade, status, img, user_id):
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            raise ValidationError("Preço inválido")

        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValidationError("Quantidade inválida")

        if preco < 0:
            raise ValidationError("Preço não pode ser negativo")

        if quantidade < 0:
            raise ValidationError("Quantidade não pode ser negativa")
        
        if status not in ["Ativo", "Inativo"]:
            raise ValidationError("Status inválido")

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
    def list_products(user_id):
        produtos = Produto.query.filter_by(user_id=user_id).all()

        return [
            ProdutoDomain(produto.id, produto.name, produto.preco, produto.quantidade, produto.status, produto.img, produto.user_id)
            for produto in produtos       
        ]

    @staticmethod
    def list_product(id, user_id):
        produto = Produto.query.filter_by(id=id, user_id=user_id).first()

        if not produto:
            raise NotFoundError("Produto não encontrado")

        return ProdutoDomain(produto.id, produto.name, produto.preco, produto.quantidade, produto.status, produto.img, produto.user_id)

    @staticmethod
    def update_product(data, id, user_id):
        produto = Produto.query.filter_by(id=id, user_id=user_id).first()
        
        if not produto:
            raise NotFoundError("Produto não encontrado")

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
                raise ValidationError("Preço inválido")

            if preco < 0:
                raise ValidationError("Preço não pode ser negativo")

            produto.preco = preco

        if quantidade is not None:
            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                raise ValidationError("Quantidade inválida")

            if quantidade < 0:
                raise ValidationError("Quantidade não pode ser negativa")

            produto.quantidade = quantidade

        if status is not None:
            if status not in ["Ativo", "Inativo"]:
                raise ValidationError("Status inválido")
            produto.status = status

        if img is not None:
            produto.img = img

        db.session.commit()

        return ProdutoDomain(produto.id, produto.name, produto.preco, produto.quantidade, produto.status, produto.img, produto.user_id)

    @staticmethod
    def inactivate_product(id, user_id):
        produto = Produto.query.filter_by(id=id, user_id=user_id).first()

        if not produto:
            raise NotFoundError("Produto não encontrado")
        
        if produto.status == "Inativo":
            raise ValidationError("Produto já está inativo")
        
        produto.status = "Inativo"
        db.session.commit()

        return ProdutoDomain(produto.id, produto.name, produto.preco, produto.quantidade, produto.status, produto.img, produto.user_id)
