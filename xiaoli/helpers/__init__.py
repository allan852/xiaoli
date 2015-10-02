#! -*- coding=utf-8 -*-

from flask import request, url_for


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