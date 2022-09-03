import random

from flask import Blueprint, request,g
from sqlalchemy import and_

from app.extensions import db
from app.api import bp
from app.api.auth import token_user, token_admin
from app.model import Comment, UserLike, UserDislike, Question
from app.utils import pack

comment_bp = Blueprint('comment', __name__)
bp.register_blueprint(comment_bp, url_prefix='/comment')

@comment_bp.route("/",methods=["POST"])
@token_user.login_required
def comment():
    params = request.get_json()
    comment = Comment()
    comment.father_id = params["question"]
    comment.question = params["question"]
    comment.comment = params["comment"]
    comment.picture = params["pictures"]
    comment.avatar = params["avatar"]
    comment.nickname = params["nickname"]
    comment.like_number = 0
    comment.dislike_number = 0
    comment.isShow = 1
    comment.userid = g.userid
    comment.type = 0
    db.session.add(comment)
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("/son",methods=["POST"])
@token_user.login_required
def comment_son():
    params = request.get_json()
    comment = Comment()
    comment.father_id = params["targetId"]
    comment.question = params["question"]
    comment.comment = params["comment"]
    comment.picture = params["pictures"]
    comment.avatar = params["avatar"]
    comment.nickname = params["nickname"]
    comment.root_comment_id = params["commentId"]
    comment.like_number = 0
    comment.dislike_number = 0
    comment.isShow = 1
    comment.userid = g.userid
    comment.type = 1
    db.session.add(comment)
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("like",methods=["POST"])
@token_user.login_required
def comment_like():
    params = request.get_json()
    comment:Comment = Comment.query.get(params["id"])

    user_like:UserLike = UserLike.query.filter(and_(UserLike.userid == g.userid,UserLike.comment_id == params["id"],UserLike.type == 1)).first()
    if(params["flag"]==0):
        if(user_like):
            comment.like_number-=1
            db.session.delete(user_like)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    elif(params["flag"]==1):
        if(user_like is None):
            comment.like_number+=1
            new_user_like = UserLike()
            new_user_like.userid = g.userid
            new_user_like.type = 1
            new_user_like.comment_id = params["id"]
            db.session.add(new_user_like)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    else:
        return pack.error_response(pack.COMMENT_LIKE_FAILED_PARAM)
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("dislike",methods=["POST"])
@token_user.login_required
def comment_dislike():
    params = request.get_json()
    comment:Comment = Comment.query.get(params["id"])

    user_dislike:UserDislike = UserDislike.query.filter(and_(UserDislike.userid == g.userid,UserDislike.comment_id == params["id"],UserLike.type == 1)).first()
    if(params["flag"]==0):
        if(user_dislike):
            comment.dislike_number-=1
            db.session.delete(user_dislike)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    elif(params["flag"]==1):
        if(user_dislike is None):
            comment.dislike_number+=1
            new_user_dislike = UserDislike()
            new_user_dislike.userid = g.userid
            new_user_dislike.type = 1
            new_user_dislike.comment_id = params["id"]
            db.session.add(new_user_dislike)
        else:
            return pack.error_response(pack.COMMENT_LIKE_FAILED_EXSIT)
    else:
        return pack.error_response(pack.COMMENT_DISLIKE_FAILED_PARAM)
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("get",methods=["GET"])
@token_user.login_required
def get_comment_page():
    order_type = int(request.args.get("type"))
    question_id = int(request.args.get("id"))
    curpage = int(request.args.get("curpage"))
    # 获取问题相关的信息
    qurestion:Question = Question.query.get(question_id)
    # 获取总评论数
    total_comment_number = Comment.query.filter(and_(Comment.question == question_id,Comment.isShow == 1)).count()
    # 获取所有的一级评论
    if(order_type==0): #按照时间降序
        comments :list[Comment] = Comment.query.filter(and_(Comment.question == question_id,Comment.isShow == 1,Comment.type==0)).order_by(
            Comment.created_at.desc()).paginate(curpage,5,error_out=False)
    else:
        comments: list[Comment] = Comment.query.filter(and_(Comment.question == question_id,Comment.isShow == 1,Comment.type==0)).order_by(
            Comment.like_number.desc()).paginate(curpage, 5,error_out=False)
    # 获取所有的次级评论
    comment_dic_list = []
    for comment in comments.items:
        main_comment_dic = comment.to_dic()
        main_comment_id = comment.id
        son_comments :list[Comment] = Comment.query.filter(and_(Comment.root_comment_id == main_comment_id,Comment.isShow == 1,Comment.type==1)).all()
        son_comments_count = len(son_comments)
        if(son_comments_count<=3):
            son_comments_three = son_comments[:son_comments_count]
        else:
            son_comments_three = son_comments[:3]
        main_comment_dic["sonCommentCount"] = son_comments_count
        for i in range(len(son_comments_three)):
            son_comments_three[i] = son_comments_three[i].to_dic()
        main_comment_dic["contains"] = son_comments_three
        comment_dic_list.append(main_comment_dic)
    res = {
        "question":qurestion.to_dic(),
        "CommentCount":total_comment_number,
        "comments":comment_dic_list
    }
    return pack.ok_response(res)
