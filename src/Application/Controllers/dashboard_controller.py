from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.vendas import Venda
from src.config.data_base import db
from sqlalchemy import func


class DashboardController:

    @staticmethod
    def get_dashboard():
        user_id = int(get_jwt_identity())

        # Total de produtos ativos e inativos
        total_produtos = Produto.query.filter_by(user_id=user_id).count()
        produtos_ativos = Produto.query.filter_by(user_id=user_id, status='Ativo').count()
        produtos_inativos = Produto.query.filter_by(user_id=user_id, status='Inativo').count()

        # Produtos com estoque baixo (menos de 10 unidades, apenas ativos)
        estoque_baixo = Produto.query.filter(
            Produto.user_id == user_id,
            Produto.status == 'Ativo',
            Produto.quantidade < 10
        ).all()

        # Total de vendas e faturamento (join com produto para filtrar por user)
        vendas_query = db.session.query(Venda).join(Produto).filter(Produto.user_id == user_id)

        total_vendas = vendas_query.count()

        faturamento_total = db.session.query(
            func.sum(Venda.preco_unitario * Venda.quantidade)
        ).join(Produto).filter(Produto.user_id == user_id).scalar() or 0.0

        # Top 5 produtos mais vendidos
        top_produtos = db.session.query(
            Produto.name,
            func.sum(Venda.quantidade).label('total_vendido'),
            func.sum(Venda.preco_unitario * Venda.quantidade).label('faturamento')
        ).join(Venda, Venda.produto_id == Produto.id)\
         .filter(Produto.user_id == user_id)\
         .group_by(Produto.id)\
         .order_by(func.sum(Venda.quantidade).desc())\
         .limit(5).all()

        # Últimas 5 vendas
        ultimas_vendas = db.session.query(Venda, Produto.name)\
            .join(Produto, Venda.produto_id == Produto.id)\
            .filter(Produto.user_id == user_id)\
            .order_by(Venda.id.desc())\
            .limit(5).all()

        return jsonify({
            "resumo": {
                "total_produtos": total_produtos,
                "produtos_ativos": produtos_ativos,
                "produtos_inativos": produtos_inativos,
                "total_vendas": total_vendas,
                "faturamento_total": round(faturamento_total, 2)
            },
            "estoque_baixo": [
                {
                    "id": p.id,
                    "name": p.name,
                    "quantidade": p.quantidade,
                    "preco": p.preco
                } for p in estoque_baixo
            ],
            "top_produtos": [
                {
                    "name": row.name,
                    "total_vendido": int(row.total_vendido),
                    "faturamento": round(float(row.faturamento), 2)
                } for row in top_produtos
            ],
            "ultimas_vendas": [
                {
                    "id": venda.id,
                    "produto": nome,
                    "quantidade": venda.quantidade,
                    "preco_unitario": venda.preco_unitario,
                    "total": round(venda.quantidade * venda.preco_unitario, 2)
                } for venda, nome in ultimas_vendas
            ]
        }), 200