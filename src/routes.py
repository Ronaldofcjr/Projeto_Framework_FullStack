from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.produto_controller import ProdutoController
from flask import jsonify, make_response
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
    
    @app.route('/user', methods=['PUT'])
    @jwt_required()
    def update_user():
        return UserController.update_user()
    
    @app.route('/user', methods=["DELETE"])
    @jwt_required()
    def delete_user():
        return UserController.delete_user()
    
    @app.route('/user/login', methods=["POST"])
    def login():
        return UserController.login_user()
    
    @app.route('/product', methods=['POST'])
    @jwt_required()
    def create_product():
        return ProdutoController.create_product()
    
    @app.route('/product', methods=['GET'])
    @jwt_required()
    def list_products():
        return ProdutoController.list_products()
    
    @app.route('/product/<int:id>', methods=['GET'])
    @jwt_required()
    def list_product():
        return ProdutoController.list_product()
    
    @app.route('/product', methods=['PUT'])
    @jwt_required()
    def update_product():
        return ProdutoController.update_product()
    
    @app.route('/product', methods=['PATCH'])
    @jwt_required()
    def inactivate_product():
        return ProdutoController.inactivate_product()