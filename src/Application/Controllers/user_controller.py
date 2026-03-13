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