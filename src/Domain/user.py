class UserDomain:
    def __init__(self, id, name, email, cnpj, celular, status):
        self.id = id
        self.name = name
        self.email = email
        self.cnpj = cnpj
        self.celular = celular
        self.status = status        
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cnpj": self.cnpj,
            "celular": self.celular,
            "status": self.status
        }