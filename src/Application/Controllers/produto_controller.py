from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService
from flask_jwt_extended import get_jwt_identity
from src.Domain.exceptions import NotFoundError, ValidationError

class ProdutoController:
    @staticmethod
    def create_product():
        user_id = int(get_jwt_identity())

        data = request.get_json()
        name = data.get('name')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        img = data.get('img')
        status = data.get('status')
        
        if name is None or preco is None or quantidade is None or status is None or img is None:
            return make_response(jsonify({"erro": "Campos obrigatórios"}), 400)
        
        try:
            produto = ProdutoService.create_product(name, preco, quantidade, status, img, user_id)
            return make_response(jsonify({
                "mensagem": "Produto salvo com sucesso",
                "produto": produto.to_dict()
            }), 201)

        except ValidationError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500

    @staticmethod
    def list_products():
        user_id = int(get_jwt_identity())

        try:
            produtos = ProdutoService.list_products(user_id)
            return jsonify({
                "produtos": [produto.to_dict() for produto in produtos]
            }), 200
        
        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500

    @staticmethod
    def list_product(id):
        user_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.list_product(id, user_id)
            return jsonify({
                "produto": produto.to_dict()
            }), 200
        
        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500

    @staticmethod
    def update_product(id):
        data = request.get_json()
        user_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.update_product(data, id, user_id)
            return jsonify({
                "mensagem": "Produto atualizado com sucesso",
                "produto": produto.to_dict()
            }), 200

        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500

    @staticmethod
    def inactivate_product(id):
        user_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.inactivate_product(id, user_id)

            return jsonify({
                "mensagem": "Produto desativado com sucesso",
                "produto": produto.to_dict()
            }), 200
        
        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500