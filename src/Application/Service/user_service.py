from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, celular, status):        
        user = User(name=name, email=email, password=password, cnpj=cnpj, celular=celular, status=status)        
        db.session.add(user)
        db.session.commit()       
        return UserDomain(user.id, user.name, user.email, user.password, user.cnpj, user.celular, user.status)