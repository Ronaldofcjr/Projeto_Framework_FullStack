from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService
from flask_jwt_extended import get_jwt_identity

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

        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)

    @staticmethod
    def list_products():
        pass

    @staticmethod
    def list_product(id):
        pass
    
    @staticmethod
    def update_product(id):
        data = request.get_json()
        user_id = int(get_jwt_identity())

        try:
            response = ProdutoService.update_product(data, id, user_id)
            return jsonify(response), 200

        except ValueError as e:
            mensagem = str(e)

            if "não encontrado" in mensagem:
                return jsonify({"erro": mensagem}), 404
            else:
                return jsonify({"erro": mensagem}), 400
    
    @staticmethod
    def inactivate_product(id):
        pass