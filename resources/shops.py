from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import ShopModel
from schemas import ShopSchema


blueprint = Blueprint("shops", "__name__", description="Operations on shops")

@blueprint.route("/shop/<int:shop_id>")
class Shop(MethodView):

    @jwt_required()
    def get(self, shop_id):
        """get shop by ID"""
        try:
            shop = ShopModel.query.get(shop_id)
            if shop:
                return jsonify(shop)
            else:
                abort(404, message="Shop not found")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @jwt_required()
    def delete(self, shop_id):
        """delete a shop"""
        try:
            shop = ShopModel.query.get(shop_id)
            if shop:
                db.session.delete(shop)
                db.session.commit()
                return jsonify(shop), 204
            else:
                abort(404, message="Shop not found")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @jwt_required()
    def put(self, shop_id):
        """edit a shop"""
        try:
            shop = ShopModel.query.get(shop_id)
            if shop:
                for key, value in request.json.items():
                    setattr(shop, key, value)
                db.session.commit()
                return jsonify(shop)
            else:
                abort(404, message="Shop not found")
        except SQLAlchemyError as e:
            abort(500, message=str(e))




@blueprint.route("/shops")
class Shops(MethodView):


    @blueprint.arguments(ShopSchema)
    def post(self):
        """create a new shop"""
        shop = request.json
        new_shop = ShopModel(**shop)
        try:
            db.session.add(new_shop)
            db.session.commit()
            return jsonify(new_shop), 201
        except IntegrityError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=str(e))