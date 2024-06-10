from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (create_access_token,
                                get_jwt, jwt_required, create_refresh_token, get_jwt_identity)
from db import db
from models import UserModel
from schemas import UserSchema
from blacklist import BLACKLIST

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

@blueprint.route('/login')
class UserLogin(MethodView):
    @blueprint.arguments(UserSchema)
    def post(self, user):
        """user Login"""
        user = UserModel.query.filter(UserModel.username == user['username']).first()
        if user and pbkdf2_sha256.verify(user['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}, 200


        abort(401, message="Invalid credentials")

@blueprint.route('/logout')

class UserLogout(MethodView):
    @jwt_required()
    def delete(self):
        """User Logout"""
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@blueprint.route('/refresh')
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh token"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"access_token": new_token}, 200



