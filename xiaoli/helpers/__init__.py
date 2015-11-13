#! -*- coding=utf-8 -*-
import datetime

from flask import request, url_for, current_app, redirect
from flask.ext.login import login_user
from flask.ext.principal import identity_changed, Identity
from xiaoli.helpers.error_code import ErrorCode
from xiaoli.helpers.send_sms import SendSms
from xiaoli.models.account import Account
from xiaoli.models.session import db_session_cm


def url_for_other_page(page):
    args = request.view_args.copy()
    args.update(request.args.to_dict().copy())
    args['page'] = page
    return url_for(request.endpoint, **args)


def api_response(response=None):
    res = {
        'status': 'ok',   # 返回类型 取 ok fail reload redirect
        'response': response       # 返回数据
    }
    return res

def api_fail(response=None):
    return { 'status': 'fail', 'response': response }

def ajax_response():
    res = {
        'response': 'ok',   # 返回类型 取 ok fail reload redirect
        'data': {},       # 返回数据
        'status': 'ok',
        'message': '',
        'category': 'success'
    }
    return res


def check_register_params(session, **kwargs):
    u"""检测注册参数"""
    res = api_response()
    phone = kwargs.get("phone")
    password = kwargs.get("password")
    password2 = kwargs.get("password2")
    security_code = kwargs.get("security_code")
    nickname = kwargs.get("nickname")

    # 手机号是否重复
    if phone:
        account = session.query(Account).filter(Account.cellphone == phone).first()
        if account and account.has_registered:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_REGISTER_PHONE_EXISTS,
                "message": "phone exists"
            })
            return False, res
    
    # 用户昵称是否重复
    if nickname:
        account = session.query(Account).filter_by(nickname=nickname).first()
        if account:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_NICKNAME_EXISTS,
                "message": "nickname param exists error"
            })
            return False, res

    # 密码是否一致
    if not(password and password2 and password == password2):
        res.update(status="fail", response={
            "code": ErrorCode.CODE_REGISTER_PASSWORD_NOT_EQUAL,
            "message": "password not equal"
        })
        return False, res
    return True, res


def check_import_contacts_params(**kwargs):
    u"""检测导入联系人参数"""
    res = api_response()
    contacts = kwargs.get("contacts")

    format_error = False
    # 不是数组
    if not isinstance(contacts, list):
        format_error = True

    for contact in contacts:
        # contact 必须是dict 类型
        if not isinstance(contact, dict):
            format_error = True
            break
        # contact 必须 包含 phone 和 name 字段
        if not(contact.has_key("phone") or contact.has_key("name")):
            format_error = True
            break

    if format_error:
        res.update(status="fail", response={
            "code": ErrorCode.CODE_IMPORT_FRIENDS_PARAMS_FORMAT_ERROR,
            "message": "import friends params format error"
        })
        return False, res
    return True, res


def check_update_account_info_params(account, **kwargs):
    u"""检测更新用户信息参数
    检查规则：
    1. 有current_password 时， 必须有有 new_password和new_password2 字段，同时两者要相等。
    2. 剩下的其他字段出现那个更新那个值
    """
    current_password = kwargs.get("current_password")
    new_password = kwargs.get("new_password")
    new_password2 = kwargs.get("new_password2")
    sex = kwargs.get("sex")
    birthday = kwargs.get("birthday")
    nickname = kwargs.get("nickname")
    horoscope = kwargs.get("horoscope")

    res = api_response()

    if current_password:
        if not account.check_password(current_password):
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_INCORRECT_PASSWORD,
                "message": "password incorrect"
            })
            return False, res

        if not (new_password or new_password2):
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_NO_PASSWORD,
                "message": "no new password"
            })
            return False, res

        if new_password != new_password2:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_PASSWORD_NOT_EQUAL,
                "message": "new password not equal"
            })
            return False, res

        if new_password == current_password:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_USE_OLD_PASSWORD,
                "message": "old password equal new password"
            })
            return False, res

    if sex and sex not in [sex_type for sex_type, display_name in Account.SEX_CHOICES]:
        res.update(status="fail", response={
            "code": ErrorCode.CODE_UPDATE_INFO_PARAMS_VALUE_ERROR,
            "message": "sex param value error"
        })
        return False, res

    if birthday:
        try:
            datetime.datetime.strptime(birthday, Account.BIRTHDAY_FORMAT)
        except ValueError as e:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_UPDATE_INFO_PARAMS_VALUE_ERROR,
                "message": "birthday param format error"
            })
            return False, res

    if nickname:
        with db_session_cm() as session:
            account = session.query(Account).filter_by(nickname=nickname).first()
            if account:
                res.update(status="fail", response={
                    "code": ErrorCode.CODE_UPDATE_INFO_NICKNAME_EXISTS,
                    "message": "nickname param exists error"
                })
                return False, res

    if horoscope and horoscope not in [horoscope for horoscope, display_name in Account.HOROSCOPE_CHOICES]:
        res.update(status="fail", response={
            "code": ErrorCode.CODE_UPDATE_INFO_PARAMS_VALUE_ERROR,
            "message": "horoscope param value error"
        })
        return False, res
    return True, res


def check_renew_params(session, **kwargs):
    u"""检测重新设置密码"""
    new_password = kwargs.get("new_password")
    new_password2 = kwargs.get("new_password2")
    phone = kwargs.get("phone")
    code = kwargs.get("code")

    res = api_response()

    if not (new_password or new_password2):
        res.update(status="fail", response={
            "code": ErrorCode.CODE_UPDATE_INFO_NO_PASSWORD,
            "message": "no new password"
        })
        return False, res

    if new_password != new_password2:
        res.update(status="fail", response={
            "code": ErrorCode.CODE_UPDATE_INFO_PASSWORD_NOT_EQUAL,
            "message": "new password not equal"
        })
        return False, res

    # 手机号是否重复
    if phone:
        account = session.query(Account).filter(Account.cellphone == phone).first()
        if not account or account.status == Account.STATUS_UNREGISTERED:
            res.update(status="fail", response={
                "code": ErrorCode.CODE_LOGIN_PHONE_NOT_EXISTS,
                "message": "phone not exists"
            })
            return False, res

    # 检测验证码是否正确

    return True, res


def validate_user(phone, name, next_url=None):

    user = Account.m.find({'email': email, 'name': name}).first()
    if not user:
        user = Account.m.find({'email': email}).first()

    if user.active:
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user._id))
        user.login_time = datetime.datetime.now()
        user.m.save()

        if next_url:
            return redirect(next_url)
        else:
            return redirect(url_for('frontend.index'))
    else:
        user.send_register_mail(host_url=request.host_url, next=next_url)
    return redirect(url_for('frontend.sign_success', email=user.email))
