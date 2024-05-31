from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import uuid
from schemas import OrderSchema
from models import OrderModel

blueprint = Blueprint('orders', __name__, description='Orders API')


@blueprint.route('/orders/<int:order_id>')
class Order(MethodView):

    @blueprint.response(200, 'Success')
    @jwt_required()
    def get(self, order_id):
        """Get order by ID"""
        try:
            order = OrderModel.query.get(order_id)
            if order:
                return jsonify(order)
            else:
                abort(404, message='Order not found')
        except SQLAlchemyError as e:
            abort(500, message=str(e))


    @blueprint.arguments(OrderSchema)
    @blueprint.response(201, 'Order successfully created')
    @jwt_required()
    def post(self, order):
        """Create a new order"""
        pass
    @blueprint.arguments(OrderSchema)
    @blueprint.response(200, 'Order successfully updated')
    def put(self, order, order_id):
        """Update an order"""
        pass

    @blueprint.response(204, 'Order successfully deleted')
    def delete(self, order_id):
        """Delete an order"""
        pass