from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.vendas_service import VendasService
from src.Domain.exceptions import NotFoundError, ValidationError

class VendasController:

    @staticmethod
    def create_venda():
        user_id = int(get_jwt_identity())

        data = request.get_json()
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade')

        if produto_id is None or quantidade is None:
            return make_response(jsonify({"erro": "Campos obrigatórios"}), 400)

        try:
            venda = VendasService.create_venda(produto_id, quantidade, user_id)

            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "venda": venda.to_dict()
            }), 201)

        except ValidationError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        
        except NotFoundError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        
        except Exception as e:
            print(f"Erro ao criar venda: {str(e)}")
            return make_response(jsonify({"erro": "Erro interno"}), 500)