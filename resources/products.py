from flask.views import MethodView
from flask_smorest import Blueprint


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