from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
from src.Infrastructure.http.whats_app import WhatsAppService
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from src.Domain.exceptions import (NotFoundError, ValidationError, UnauthorizedError, ForbiddenError)

class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, celular, status):
        if User.query.filter_by(celular=celular).first():
            raise ValidationError("Celular já cadastrado")
        if User.query.filter_by(email=email).first():
            raise ValidationError("Email já cadastrado")
        if User.query.filter_by(cnpj=cnpj).first():
            raise ValidationError("CNPJ já cadastrado")

        hashed_password = generate_password_hash(password)
        gerar_token_usuario = WhatsAppService.gerar_token()

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            cnpj=cnpj,
            celular=celular,
            status=status,
            token=gerar_token_usuario
        )

        db.session.add(user)
        db.session.commit()

        WhatsAppService.enviar_codigo(celular, gerar_token_usuario)

        return UserDomain(user.id, user.name, user.email, user.cnpj, user.celular, user.status)

    @staticmethod
    def update_user(data, user_id):
        user = User.query.get(user_id)

        if not user:
            raise NotFoundError("Usuário não encontrado")

        name = data.get('name')
        password = data.get('password')
        cnpj = data.get('cnpj')
        celular = data.get('celular')
        email = data.get('email')

        if celular and User.query.filter(User.celular == celular, User.id != user_id).first():
            raise ValidationError("Celular já cadastrado")

        if email and User.query.filter(User.email == email, User.id != user_id).first():
            raise ValidationError("Email já cadastrado")

        if cnpj and User.query.filter(User.cnpj == cnpj, User.id != user_id).first():
            raise ValidationError("CNPJ já cadastrado")

        if name is not None:
            user.name = name

        if password is not None:
            user.password = generate_password_hash(password)

        if cnpj is not None:
            user.cnpj = cnpj

        if celular is not None:
            user.celular = celular

        if email is not None:
            user.email = email

        db.session.commit()

        return UserDomain(user.id, user.name, user.email, user.cnpj, user.celular, user.status)

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)

        if not user:
            raise NotFoundError("Usuário não encontrado")

        if user.status == "Inativo":
            raise ValidationError("Usuário já está inativo")

        user.status = "Inativo"
        db.session.commit()

        return UserDomain(user.id, user.name, user.email, user.cnpj, user.celular, user.status)

    @staticmethod
    def verify_token(email, token):
        user = User.query.filter_by(email=email, token=token).first()
        
        if not user:
            raise ValidationError("Token inválido ou e-mail não encontrado")
        
        user.status = "Ativo"
        user.token = None
        
        db.session.commit()
        
        return {"mensagem": "Usuário verificado com sucesso"}

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            raise NotFoundError("Usuário não encontrado")
        
        if not check_password_hash(user.password, password):
            raise UnauthorizedError("Senha inválida")
        
        if user.status != 'Ativo':
            raise ForbiddenError("Conta não ativada")
        
        access_token = create_access_token(identity=str(user.id))
        return {
            "mensagem": "Usuário logado com sucesso",
            "access_token": access_token
        }