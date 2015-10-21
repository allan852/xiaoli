#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import json

from flask import Blueprint, render_template, redirect, url_for, request,make_response
from flask.ext.babel import gettext as _
from flask.ext.paginate import Pagination
from xiaoli.models import Account, Plan,Uploader, PlanKeyword
from xiaoli.models.session import db_session_cm
from xiaoli.config import setting


__author__ = 'zouyingjun'

admin_frontend = Blueprint("admin_frontend", __name__, template_folder="templates", static_folder="../static")


@admin_frontend.route('/')
def index():
    u"""管理员首页"""
    return redirect(url_for("admin_frontend.accounts"))


@admin_frontend.route('/accounts')
def accounts():
    u"""用户列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", Account.PER_PAGE, type=int)
    with db_session_cm() as session:
        users_query = session.query(Account)
        pagination = Pagination(page=page, total=users_query.count(), record_name=_(u"用户"), bs_version=3)
        users = users_query.order_by(Account.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "users": users,
            "pagination": pagination
        }
        return render_template("admin/account/index.html", **context)


@admin_frontend.route('/account/<int:account_id>')
def account_show(account_id):
    u"""查看用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/edit/<int:account_id>', methods=["GET", "POST"])
def account_edit(account_id):
    u"""修改用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/delete/<int:account_id>')
def account_delete(account_id):
    u"""删除用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/active/<int:account_id>')
def account_active(account_id):
    u"""激活用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/freeze/<int:account_id>')
def account_freeze(account_id):
    u"""冻结用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/plans')
def plans():
    u"""方案列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", Account.PER_PAGE, type=int)
    with db_session_cm() as session:
        plans_query = session.query(Plan)
        pagination = Pagination(page=page, total=plans_query.count(), record_name=_(u"方案"), bs_version=3)
        plans = plans_query.offset((page - 1) * per_page).limit(per_page)
        context = {
            "plans": plans,
            "pagination": pagination
        }
        return render_template("admin/plan/index.html", **context)


@admin_frontend.route('/plan/<int:plan_id>')
def plan_show(plan_id):
    u"""查看方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/plan/edit/<int:plan_id>', methods=["GET", "POST"])
def plan_edit(plan_id):
    u"""修改方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/plan/delete/<int:plan_id>')
def plan_delete(plan_id):
    u"""删除方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/plan/new')
def plan_new():
    u"""新建方案"""
    return render_template("admin/plan/new.html")


@admin_frontend.route('/upload/',methods=['GET', 'POST','OPTIONS'])
def upload():
    u"""UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')
    # 解析JSON格式的配置文件

    CONFIG = setting.EDITOR_CONFIG
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG
    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, 'public/static')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']
        if fieldName in request.form:
            source = []
        elif '%s[]' % fieldName in request.form:
            source = request.form.getlist('%s[]' % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })
        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list
    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res


@admin_frontend.route('/plan/publish/<int:plan_id>')
def plan_publish(plan_id):
    u"""发布方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/plan/revocation/<int:plan_id>')
def plan_revocation(plan_id):
    u"""撤销方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/keywords')
def keywords():
    u"""关键字"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", PlanKeyword.PER_PAGE, type=int)
    with db_session_cm() as session:
        keywords_query = session.query(PlanKeyword)
        pagination = Pagination(page=page, total=keywords_query.count(), record_name=_(u"关键字"), bs_version=3)
        keywords = keywords_query.order_by(PlanKeyword.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "keywords": keywords,
            "pagination": pagination
        }
        return render_template("admin/keyword/index.html", **context)


@admin_frontend.route('/keyword/new', methods=["GET", "POST"])
def keyword_new():
    u"""新建关键字"""
    return render_template("admin/keyword/new.html")


@admin_frontend.route('/keyword/<int:keyword_id>')
def keyword_show(keyword_id):
    u"""关键之详情"""
    return render_template("admin/keyword/show.html")


@admin_frontend.route('/keyword/<int:keyword_id>')
def keyword_delete(keyword_id):
    u"""删除关键字"""
    return render_template("admin/keyword/index.html")