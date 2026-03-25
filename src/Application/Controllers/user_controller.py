from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import get_jwt_identity

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
                "mensagem": "User salvo com sucesso",
                "usuarios": user.to_dict()
            }), 201)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
    
    @staticmethod
    def update_user():
        data = request.get_json()
        user_id = int(get_jwt_identity())
        
        response, status = UserService.update_user(data, user_id)

        return jsonify(response), status
    
    @staticmethod
    def delete_user():
        user_id = int(get_jwt_identity())
        
        response, status = UserService.delete_user(user_id)

        return jsonify(response), status
        
    @staticmethod
    def verify_token():
        data = request.get_json()
        email = data.get('email')
        token = data.get('token') 

        result, status_code = UserService.verify_token(email, token)
        return jsonify(result), status_code
    
    @staticmethod
    def login_user():
        data = request.json

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

        body, status = UserService.login_user(email, password)

        return jsonify(body), status