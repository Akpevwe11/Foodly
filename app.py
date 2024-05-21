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
    pass


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({ 'error': 'Product not found' }), 404
    data = request.get_json()

    # Validate incoming data
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    if 'id' not in data or not isinstance(data['id'], str):
        return jsonify({'error': 'Invalid or missing id'}), 400
    if 'name' not in data or not isinstance(data['name'], str):
        return jsonify({'error': 'Invalid or missing name'}), 400
    if 'price' not in data or not isinstance(data['price'], (int, float)):
        return jsonify({'error': 'Invalid or missing price'}), 400

    # here I want to use a try catch in case the product key does not exist
    try:
        product_id = data.get('id')
        name = data.get('name')
        price = data.get('price')
        product['id'] = product_id
        product['name'] = name
        product['price'] = price
        return jsonify(product)
    except KeyError:
        return jsonify({'error': 'Invalid or missing id'}), 400


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products.get(product_id)
    if product is None:
        return jsonify({ 'error': 'Product not found' }), 404
    del products[product_id]
    return jsonify({ 'message': 'Product deleted' })



if __name__ == '__main__':
    app.run()