@comment_bp.route("son/get",methods=["GET"])
@token_user.login_required
def get_son_comment_page():
    main_comment_id = request.args.get("id")
    order_type = int(request.args.get("type"))
    curpage = int(request.args.get("curpage"))
    # 获取总数
    total_count = Comment.query.filter(
            and_(Comment.root_comment_id == main_comment_id, Comment.isShow == 1, Comment.type == 1)).count()
    # 获取一级评论
    comment :Comment = Comment.query.get(main_comment_id)
    main_comment_dic = {"comment":comment.to_dic()}
    if (order_type == 0):
        son_comments: list[Comment] = Comment.query.filter(
            and_(Comment.root_comment_id == main_comment_id, Comment.isShow == 1, Comment.type == 1)).order_by(
                Comment.created_at.desc()).paginate(curpage,5,error_out=False).items
    else:
        son_comments: list[Comment] = Comment.query.filter(
            and_(Comment.root_comment_id == main_comment_id, Comment.isShow == 1, Comment.type == 1)).order_by(
                Comment.like_number.desc()).paginate(curpage,5,error_out=False).items

    main_comment_dic["sonCommentCount"] = total_count
    for i in range(len(son_comments)):
        son_comments[i] = son_comments[i].to_dic()
    main_comment_dic["contains"] = son_comments
    return pack.ok_response(main_comment_dic)

@comment_bp.route("getrandom",methods=["GET"])
@token_user.login_required
def get_random_comments():
    size = request.args.get("size")
    total_question_size = Question.query.count()
    random_question_id = random.randint(1, total_question_size)
    # random_question_id = 1
    question:Question = Question.query.get(random_question_id)
    comment_list :list[Comment] = db.session.execute("select * from comment where isShow = 1 and is_special = 1 and question = {0} order by RAND() limit {1}".format(random_question_id,size))
    comments = []
    for item in comment_list:
        comments.append(Comment(item))
    for i in range(len(comments)):
        comments[i] = comments[i].to_random_dic()
    res = {
        "question":question.to_dic(),
        "contains":comments
    }
    return pack.ok_response(res)

@comment_bp.route("show/add",methods=["GET"])
@token_admin.login_required
def comment_show_add():
    id = request.args.get("id")
    comment: Comment = Comment.query.get(id)
    comment.is_special = 1
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("show/delete",methods=["GET"])
@token_admin.login_required
def comment_show_detele():
    id = request.args.get("id")
    comment: Comment = Comment.query.get(id)
    comment.is_special = 0
    db.session.commit()
    return pack.ok_response()

@comment_bp.route("delete/",methods=["GET"])
@token_admin.login_required
def comment_delete():
    id = request.args.get("id")
    comment : Comment = Comment.query.get(id)
    comment.isShow = 0
    db.session.commit()
    return pack.ok_response()