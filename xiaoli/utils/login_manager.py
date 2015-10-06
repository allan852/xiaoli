# -*- coding=utf-8 -*-

from flask.ext.babel import gettext as _
from flask import request, abort, redirect
from flask.ext.login import LoginManager, login_url, AnonymousUserMixin

from xiaoli.models.account import Account
from xiaoli.models.session import db_session_cm

_login_manager = LoginManager()
_login_manager.login_view = 'frontend.login'
_login_manager.login_message = _(u'请登录')


def init_app(app):
    _login_manager.init_app(app)


@_login_manager.user_loader
def user_loader(user_id):
    user = AnonymousUserMixin()
    if user_id:
        with db_session_cm() as session:
            user = session.query(Account).get(user_id)
    return user


@_login_manager.unauthorized_handler
def unauthorized():
    if request.is_xhr or not _login_manager.login_view:
        abort(401)

    return redirect(login_url(_login_manager.login_view, request.url))