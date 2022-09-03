from flask import Blueprint, g, request
from app.extensions import db
from app.api import bp
from app.api.auth import token_user, token_admin
from app.model import User
from app.utils import pack

user_bp = Blueprint('user', __name__)
bp.register_blueprint(user_bp, url_prefix='/user')


@user_bp.route("get", methods=["GET"])
@token_user.login_required
def get_user_info():
    userid = g.userid
    user: User = User.query.get(userid)
    return pack.ok_response(user.to_dic())


@user_bp.route("admin/add", methods=["GET"])
@token_admin.login_required
def add_new_admin():
    userid = request.args.get("userid")
    user: User = User.query.get(userid)
    user.is_admin = 1
    db.session.commit()
    return pack.ok_response()
