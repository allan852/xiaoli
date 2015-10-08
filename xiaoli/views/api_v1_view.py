#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from flask.ext.paginate import Pagination
from flask import Blueprint, abort, request, jsonify

from xiaoli.helpers import api_response, check_register_params, ErrorCode
from xiaoli.models import Account, Comment, Impress, ImpressContent
from xiaoli.models import Plan,PlanKeyword,PlanContent
from xiaoli.models.session import db_session_cm
from xiaoli.models import Token
from xiaoli.utils.logs.logger import api_logger
from xiaoli.utils.pagination import Page

__author__ = 'zouyingjun'

api_v1 = Blueprint("api_v1", __name__, template_folder="templates/api_v1", static_folder="../static")


@api_v1.route("/register", methods=["POST"])
def register():
    u"""注册"""
    try:
        phone = request.form.get("phone")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        security_code = request.form.get("security_code")
        params = {
            "phone": phone,
            "password": password,
            "password2": password2,
            "security_code": security_code
        }
        ok, res = check_register_params(**params)
        if not ok:
            return jsonify(res)
        with db_session_cm() as session:
            user = Account(phone, password)
            session.add(user)
            session.commit()
            res = api_response()
            res.update(response={
                "status": "ok",
                "account_id": user.id,
                "token": Token.get_token(session, user.id).code
            })
            return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/login", methods=["POST"])
