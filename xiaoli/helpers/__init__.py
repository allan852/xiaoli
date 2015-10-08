#! -*- coding=utf-8 -*-

from flask import request, url_for
from xiaoli.helpers.error_code import ErrorCode
from xiaoli.models.account import Account


def url_for_other_page(page):
    args = request.view_args.copy()
    args.update(request.args.to_dict().copy())
    args['page'] = page
    return url_for(request.endpoint, **args)


def api_response():
    res = {
        'status': 'ok',   # 返回类型 取 ok fail reload redirect
        'response': None       # 返回数据
    }
    return res


def ajax_response():
    res = {
        'response': 'ok',   # 返回类型 取 ok fail reload redirect
        'data': {},       # 返回数据
        'status': 'ok',
        'message': '',
        'category': 'success'
    }
    return res


def check_register_params(**kwargs):
    res = api_response()
    phone = kwargs.get("phone")
    password = kwargs.get("password")
    password2 = kwargs.get("password2")
    security_code = kwargs.get("security_code")

    # 手机号是否重复
    if phone and Account.exists_phone(phone):
        res.update(status="fail", response={
            "code": ErrorCode.CODE_REGISTER_PHONE_EXISTS,
            "message": "phone exists"
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
