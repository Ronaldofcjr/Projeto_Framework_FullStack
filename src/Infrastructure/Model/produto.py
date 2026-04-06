from src.config.data_base import db 
class Produto(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='produtos')
    vendas = db.relationship('Venda', back_populates='produto')
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "img": self.img,
            "user_id": self.user_id
        }