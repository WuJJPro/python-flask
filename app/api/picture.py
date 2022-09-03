import json

from flask import Blueprint, request, g
from app.api.auth import token_user, token_admin
from app.model import Picture, User
from app.api import bp
from app.utils import pack
from app.extensions import db

picture = Blueprint('picture', __name__)
bp.register_blueprint(picture, url_prefix='/picture')


@picture.route('/update', methods=["POST"])
@token_user.login_required
def update_picture():
    """接受更新的坐标位置，更新"""
    """参数为新增坐标，图片id，上限十个，post，json"""
    params = request.get_json()
    position_array = params.get("array")
    picture_id = params.get("picture")
    target_picture: Picture = db.session.query(Picture).get(picture_id)
    row_array = json.loads(target_picture.array)
    ori_state = target_picture.state
    if (target_picture.state == 0):
        res = pack.error_response(pack.PICTURE_ALREADY_FILLED)
        return res
    for item in position_array:
        row_array[item[0]][item[1]] = 1
    # 统计剩余块的个数
    count = target_picture.count()
    target_picture.array = str(row_array)
    # 修改用户的tap数
    userid = g.userid
    user: User = User.query.get(userid)
    user.tapNumber+= (ori_state - count)
    # 这个地方有bug，commit没有用
    print(db.session.commit())
    res = pack.ok_response(target_picture.to_dic())
    return res


@picture.route("/get", methods=["GET"])
def get_picture():
    pic: Picture = Picture.query.filter(Picture.state != 0).order_by(Picture.id).first()
    res = pack.ok_response(pic.to_dic())
    return res


@picture.route("/alter", methods=["GET"])
@token_admin.login_required
def alter_picture():
    id = int(request.args.get("id"))
    max_id = Picture.query.count()
    pictures: list[Picture] = Picture.query.all()
    for i in range(id):
        pictures[i].state = 0
        db.session.commit()
    for i in range(id, max_id):
        pictures[i].count()
    db.session.commit()
    return pack.ok_response()
