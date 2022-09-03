from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.extensions import db
from app.model import User
from app.utils import jwt, pack

token_user = HTTPTokenAuth()
token_admin = HTTPTokenAuth()

@token_user.verify_token
def verify_token(token):
    '''用于检查用户请求是否有token，并且token真实存在，还在有效期内'''
    try:
        userid = jwt.get_userid(token)
        user: User = User.query.get(userid)
        if (user is None):
            new_user = User()
            new_user.is_admin = 0
            new_user.tapNumber = 0
            new_user.id = userid
            db.session.add(new_user)
            db.session.commit()
        g.userid = userid
        return True
    except:
        return False


@token_user.error_handler
def token_auth_error():
    '''用于在 Token Auth 认证失败的情况下返回错误响应'''
    return pack.error_response(pack.USER_NOT_LOGIN)

@token_admin.verify_token
def verify_token_admin(token):
    '''用于检查用户请求是否有token，并且token真实存在，还在有效期内'''
    try:
        userid = jwt.get_userid(token)
        user: User = User.query.get(userid)
        if (user is None):
            new_user = User()
            new_user.is_admin = 0
            new_user.tapNumber = 0
            new_user.id = userid
            db.session.add(new_user)
            db.session.commit()
            return False
        g.userid = userid
        if(user.is_admin==1):
            return True
    except:
        return False


@token_admin.error_handler
def token_auth_error():
    '''用于在 Token Auth 认证失败的情况下返回错误响应'''
    return pack.error_response(pack.PERMISSION_DENIED)
