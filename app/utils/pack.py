from flask import jsonify


def ok_response(result=None):
    payload = {'code': 200}

    payload['message'] = "ok"
    if (result):
        payload['result'] = result
    response = jsonify(payload)
    return response


def error_response(dic):
    payload = {'code': dic["code"]}
    if dic:
        payload['message'] = dic["message"]
    response = jsonify(payload)
    return response


USER_NOT_LOGIN = {"code": 1001, "message": "token无效，用户未登录"}
PERMISSION_DENIED = {"code": 1002, "message": "非管理员用户，无法进行此操作"}

PICTURE_ALREADY_FILLED = {"code": 2001, "message": "图片已经被填充完整"}
PICTURE_ALTER_FAILED_PARAM = {"code": 2002, "message": "参数错误，图片修改失败"}
PICTURE_ALTER_FAILED_AUTH = {"code": 2003, "message": "无管理员权限，无法修改"}

COMMENT_LIKE_FAILED_PARAM = {"code":3001,"message":"参数错误，点赞失败"}
COMMENT_DISLIKE_FAILED_PARAM = {"code":3001,"message":"参数错误，点踩失败"}
COMMENT_LIKE_FAILED_EXSIT = {"code":3002,"message":"当前操作非法，因为已经处于该状态"}