# -*- coding=utf-8 -*-
__author__ = 'zou'

import base64
import json
import urllib2

from xiaoli import setting

def get_user_roles_by_project(project_id, username):
    options = dict(params=(project_id, username))
    result = basic_auth_request(setting.ROLE_BASIC_AUTH_URL, setting.ROLE_BASIC_AUTH_USERNAME, setting.ROLE_BASIC_AUTH_PASSWORD, options)
    return json.loads(result.read())

def basic_auth_request(url, username, password,  options={}):
    '''
    采用HTTP Basic Auth 方式请求 url地址
    @param url: 请求的url
    @param username: basic auth的帐号
    @param password: basic auth的密码
    @param options: 额外其他参数， 如果在url中有%s 占位符，需要在 options中提供 params参数
    '''
    try:
        if url.rfind('%s'):
            url = url % options['params']
    except KeyError as e:
        raise 'No options apply with url:%s' % url

    request = urllib2.Request(url)

    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

    request.add_header("Authorization", "Basic %s" % base64string)

    result = urllib2.urlopen(request)
    return result
