from flask import request, jsonify, make_response
from src.Application.Service.produto_service import ProdutoService
from flask_jwt_extended import get_jwt_identity
from src.Domain.exceptions import NotFoundError, ValidationError
import os
from werkzeug.utils import secure_filename


class ProdutoController:
    @staticmethod
    def create_product():
        user_id = int(get_jwt_identity())

        name = request.form.get('name')
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        img = request.files.get('img')
        status = request.form.get('status')

        if img:

            os.makedirs('uploads', exist_ok=True)

            nome_arquivo = secure_filename(img.filename)

            caminho = os.path.join('uploads', nome_arquivo)

            img.save(caminho)
        
        if name is None or preco is None or quantidade is None or status is None or img is None:
            return make_response(jsonify({"erro": "Campos obrigatórios"}), 400)
        
        try:
            produto = ProdutoService.create_product(name, preco, quantidade, status, nome_arquivo, user_id)
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

        dados = {

            "name" : request.form.get('name'),
            "preco" : request.form.get('preco'),
            "quantidade" : request.form.get('quantidade'),
            "status" : request.form.get('status')

        }

        img = request.files.get('img')

        if img:
            os.makedirs('uploads', exist_ok=True)

            nome_arquivo = secure_filename(img.filename)

            caminho = os.path.join('uploads', nome_arquivo)

            img.save(caminho)

            dados['img'] = nome_arquivo

        user_id = int(get_jwt_identity())

        try:
            produto = ProdutoService.update_product(dados, id, user_id)
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