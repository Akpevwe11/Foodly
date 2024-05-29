from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from db import db
import uuid
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import ProductSchema, ProductUpdateSchema
from models import ProductModel


blueprint = Blueprint('products', __name__, description='Products API')

@blueprint.route('/products/<int:product_id>')
class Product(MethodView):

    @blueprint.response(200, 'Success')
    def get(self, product_id):
        """Get product by ID"""
        return products.get(product_id)

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, 'Product successfully created')
    def post(self, product):
        """Create a new product"""
        product_id = str(uuid.uuid4())
        products[product_id] = product
        return { 'id': product_id, **product }, 201

    @blueprint.arguments(ProductUpdateSchema)
    @blueprint.response(200, 'Product successfully updated')
    def put(self, product_data, product_id):
        """Update a product"""
        try:
            product = product_data[product_id]
            product |= product_data
            return product
        except KeyError:
            abort(404, message='Product not found')

    @blueprint.response(204, 'Product successfully deleted')
    def delete(self, product_id):
        """Delete a product"""
        try:
            del products[product_id]
            return '', 204
        except KeyError:
            abort(404, message='Product not found')




@blueprint.route('/products')
class ProductList(MethodView):

    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products"""
        return products.values()

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, 'Product successfully created')
    def post(self, existing_product):
        """Create a new product validate before creating"""

        new_product = ProductModel(**existing_product)

        try:
            db.session.add(new_product)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return jsonify(new_product), 201