def login():
    u"""登录"""
    try:
        phone = request.form.get("phone")
        password = request.form.get("password")

        res = api_response()

        with db_session_cm() as session:
            user = session.query(Account).filter(Account.cellphone == phone).first()
            if not user:
                res.update(status="fail", response={
                    "code": ErrorCode.CODE_LOGIN_PHONE_NOT_EXISTS,
                    "message": "phone not exists"
                })
                return jsonify(res)
            if not user.check_password(password):
                res.update(status="fail", response={
                    "code": ErrorCode.CODE_LOGIN_PASSWORD_INCORRECT,
                    "message": "password incorrect"
                })
                return jsonify(res)

            res = api_response()
            res.update(response={
                "status": "ok",
                "account_id": user.id,
                "token": Token.get_token(session, user.id, force_update=True).code
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/logout", methods=["POST"])
def logout():
    u"""登出
    删除用户的token
    """
    try:
        account_id = request.form.get("account_id")
        res = api_response()
        with db_session_cm() as session:
            token = session.query(Token).filter(Token.account_id == account_id).first()
            if token:
                session.delete(token)
                session.commit()
                res.update(response={"status": "ok", "account_id": account_id})
            else:
                res.update(status="fail", response={
                    "code": ErrorCode.CODE_TOKEN_NOT_EXISTS,
                    "message": "token not exists"
                })
        return jsonify(res)

    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/send_security_code", methods=["POST"])
def send_security_code():
    u"""发送短信"""
    try:
        phone = request.form.get("phone")
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>", methods=["GET"])
def account_info(account_id):
    u"""获取用户基本信息"""
    try:
        res = api_response()
        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            if account:
                res.update(response={
                    "user": account.to_dict()
                })
            else:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/impress", methods=["GET"])
def account_impress(account_id):
    u"""获取用户印象"""
    try:
        res = api_response()
        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            if not account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            impress = session.query(Account.impresses)
            print impress
            res.update(response={
                "impresses": []
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/comments", methods=["GET"])
def account_comments(account_id):
    u"""获取用户评论"""
    try:
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", Comment.PER_PAGE, int)
        res = api_response()
        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            if not account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            comments_query = session.query(Comment).join(Account.comments).filter(Account.id == account_id)
            paginate = Page(total_entries=comments_query.count(), entries_per_page=per_page, current_page=page)
            comments = comments_query.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()
            # TODO: 为实现，需要进一步却定查询和返回数据
            res.update(response={
                "page": page,
                "per_page": per_page,
                "comments": [comment.to_dict() for comment in comments]
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/friends", methods=["GET"])
def account_friends(account_id):
    u"""获取用户好友"""
    try:
        pass
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plans", methods=["GET"])
def plans():
    u"""获取礼物方案列表"""
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        search_key = request.args.get("search_key", None)
        key_word_id = request.args.get("key_word_id", None)
        with db_session_cm() as session:
            plans = session.query(Plan).join((PlanContent, Plan.contents)).join((PlanKeyword,Plan.keywords))
            if search_key:
                plans = plans.filter(Plan.title.like('%' + search_key + '%'))
            if key_word_id:
                plans = plans.filter(PlanKeyword.id == key_word_id)

        plans = plans.all()

        pagination = Pagination(page=page,per_page=per_page, total=len(plans), search=search_key, record_name='plans')
        res = api_response()
        res.update(response={
            "status": "ok",
            "plans": jsonify(pagination)
        })
        return jsonify(res)
    except Exception as e:
        print traceback.format_exc(e)
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>", methods=["GET"])
def plan_info(plan_id):
    u"""获取礼物方案详情"""
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).join((PlanContent, Plan.title)).join((PlanKeyword,Plan.keyowrds)).filter(Plan.id == plan_id ).first()
            res = api_response()
            res.update(response={
                "status": "ok",
                "plan": jsonify(plan)
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>/star", methods=["GET"])
def star_plan(plan_id):
    u"""点赞礼物方案"""
    try:
        account_id = request.args.get("account_id")
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)
            up_vote = session.query().filter(account.vote_plans.any(plan.id == plan_id )).filter(account.vote_plans.any(account.id == account_id)).first()

            if not up_vote :
                account.vote_plans.append(plan)
                session.add(account)
                session.commit()
                res = api_response()
                res.update(response={
                    "status":"ok",
                    "tips":"like success."
                })
            else:
                session.delete(up_vote)
                session.commit()
                res = api_response()
                res.update(response={
                    "status":"ok",
                    "tips":"unlike success."
                })
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>/share", methods=["GET"])
def share_plan(plan_id):
    u"""分享礼物方案"""
    try:
        account_id = request.args.get("account_id")
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)

    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>/collect", methods=["GET"])
def collect_plan(plan_id):
    u"""收藏礼物方案"""
    try:
        account_id = request.args.get("account_id")

        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)
            collect = session.query().filter(account.favorite_plans.any(plan.id == plan_id)).filter(account.favorite_plans.any(account.id == account_id)).first()
            if not collect :
                account.favorite_plans.append(plan)
                session.add(account)
                session.commit()
                res = api_response()
                res.update(response={
                    "status":"ok",
                    "tips":"collect success."
                })
            else:
                session.delete(collect)
                session.commit()
                res = api_response()
                res.update(response={
                    "status":"ok",
                    "tips":"cancel collect success."
                })
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/comment", methods=["POST"])
def add_comment(account_id):
    u"""评论用户"""
    try:
        target_account_id = request.form.get("target_account_id")
        content = request.form.get("content")

        res = api_response()
        with db_session_cm() as session:
            operator = session.query(Account).get(account_id)
            target_account = session.query(Account).get(target_account_id)
            if not operator or not target_account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)

            comment = Comment()
            comment.target = target_account
            comment.operator = operator
            comment.content = content
            session.add(comment)
            try:
                session.commit()
                res.update(response={"status": "ok"})
                return jsonify(res)
            except Exception as e:
                api_logger.error(traceback.format_exc(e))
                session.rollback()
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_SERVER_TEMPORARILY_UNUSABLE,
                    "message": "server temporarily unusable"
                })
                return jsonify(res)

    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/impress", methods=["POST"])
def add_impress(account_id):
    u"""给用户添加印象"""
    try:
        target_account_id = request.form.get("target_account_id")
        contents = request.form.getlist("content[]")

        res = api_response()
        # 检测印象格式
        if len(contents) > 4:
            res.update(status="fail",response={
                "code": ErrorCode.CODE_IMPRESS_COUNT_BEYOND_MAX_COUNT,
                "message": "impress count beyond max count"
            })
            return jsonify(res)
        for content in contents:
            if len(content) > 8:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_IMPRESS_LENGTH_BEYOND_MAX_LENGTH,
                    "message": "impress length beyond max count"
                })
                return jsonify(res)
        with db_session_cm() as session:
            operator = session.query(Account).get(account_id)
            target_account = session.query(Account).get(target_account_id)
            if not operator or not target_account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            for content in contents:
                impress = Impress()
                impress.target = target_account
                impress.operator = operator
                impress_content = ImpressContent.get_or_create(session, content)
                impress.content = impress_content
                session.add(impress)
            try:
                session.commit()
                res.update(response={"status": "ok"})
                return jsonify(res)
            except Exception as e:
                api_logger.error(traceback.format_exc(e))
                session.rollback()
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_SERVER_TEMPORARILY_UNUSABLE,
                    "message": "server temporarily unusable"
                })
                return jsonify(res)

    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/avatar", methods=["POST"])
def set_avatar(account_id):
    u"""设置头像"""
    try:
        image_file = request.args.get("image_file")
        content = request.args.get("content")
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>", methods=["PUT"])
def update_account_info(account_id):
    u"""更新用户信息"""
    try:
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        new_password2 = request.form.get("new_password2")
        sex = request.form.get("sex")
        birthday = request.form.get("birthday")
        horoscope = request.form.get("horoscope")
        allow_notice = request.form.get("allow_notice")
        allow_score = request.form.get("allow_score")
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)






