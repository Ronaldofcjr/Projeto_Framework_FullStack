from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import get_jwt_identity
from src.Domain.exceptions import (NotFoundError, ValidationError, UnauthorizedError, ForbiddenError)

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')
        status = "Inativo"

        if not name or not email or not password or not cnpj or not celular:
            return make_response(jsonify({"erro": "Campos obrigatórios"}), 400)

        try:
            user = UserService.create_user(name, email, password, cnpj, celular, status)
            return make_response(jsonify({
                "mensagem": "Usuário salvo com sucesso",
                "usuário": user.to_dict()
            }), 201)

        except ValidationError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        
        except Exception as e:
            print("Erro interno:", str(e))
            return{"erro": str(e)}, 500
    
    @staticmethod
    def update_user():
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        try:
            user = UserService.update_user(data, user_id)
            return jsonify({
                "mensagem": "Usuário atualizado com sucesso",
                "usuário": user.to_dict()
            }), 200

        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500
    
    @staticmethod
    def delete_user():
        user_id = int(get_jwt_identity())
        
        try:
            user = UserService.delete_user(user_id)
            return jsonify({
                "mensagem": "Usuário desativado com sucesso",
                "usuário": user.to_dict()
            }), 200

        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500
        
    @staticmethod
    def verify_token():
        data = request.get_json()
        email = data.get('email')
        token = data.get('token') 

        try:
            result = UserService.verify_token(email, token)
            return jsonify(result), 200

        except ValidationError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500
    
    @staticmethod
    def login_user():
        data = request.json

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

        try:
            body = UserService.login_user(email, password)
            return jsonify(body), 200

        except NotFoundError as e:
            return jsonify({"erro": str(e)}), 404

        except UnauthorizedError as e:
            return jsonify({"erro": str(e)}), 401

        except ForbiddenError as e:
            return jsonify({"erro": str(e)}), 403

        except ValidationError as e:
            return jsonify({"erro": str(e)}), 400
        
        except Exception as e:
            return jsonify({"erro": "Erro interno"}), 500