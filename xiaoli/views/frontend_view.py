#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import datetime
from flask import Blueprint, render_template, send_file, request, url_for, redirect, abort, current_app
from flask.ext.login import current_user, login_user, logout_user, login_required
from flask.ext.principal import identity_changed, Identity
from xiaoli.forms import LoginForm
from xiaoli.helpers import validate_user
from xiaoli.models import Account
from xiaoli.models.session import db_session_cm
from xiaoli.utils.logs.logger import common_logger

__author__ = 'zouyingjun'

frontend = Blueprint("frontend", __name__, template_folder="templates", static_folder="../static")


@frontend.route('/')
def index():
    u"""首页"""
    return render_template("frontend/index.html")


@frontend.route('/register', methods=["GET", "POST"])
def register():
    u"""注册"""
    pass


@frontend.route('/login', methods=["GET", "POST"])
def login():
    u"""登陆
    登录成功后，管理员直接到管理后台首页，其他到前台首页
    """
    try:
        common_logger.info("login" * 20)
        current_app.logger.debug("ssss" * 20)
        login_form = LoginForm(request.form)
        next = request.args.get('next')
        context = {
            'form': login_form,
            'next': next,
        }

        def __return_index():
            if current_user.is_admin:
                return redirect(url_for("admin_frontend.index"))
            return redirect(url_for("frontend.index"))

        if current_user and current_user.is_authenticated:
            return __return_index()

        if request.method == 'POST':
            if login_form.validate_on_submit():
                with db_session_cm() as session:
                    user = session.query(Account).filter(Account.cellphone == login_form.phone.data.strip()).one()
                    if user.is_active:
                        login_user(user)
                        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                        return next and redirect(next) or __return_index()
                    else:
                        return redirect(url_for('frontend.wait_to_active', phone=login_form.phone.data.strip()))
        return render_template('frontend/login.html', **context)
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        abort(500)


@frontend.route('/logout')
@login_required
def logout():
    u"""登出"""
    logout_user()

    return redirect(url_for("frontend.index"))


@frontend.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    u"""忘记密码"""
    pass


@frontend.route('/wait_to_active')
def wait_to_active():
    u"""等待激活"""
    pass


@frontend.route('/favicon.ico')
def favicon():
    return send_file("static/favicon.ico")