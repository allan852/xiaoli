#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import uuid

from flask import Blueprint, render_template, send_file, request, url_for, redirect, abort, current_app, flash
from flask.ext.babel import gettext as _
from flask.ext.login import current_user, login_user, logout_user, login_required
from flask.ext.principal import identity_changed, Identity
from flask.ext.uploads import UploadNotAllowed

from xiaoli.forms import LoginForm, RegisterForm
from xiaoli.models import Account, ImageResource
from xiaoli.models.session import db_session_cm
from xiaoli.extensions.upload_set import image_resources
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
    try:
        register_form = RegisterForm(request.form)
        context = {
            'form': register_form,
        }
        if request.method == 'POST' and register_form.validate_on_submit():
            phone = register_form.phone.data.strip().lower()
            password = register_form.password.data.strip()
            with db_session_cm() as session:
                user = Account(phone, password)
                user.nickname = register_form.nickname.data.strip()
                session.add(user)
                session.commit()
            flash(_(u"恭喜您，注册成功！ 赶快登录吧！"))
            return redirect(url_for('frontend.login'))
    except Exception, e:
        common_logger.error(traceback.format_exc(e))
        abort(500)

    return render_template('frontend/register.html', **context)


@frontend.route('/login', methods=["GET", "POST"])
def login():
    u"""登陆
    登录成功后，管理员直接到管理后台首页，其他到前台首页
    """
    try:
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


@frontend.route('/upload_images', methods=['GET', 'POST'])
@login_required
def upload_images():
    try:
        if request.method == 'POST' and 'image' in request.files:
            with db_session_cm() as session:
                request_file = request.files['image']
                filename = image_resources.save(request_file, folder=str(current_user.id))
                irs = ImageResource(filename, current_user.id)
                irs.format = request_file.mimetype
                session.add(irs)
                session.commit()
                flash("图片上传成功", category="success")
                return redirect(url_for('frontend.image', id=irs.id))
        return render_template('frontend/upload.html')
    except UploadNotAllowed as e:
        flash(u"文件格式不支持", category="warning")
        return render_template('frontend/upload.html')
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        abort(500)


@frontend.route('/images/<id>')
def image(id):
    with db_session_cm() as session:
        image = session.query(ImageResource).get(id)
        if image is None:
            abort(404)
        url = image_resources.url(image.path)
        return render_template('frontend/show_images.html', url=url, image=image)


@frontend.route('/favicon.ico')
def favicon():
    return send_file("static/favicon.ico")
