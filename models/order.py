from db import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.String, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('ProductModel', back_populates='orders')
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

