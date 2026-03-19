from src.Application.Controllers.user_controller import UserController
from src.Infrastructure.Model.user import User 
from src.Application.Service.user_service import UserService
from flask import jsonify, make_response, request
from src.config.data_base import db
from flask_jwt_extended import jwt_required

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
        return UserController.verify_token()
    
    @jwt_required
    @app.route('/user', methods=['PUT'])
    def update_user():
        return UserController.update_user()
    
    @jwt_required
    @app.route("/user", methods=["DELETE"])
    def delete_user():
        return UserController.delete_user()
    
    @app.route("/user/login", methods=["POST"])
    def login():
        return UserController.login_user()