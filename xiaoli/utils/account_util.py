# -*- coding:utf-8 -*-
# author: zouyingjun
# date: 2015/10/19 13:44
from functools import wraps
from flask import current_app
from flask.ext.login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        return current_app.login_manager.unauthorized()
    return decorated_view

if __name__ == '__main__':
    pass