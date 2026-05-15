from src.Domain.vendas import VendasDomain
from src.Infrastructure.Model.vendas import Venda
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Domain.exceptions import NotFoundError, ValidationError

class VendasService:

    @staticmethod
    def create_venda(produto_id, quantidade, user_id, preco_unitario=None):

        #valida quantidade
        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValidationError("Quantidade inválida")

        if quantidade <= 0:
            raise ValidationError("Quantidade deve ser maior que zero")

        #valida usuário ativo
        user = User.query.get(user_id)

        if not user or user.status.strip().lower() != "ativo":
            raise ValidationError("Usuário inativo não pode realizar vendas")

        #busca produto do usuário
        produto = Produto.query.filter_by(id=produto_id, user_id=user_id).first()

        if not produto:
            raise NotFoundError("Produto não encontrado")

        #valida produto ativo
        if produto.status.strip().lower() != "ativo":
            raise ValidationError("Produto inativo")

        #valida estoque
        if produto.quantidade < quantidade:
            raise ValidationError("Quantidade em estoque insuficiente")

        #preço REAL do momento
        preco_final = float(preco_unitario) if preco_unitario is not None else produto.preco

        venda = Venda(
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_final
        )

        db.session.add(venda)

        #atualiza estoque
        produto.quantidade -= quantidade

        #transação segura
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return VendasDomain(
            venda.id,
            venda.produto_id,
            venda.quantidade,
            venda.preco_unitario
        )
    
    @staticmethod
    def list_vendas(user_id):
        vendas = Venda.query.join(Produto).filter(Produto.user_id == user_id).all()

        return [
            VendasDomain(v.id, v.produto_id, v.quantidade, v.preco_unitario)
            for v in vendas
        ]