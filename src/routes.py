from src.Application.Controllers.user_controller import UserController
from src.Infrastructure.Model.user import User 
from src.Application.Service.user_service import UserService
from flask import jsonify, make_response, request
from src.config.data_base import db

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/user/verify', methods=['POST'])
    def verify_token():
        data = request.get_json()
        email = data.get('email')
        token = data.get('token')

        user = User.query.filter_by(email=email, token=token).first()

        if not user:
            return make_response(jsonify({"erro": "Token inválido ou Email não encontrado"}), 400)

        user.status = "ativo"
        user.token = None

        db.session.commit()

        return {"message": "Usuário verificado com sucesso"}
    
    @app.route('/users/atualizar_usuario', methods=['PUT'])
    def atualizar_usuario():
        return UserController.atualizar_usuario()
    
    @app.route("/users/<string:email>", methods=["DELETE"])
    def delete_user_by_email_route(email):
        return UserController.delete_user_by_email(email)
    

    
    

