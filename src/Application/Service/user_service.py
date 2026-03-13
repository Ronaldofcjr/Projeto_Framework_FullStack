from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
import random

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
    def atualizar_usuario(data):

        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        cnpj = data.get('cnpj')
        celular = data.get('celular')

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"erro": "Email não encontrado"}, 400

        user.name = name
        user.password = password
        user.cnpj = cnpj
        user.celular = celular

        db.session.commit()

        return {"message": "Usuário atualizado com sucesso"}, 200
    

    @staticmethod
    def delete_user_by_email(email):

        user = User.query.filter_by(email=email).first()

        if not user:
            raise Exception("Usuário não encontrado")

        if user.status == "inativo":
            raise Exception("Usuário já está inativo")

        user.status = "inativo"
        db.session.commit()

        return True
