from flask import Flask, jsonify, request
from db import products
import uuid

app = Flask(__name__)

@app.route('/')
def hello_world():
    data  = { 'name': 'John', 'age': 30, 'city': 'New York' }
    return jsonify(data)

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({ 'error': 'Product not found' }), 404
    return jsonify(product)

@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    product_id = str(uuid.uuid4())
    product = { 'name': name, 'price': price }
    return jsonify({ 'id': product_id, **product }), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({ 'error': 'Product not found' }), 404
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    product['name'] = name
    product['price'] = price
    return jsonify(product)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({ 'error': 'Product not found' }), 404
    del products[product_id]
    return jsonify({ 'message': 'Product deleted' })



if __name__ == '__main__':
    app.run()