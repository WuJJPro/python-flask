from flask import Blueprint, request, g
from sqlalchemy import and_

from app.api import bp
from app.api.auth import token_user
from app.model import Question, Comment, UserLike, UserDislike
from app.utils import pack
from app.extensions import db
question_bp = Blueprint('question', __name__)
bp.register_blueprint(question_bp, url_prefix='/question')

@question_bp.route("getall",methods=["GET"])
@token_user.login_required
def get_all_question():
    questions : list[Question] = Question.query.all()
    for i in range(len(questions)):
        commentCount = Comment.query.filter(Comment.question == questions[i].id).count()
        questions[i] = questions[i].to_dic()
        questions[i]["commentCount"] = commentCount
    return pack.ok_response(questions)

@question_bp.route("like",methods=["POST"])
@token_user.login_required
def question_like():
    params = request.get_json()
    question:Question = Question.query.get(params["id"])

    user_like:UserLike = UserLike.query.filter(and_(UserLike.userid == g.userid,UserLike.comment_id == params["id"],UserLike.type == 0)).first()
    if(params["flag"]==0):
        if(user_like):
            question.like_number-=1
            db.session.delete(user_like)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    elif(params["flag"]==1):
        if(user_like is None):
            question.like_number+=1
            new_user_like = UserLike()
            new_user_like.userid = g.userid
            new_user_like.type = 0
            new_user_like.comment_id = params["id"]
            db.session.add(new_user_like)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    else:
        return pack.error_response(pack.COMMENT_LIKE_FAILED_PARAM)
    db.session.commit()
    return pack.ok_response()

@question_bp.route("dislike",methods=["POST"])
@token_user.login_required
def comment_dislike():
    params = request.get_json()
    question:Question = Question.query.get(params["id"])

    user_dislike:UserDislike = UserDislike.query.filter(and_(UserDislike.userid == g.userid,UserDislike.comment_id == params["id"],UserLike.type == 0)).first()
    if(params["flag"]==0):
        if(user_dislike):
            question.dislike_number-=1
            db.session.delete(user_dislike)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    elif(params["flag"]==1):
        if(user_dislike is None):
            question.dislike_number+=1
            new_user_dislike = UserDislike()
            new_user_dislike.userid = g.userid
            new_user_dislike.type = 0
            new_user_dislike.comment_id = params["id"]
            db.session.add(new_user_dislike)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    else:
        return pack.error_response(pack.COMMENT_DISLIKE_FAILED_PARAM)
    db.session.commit()
    return pack.ok_response()