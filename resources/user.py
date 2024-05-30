from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blueprint = Blueprint("Users", "users", description="Operations on users")

@blueprint.route("/register")
class UserRegister(MethodView):
    @blueprint.arguments(UserSchema)
    @blueprint.response(201, "User successfully created")
    def post(self, user):
        """Create a new user"""
        if UserModel.query.filter_by(username=user["username"]).first():
            abort(409, message="User already exists")
        user['username'] = user['username'].lower()
        user["password"] = pbkdf2_sha256.hash(user["password"])
        new_user = UserModel(**user)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, 201
        except Exception as e:
            abort(400, message=str(e))