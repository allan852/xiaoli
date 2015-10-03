#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, abort, request
from xiaoli.helpers import api_response, check_register_params, ErrorCode
from xiaoli.models import db_session_cm
from xiaoli.models.account import Account
from xiaoli.models.token import Token

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
        ok, res = check_register_params(**{
            "phone": phone,
            "password": password,
            "password2": password2,
            "security_code": security_code
        })
        if not ok:
            return res
        user = Account.create(phone, password)
        res = api_response()
        res.update(response={
            "status": "ok",
            "account_id": user.id,
            "token": Token.get_token(user.id).code
        })
    except Exception as e:
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
                res.update(status = "fail", response={
                    "code": ErrorCode.CODE_LOGIN_PHONE_NOT_EXISTS,
                    "message": "phone not exists"
                })
                return res
            if not user.check_password(password):
                res.update(status = "fail", response={
                    "code": ErrorCode.CODE_LOGIN_PASSWORD_INCORRECT,
                    "message": "password incorrect"
                })
                return res

            res = api_response()
            res.update(response={
                "status": "ok",
                "account_id": user.id,
                "token": Token.get_token(user.id, force_update=True).code
            })
    except Exception as e:
        abort(400)


@api_v1.route("/logout", methods=["POST"])
def logout():
    u"""登出"""
    try:
        account_id = request.form.get("account_id")
    except Exception as e:
        abort(400)


@api_v1.route("/send_security_code", methods=["POST"])
def send_security_code():
    u"""发送短信"""
    try:
        phone = request.form.get("phone")
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>", methods=["GET"])
def account_info(account_id):
    u"""获取用户基本信息"""
    try:
        pass
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>/impress", methods=["GET"])
def account_impress(account_id):
    u"""获取用户印象"""
    try:
        pass
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>/comments", methods=["GET"])
def account_comments(account_id):
    u"""获取用户评论"""
    try:
        pass
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>/friends", methods=["GET"])
def account_friends(account_id):
    u"""获取用户好友"""
    try:
        pass
    except Exception as e:
        abort(400)


@api_v1.route("/plans", methods=["GET"])
def plans():
    u"""获取礼物方案列表"""
    try:
        page = request.args.get("page", 1)
        per_page = request.args.get("per_page", 10)
        search_key = request.args.get("search_key", None)
        key_word_id = request.args.get("key_word_id", None)
    except Exception as e:
        abort(400)


@api_v1.route("/plan/<plan_id>", methods=["GET"])
def plan_info(plan_id):
    u"""获取礼物方案详情"""
    try:
        pass
    except Exception as e:
        abort(400)


@api_v1.route("/plan/<plan_id>/star", methods=["GET"])
def star_plan(plan_id):
    u"""点赞礼物方案"""
    try:
        account_id = request.args.get("account_id")
    except Exception as e:
        abort(400)


@api_v1.route("/plan/<plan_id>/share", methods=["GET"])
def share_plan(plan_id):
    u"""分享礼物方案"""
    try:
        account_id = request.args.get("account_id")
    except Exception as e:
        abort(400)


@api_v1.route("/plan/<plan_id>/collect", methods=["GET"])
def collect_plan(plan_id):
    u"""收藏礼物方案"""
    try:
        account_id = request.args.get("account_id")
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>/comment", methods=["GET"])
def comment(account_id):
    u"""评论用户"""
    try:
        target_account_id = request.args.get("target_account_id")
        content = request.args.get("content")
    except Exception as e:
        abort(400)


@api_v1.route("/account/<account_id>/avatar", methods=["POST"])
def set_avatar(account_id):
    u"""设置头像"""
    try:
        image_file = request.args.get("image_file")
        content = request.args.get("content")
    except Exception as e:
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
        abort(400)






