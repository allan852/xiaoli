#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import traceback
from flask import Blueprint, abort, request, jsonify
from sqlalchemy import func, or_, outerjoin
from sqlalchemy.orm import aliased, joinedload, subqueryload
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import RequestEntityTooLarge
from xiaoli.extensions.upload_set import image_resources

from xiaoli.helpers import api_response, check_register_params, ErrorCode, check_import_contacts_params, \
    check_update_account_info_params, check_renew_params,SendSms, ajax_response
from xiaoli.models import Account, Comment, Impress, ImpressContent, account_friends_rel_table,Sms, ImageResource, \
    Avatar
from xiaoli.models import Plan,PlanKeyword,PlanContent
from xiaoli.models.session import db_session_cm
from xiaoli.models import Token
from xiaoli.utils.logs.logger import api_logger
from xiaoli.utils.pagination import Page

__author__ = 'zouyingjun'

api_v1 = Blueprint("api_v1", __name__, template_folder="templates/api_v1", static_folder="../static")


@api_v1.route("/register", methods=["POST","GET"])
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
        with db_session_cm() as session:
            ok, res = check_register_params(session, **params)
            if not ok:
                return jsonify(res)
            # 看该手机号是否导入过
            user = session.query(Account).\
                filter(Account.cellphone == phone).\
                filter(Account.status == Account.STATUS_UNREGISTERED).first()
            if user:
                # 已经导入过，更新密码和状态
                user.password = password
                user.status = Account.STATUS_ACTIVE
            else:
                # 没有导入过，创建用户
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
            user = session.query(Account).\
                filter(Account.cellphone == phone).first()

            if not user or not user.has_registered:
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
    u"""发送短信验证码"""
    try:
        phone = request.form.get("phone")
        sms_code = SendSms.rand_code()
        content = "code is: %s" % sms_code
        content = content.encode('gbk','ignore')
        code = SendSms.send(phone, content)
        res = api_response()
        if 'success' in code:
            with db_session_cm() as session:
                sms = Sms(phone, sms_code)
                session.add(sms)
                session.commit()
            res.update(response={
                "status": "ok"
            })
        else:
            res.update(response={
                "status": "fail"
            })
        return jsonify(res)
    except Exception as e:
        print traceback.format_exc(e)
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/check_security_code", methods=["POST"])
def check_security_code():
    u"""短信验证码检验"""
    try:
        phone = request.form.get("phone")
        code = request.form.get("code")
        res = api_response()
        with db_session_cm() as session:
            sms = session.query(Sms).filter(Sms.phone == phone).first()
            if sms and sms.code == code:
                res.update(response={
                    "status": "ok"
                })
                session.delete(sms)
                session.commit()
            else:
                res.update(response={
                    "status": "fail"
                })
        return jsonify(res)
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


