from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
import random
from flask_jwt_extended import create_access_token

class UserService:

    @staticmethod
    def gerar_token():
        token = random.randint(1000, 9999)
        return token

    @staticmethod
    def create_user(name, email, password, cnpj, celular, status):
        from src.Infrastructure.http.whats_app import WhatsAppService
        gerar_token_usuario = UserService.gerar_token()    
        user = User(name=name, email=email, password=password, cnpj=cnpj, celular=celular, status=status, token = gerar_token_usuario)        
        db.session.add(user)
        db.session.commit() 

        WhatsAppService.enviar_codigo(celular, gerar_token_usuario)  
        return UserDomain(user.id, user.name, user.email, user.password, user.cnpj, user.celular, user.status)
    
    @staticmethod
    def update_user(data, user_id):
        name = data.get('name')
        password = data.get('password')
        cnpj = data.get('cnpj')
        celular = data.get('celular')

        user = User.query.get(user_id)

        if not user:
            return {"erro": "Usuário não encontrado"}, 404
        
        if name:
            user.name = name

        if password:
            user.password = password

        if cnpj:
            user.cnpj = cnpj

        if celular:
            user.celular = celular

        db.session.commit()

        return {"message": "Usuário atualizado com sucesso"}, 200
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)

        if not user:
            return {"erro": "Usuário não encontrado"}, 404

        if user.status == "inativo":
            return {"erro": "Usuário já está inativo"}, 400

        user.status = "inativo"
        db.session.commit()

        return {"message": "Usuário desativado com sucesso"}, 200
    
    @staticmethod
    def verify_token(celular, token):
        user = User.query.filter_by(celular=celular, token=token).first()
        
        if not user:
            return {"erro": "Token inválido ou celular não encontrado"}, 400
        
        user.status = "ativo"
        user.token = None
        
        db.session.commit()
        
        return {"message": "Usuário verificado com sucesso"}, 200

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"erro": "Usuário não encontrado"}, 404
        
        if user.password != password:
            return {"erro": "Senha inválida"}, 401
        
        if user.status != 'ativo':
            return {"erro": "Conta não ativada"}, 403
        
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200