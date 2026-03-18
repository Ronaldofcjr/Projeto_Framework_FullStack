from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')
        status = "inativo"

        if not name or not email or not password or not cnpj or not celular:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password, cnpj, celular, status)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
    
    @staticmethod
    def atualizar_usuario():
        data = request.get_json()

        response, status = UserService.atualizar_usuario(data)

        return jsonify(response), status
    
    
    @staticmethod
    def delete_user_by_email(email):
        try:
            UserService.delete_user_by_email(email)
            return {"message": f"Usuário {email} desativado com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    @staticmethod
    def verify_token():
        data = request.get_json()
        celular = data.get('celular')
        token = data.get('token') 

        result, status_code = UserService.verify_token(celular, token)
        return jsonify(result), status_code
    
    @staticmethod
    def login():
        data = request.json

        result = UserService.login_user(data["email"], data["senha"])

        if "erro" in result:
            return jsonify(result), result["status"]  
        
        return jsonify(result), 200