@api_v1.route("/account/<account_id>/impresses", methods=["GET"])
def account_impresses(account_id):
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
            impress_query = session.query(Impress, func.count(ImpressContent.content)).\
                join(Account.impresses, Impress.content).\
                filter(Impress.target == account).group_by(ImpressContent.content)
            impresses = impress_query.all()
            impress_dicts = []
            for impress, count in impresses:
                d = {
                    "content": impress.content.content,
                    "count": count
                }
                impress_dicts.append(d)
            res.update(response={
                "impresses": impress_dicts
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/impress_details", methods=["GET"])
def impress_details(account_id):
    u"""获取用户印象详情"""
    try:
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", Impress.PER_PAGE, int)
        res = api_response()
        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            if not account:
                res.update(status="fail", response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            impress_query = session.query(Impress, func.group_concat(ImpressContent.id)).\
                join(Account.added_impresses, Impress.content).\
                filter(Impress.target == account).group_by(Impress.operator_id).order_by(Impress.create_time.desc())

            paginate = Page(total_entries=impress_query.count(), entries_per_page=per_page, current_page=page)
            impresses = impress_query.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()
            impress_dicts = []
            for impress, content_ids in impresses:
                d = {
                    "account": impress.operator.to_dict(),
                    "contents": [c.to_dict() for c in session.query(ImpressContent).filter(ImpressContent.id.in_(content_ids.split(',')))]
                }
                impress_dicts.append(d)
            res.update(response={
                "impress_details": impress_dicts,
                "page": page,
                "per_page": per_page,
                "total": paginate.total_entries()
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/system/preset_impresses", methods=["GET"])
def preset_impresses():
    u"""获取系统预设印象"""
    try:
        res = api_response()
        with db_session_cm() as session:
            preset_impresses_query = session.query(ImpressContent).\
                filter(ImpressContent.type == ImpressContent.TYPE_PRESET)
            impresses = preset_impresses_query.all()
            impress_dicts = []
            for impress in impresses:
                impress_dicts.append(impress.to_dict())
            res.update(response={
                "impresses": impress_dicts
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/system/preset_keywords", methods=["GET"])
def preset_keywords():
    u"""获取系统预设关键字"""
    try:
        res = api_response()
        with db_session_cm() as session:
            plan_keyword_query = session.query(PlanKeyword).\
                filter(PlanKeyword.type == PlanKeyword.TYPE_PRESET)
            keywords = plan_keyword_query.all()
            keywords_dicts = []
            for keyword in keywords:
                keywords_dicts.append(keyword.to_dict())
            res.update(response={
                "impresses": keywords_dicts
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
            comments_query = session.query(Comment).join(Account.comments).filter(Comment.target == account)
            paginate = Page(total_entries=comments_query.count(), entries_per_page=per_page, current_page=page)
            comments = comments_query.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()
            res.update(response={
                "page": paginate.current_page(),
                "per_page": per_page,
                "total": paginate.total_entries(),
                "comments": [comment.to_dict() for comment in comments]
            })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/friends", methods=["GET"])
def account_friends(account_id):
    u"""获取用户好友
    :param page: optional 当前页数
    :param per_page: optional 每页显示数量
    :param only_register: optional 是否只获取已经注册的用户
    """
    try:
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", Comment.PER_PAGE, int)
        _only_register = request.args.get("only_register", 0, int)
        only_register = bool(_only_register)

        api_logger.debug(only_register)

        res = api_response()
        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            if not account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            account_alias = aliased(Account)
            friends_query = session.query(Account)
            if only_register:
                api_logger.debug("*" * 10)
                friends_query.filter(Account.status == Account.STATUS_ACTIVE)
            friends_query = friends_query.join(account_alias.friends).filter(account_alias.id == account_id)

            api_logger.debug(friends_query)
            paginate = Page(total_entries=friends_query.count(), entries_per_page=per_page, current_page=page)
            friends = friends_query.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()
            res.update(response={
                "page": paginate.current_page(),
                "per_page": per_page,
                "total": paginate.total_entries(),
                "friends": [friend.to_dict() for friend in friends]
            })
            return jsonify(res)

    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plans", methods=["GET"])
def plans():
    u"""获取礼物方案列表"""
    try:
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", Comment.PER_PAGE, int)
        search_key = request.args.get("search_key", None)
        key_word_id = request.args.get("key_word_id", None)
        res = api_response()
        with db_session_cm() as session:
            plans = session.query(Plan).\
                filter(Plan.status == Plan.STATUS_PUBLISH)
            if search_key:
                plans = plans.filter(Plan.title.like('%' + search_key + '%'))
            if key_word_id:
                plans = plans.filter(Plan.id == key_word_id)
            api_logger.debug(plans)
            paginate = Page(total_entries=plans.count(), entries_per_page=per_page, current_page=page)
            results = plans.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()

            res.update(response={
                "page": paginate.current_page(),
                "per_page": per_page,
                "total": paginate.total_entries(),
                "plans": [plan.to_dict() for plan in results]
            })

        return jsonify(res)
    except Exception as e:
        print traceback.format_exc(e)
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/recommend_plans", methods=["GET"])
def recommend_plans():
    u"""获取用户推荐礼物方案列表"""
    try:
        page = request.args.get("page", 1, int)
        per_page = request.args.get("per_page", Comment.PER_PAGE, int)
        account_id = request.args.get("account_id", None)
        res = api_response()
        with db_session_cm() as session:
            user = session.query(Account).get(account_id)
            user_impresses = [impress.content.content for impress in user.impresses if impress.content]
            match_keywords_query = session.query(PlanKeyword).filter(PlanKeyword.content.in_(user_impresses))
            match_keywords = [(kw.content) for kw in  match_keywords_query.all()]
            api_logger.debug(match_keywords)
            plans_query = session.query(Plan).filter(Plan.status == Plan.STATUS_PUBLISH).\
                join(Plan.keywords).\
                filter(PlanKeyword.content.in_(match_keywords)).\
                order_by(Plan.view_count.desc())
            api_logger.debug(user_impresses)
            api_logger.debug(plans_query)

            if not plans_query.count():
                plans_query = session.query(Plan).filter(Plan.status == Plan.STATUS_PUBLISH).\
                    order_by(Plan.view_count.desc(), Plan.publish_date.desc())

            paginate = Page(total_entries=plans_query.count(), entries_per_page=per_page, current_page=page)
            results = plans_query.offset(paginate.skipped()).limit(paginate.entries_per_page()).all()

            res.update(response={
                "page": paginate.current_page(),
                "per_page": per_page,
                "total": paginate.total_entries(),
                "plans": [plan.to_dict() for plan in results]
            })

        return jsonify(res)
    except Exception as e:
        print traceback.format_exc(e)
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<int:plan_id>", methods=["GET"])
def plan_info(plan_id):
    u"""获取礼物方案详情"""

    try:
        with db_session_cm() as session:
            plan = session.query(Plan).outerjoin(Plan.keywords).outerjoin(Plan.content).\
                filter(Plan.status == Plan.STATUS_PUBLISH).filter(Plan.id == plan_id).first()
            res = api_response()
            if not plan:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_PLAN_NOT_EXISTS,
                    "message": "plan not exists"
                })
                return jsonify(res)
            else:
                # 增加方案查看次数
                plan.view_count += 1
                session.add(plan)
                session.commit()
                res.update(response={
                    "plan": plan.to_dict(content=True)
                })
                return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<int:plan_id>/star", methods=["POST"])
def star_plan(plan_id):
    u"""点赞礼物方案"""
    try:
        account_id = request.form.get("account_id")
        res = api_response()
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)
            account_alias = aliased(Account)
            if not account:
                res.update(
                    status="fail",
                    response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            up_vote = session.query(Account).filter(account_alias.vote_plans.contains(plan)).first()

            if not up_vote :
                account.vote_plans.append(plan)
                session.add(account)
                session.commit()
                res.update(
                    status = "ok",
                    response = {
                    "message":"like success."
                })
                return jsonify(res)
            else:
                account.vote_plans.remove(plan)
                session.commit()
                res = api_response()
                res.update(
                    status="ok",
                    response={
                    "message":"unlike success."
                })
                return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>/share", methods=["POST"])
def share_plan(plan_id):
    u"""分享礼物方案
    记录分享次数
    """
    try:
        account_id = request.form.get("account_id")
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)
            plan.share_count += 1
            session.add(plan)
            session.commit()
            res = api_response()
            res.update(
                status="ok"
            )
            return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/plan/<plan_id>/collect", methods=["POST"])
def collect_plan(plan_id):
    u"""收藏礼物方案"""
    try:
        account_id = request.form.get("account_id")
        res = api_response()
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            account = session.query(Account).get(account_id)
            account_alias = aliased(Account)
            if not account:
                res.update(
                    status="fail",
                    response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            collect = session.query(Account).filter(account_alias.favorite_plans.contains(plan)).first()
            if not collect :
                account.favorite_plans.append(plan)
                session.add(account)
                session.commit()
                res.update(
                    status="ok",
                    response={
                    "message":"collect success."
                })
                return jsonify(res)
            else:
                account.favorite_plans.remove(plan)
                session.commit()
                res = api_response()
                res.update(
                    status="ok",
                    response={
                    "message":"cancel collect success."
                })
                return jsonify(res)
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
    res = ajax_response()
    try:
        with db_session_cm() as session:
            account = session.query(Account).filter(Account.id == account_id).first()

            if not account:
                res.update(status="fail",response={
                    "code": ErrorCode.CODE_ACCOUNT_NOT_EXISTS,
                    "message": "user not exists"
                })
                return jsonify(res)
            image_file = request.files.get("image_file")
            filename = image_resources.save(image_file, folder=str(account_id))
            avatar = account.avatar or Avatar(account_id)
            avatar.path = filename
            name, suffix = os.path.splitext(image_file.filename)
            avatar.format = suffix
            session.add(avatar)
            session.commit()
            res.update(response={
                "account": {
                    "id": account.id,
                    "avatar_url": account.avatar.url
                }
            })
            return jsonify(res)
    except RequestEntityTooLarge as e:
        api_logger.error(traceback.format_exc(e))
        res.update(status="fail",response={
            "code": ErrorCode.CODE_UPLOAD_IMAGE_OVER_SIZE,
            "message": "image content over size"
        })
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>", methods=["PUT"])
def update_account_info(account_id):
    u"""更新用户信息
    参数格式：
    {
        "current_password": current_password,
        "new_password": new_password,
        "new_password2": new_password2,
        "sex": sex,
        "birthday": birthday,
        "nickname": nickname,
        "horoscope": horoscope,
        "allow_notice": allow_notice,
        "allow_score": allow_score
    }
    """
    try:
        params = request.form.to_dict()

        with db_session_cm() as session:
            account = session.query(Account).get(account_id)
            ok, res = check_update_account_info_params(account, **params)
            if not ok:
                return jsonify(res)
            account.update_info(**params)
            session.add(account)
            session.commit()
            res.update(response={"status": "ok"})
            return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/<account_id>/import_friends", methods=["POST"])
def import_friends(account_id):
    u"""导入好友"""
    try:
        kwargs = request.json
        ok, res = check_import_contacts_params(**kwargs)
        if not ok:
            return jsonify(res)
        contacts = kwargs.get("contacts")
        res = api_response()
        with db_session_cm() as session:
            Account.import_friends(session, account_id, contacts)
            session.commit()
            res.update(response={"status": "ok"})
        return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)


@api_v1.route("/account/renew_password", methods=["POST"])
def renew_password():
    u"""重新设置密码"""
    try:
        phone = request.form.get("phone")
        code = request.form.get("code")
        new_password = request.form.get("new_password")
        new_password2 = request.form.get("new_password2")
        res = api_response()
        params = {
            "phone": phone,
            "code": code,
            "new_password": new_password,
            "new_password2": new_password2
        }
        with db_session_cm() as session:
            ok, res = check_renew_params(session, **params)
            if not ok:
                 return jsonify(res)
            sms = session.query(Sms).filter(Sms.phone == phone).first()
            if sms and sms.code == code:
                res.update(response={
                    "status": "ok"
                })
                session.delete(sms)
                session.commit()
            else:
                res.update(response={
                    "status": "ok"
                })
                return jsonify(res)

            account = session.query(Account).filter(Account.cellphone == phone).first()
            account.password = new_password
            session.add(account)
            session.commit()
            res.update(response={"status": "ok"})
            return jsonify(res)
    except Exception as e:
        api_logger.error(traceback.format_exc(e))
        abort(400)




