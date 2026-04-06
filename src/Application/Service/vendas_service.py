from src.Domain.vendas import VendasDomain
from src.Domain.produto import ProdutoDomain
from src.Infrastructure.Model.vendas import Venda
from src.config.data_base import db
from src.Domain.exceptions import NotFoundError, ValidationError

class VendasService:
    @staticmethod
    def create_venda(produto_id, quantidade, preco_unitario):
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValidationError("Quantidade inválida")

        try:
            preco_unitario = float(preco_unitario)
        except (TypeError, ValueError):
            raise ValidationError("Preço unitário inválido")

        if quantidade <= 0:
            raise ValidationError("Quantidade deve ser maior que zero")

        if preco_unitario <= 0:
            raise ValidationError("Preço unitário deve ser maior que zero")

        produto = ProdutoDomain.get_produto_by_id(produto_id)

        if not produto:
            raise NotFoundError("Produto não encontrado")

        if produto.quantidade < quantidade:
            raise ValidationError("Quantidade em estoque insuficiente")

        venda = Venda(
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )

        db.session.add(venda)

        # Atualiza a quantidade do produto
        produto.quantidade -= quantidade
        db.session.commit()

        return VendasDomain(venda.id, venda.produto_id, venda.quantidade, venda.preco_unitario)


