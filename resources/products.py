from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import db
import uuid
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import ProductSchema, ProductUpdateSchema
from models import ProductModel


blueprint = Blueprint('products', __name__, description='Products API')

@blueprint.route('/products/<string:product_id>')
class Product(MethodView):

    @blueprint.response(200, 'Success')
    #@jwt_required()
    def get(self, product_id):
        """Get product by ID"""
        try:
            product = ProductModel.query.get(product_id)
            if product:
                return jsonify(product.to_dict()), 200
            else:
                abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))



    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, 'Product successfully updated')
    @jwt_required()
    def put(self, product_data, product_id):
        """Update a product"""
        try:
            product = ProductModel.query.get(product_id)
            if product:
                for key, value in product_data.items():
                    setattr(product, key, value)
                db.session.commit()
                return jsonify(product.to_dict()), 200
            else:
                abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))


    @jwt_required()
    def delete(self, product_id):
        """Delete a product"""
        try:
            product = ProductModel.query.get(product_id)
            if product:
                db.session.delete(product)
                db.session.commit()
                return jsonify('product deleted successfully'), 204
            else:
                abort(404, message='Product not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))




@blueprint.route('/products')
class ProductList(MethodView):

    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products"""
        products = ProductModel.query.all()
        return jsonify([product.to_dict() for product in products]), 200

    @blueprint.arguments(ProductSchema)
    def post(self, product):
        """Create a new product validate before creating"""

        new_product = ProductModel(**product)

        try:
            db.session.add(new_product)
            db.session.commit()
            return jsonify(new_product.to_dict()), 201
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))





