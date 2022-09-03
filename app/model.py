# coding: utf-8
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from app.extensions import db
from flask import g


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    father_id = db.Column(db.Integer)
    type = db.Column(db.Integer)
    like_number = db.Column(db.Integer)
    dislike_number = db.Column(db.Integer)
    userid = db.Column(db.String(255))
    picture = db.Column(db.JSON)
    nickname = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    isShow = db.Column(db.Integer, server_default=db.FetchedValue())
    question = db.Column(db.Integer)
    is_special = db.Column(db.Integer)
    root_comment_id = db.Column(db.Integer)
    def __init__(self,dic):
        if(dic):
            self.id = dic[0]
            self.comment = dic[1]
    def to_random_dic(self):
        return {
            "id":self.id,
            "comment":self.comment
        }

    def is_like(self):
        userid = g.userid
        user_like : UserLike = UserLike.query.filter(and_(UserLike.userid == userid,UserLike.comment_id==self.id,UserLike.type==1)).first()
        if(user_like):
            return True
        else:
            return False
    def is_dislike(self):
        userid = g.userid
        user_like : UserDislike = UserDislike.query.filter(and_(UserDislike.userid == userid,UserDislike.comment_id==self.id,UserDislike.type==1)).first()
        if(user_like):
            return True
        else:
            return False
    def to_dic(self):


        return {
            "id":self.id,
            "comment":self.comment,
            "fatherId":self.father_id,
            "likeNumber":self.like_number,
            "dislikeNumber":self.dislike_number,
            "nickname":self.nickname,
            "avatar":self.avatar,
            "isLiked":self.is_like(),
            "isDislike":self.is_dislike()
        }


class Picture(db.Model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True, unique=True, server_default=db.FetchedValue())
    array = db.Column(db.Text)
    state = db.Column(db.Integer)

    def to_dic(self):
        return {
            "id":self.id,
            "array":json.loads(self.array),
            "state":self.state
        }
    def count(self):
        total = 0
        for item in json.loads(self.array):
            for j in item:
                if j == 0:
                    total += 1
        self.state = total
        return total
class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    like_number = db.Column("likeNumber",db.Integer)
    dislike_number = db.Column("dislikeNumber",db.Integer)
    picture = db.Column(db.JSON)

    def to_dic(self):
        return {"id":self.id,
                "content":self.content,
                "likeNumber":self.like_number,
                "dislikeNumber":self.dislike_number,
                "picture":self.picture,
                "isLike":self.is_like(),
                "isDislike":self.is_dislike()
                }

    def is_like(self):
        userid = g.userid
        user_like: UserLike = UserLike.query.filter(
            and_(UserLike.userid == userid, UserLike.comment_id == self.id, UserLike.type == 0)).first()
        if (user_like):
            return True
        else:
            return False

    def is_dislike(self):
        userid = g.userid
        user_like: UserDislike = UserDislike.query.filter(
            and_(UserDislike.userid == userid, UserDislike.comment_id == self.id, UserDislike.type == 0)).first()
        if (user_like):
            return True
        else:
            return False

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(255), primary_key=True, unique=True)
    tapNumber = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())


    def to_dic(self):
        return {
            "id":self.id,
            "tapNumber":self.tapNumber,
            "isAdmin":self.is_admin
        }


class UserLike(db.Model):
    __tablename__ = 'user_like'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column('userid', db.String(255))
    comment_id = db.Column('comment_id', db.Integer)
    created_at = db.Column('created_at', db.DateTime, server_default=db.FetchedValue())
    type = db.Column('type', db.Integer)


class UserDislike(db.Model):
    __tablename__ = 'user_dislike'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column('userid', db.String(255))
    comment_id = db.Column('comment_id', db.Integer)
    created_at = db.Column('created_at', db.DateTime, server_default=db.FetchedValue())
    type = db.Column('type', db.Integer)
