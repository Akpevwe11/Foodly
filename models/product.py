from db import db
import uuid

class ProductModel(db.Model):
    __tablename__: str = 'products'

    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    shop_id = db.Column(db.String, db.ForeignKey('shops.id'), unique=False, nullable=False)
    shop = db.relationship('ShopModel', back_populates='products')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'shop_id': self.shop_id
        }


# Path: schemas.py
