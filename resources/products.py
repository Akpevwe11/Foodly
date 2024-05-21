from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from db import products
import uuid


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

    @blueprint.arguments(ProductSchema)
    @blueprint.response(200, 'Product successfully updated')
    def put(self, product, product_id):
        """Update a product"""
        products[product_id] = product
        return products[product_id]

    @blueprint.response(204, 'Product successfully deleted')
    def delete(self, product_id):
        """Delete a product"""
        try:
            del products[product_id]
            return '', 204
        except KeyError:
            abort(404, message='Product not found')


def post():
    """Create a new product"""
    abort(405)


@blueprint.route('/products')
class ProductList(MethodView):

    @blueprint.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products"""
        return products.values()

    @blueprint.arguments(ProductSchema)
    @blueprint.response(201, 'Product successfully created')
    def post(self, product):
        """Create a new product validate before creating"""

        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        product_id = str(uuid.uuid4())
        product = {'name': name, 'price': price}
        return jsonify({'id': product_id, **product}), 201


