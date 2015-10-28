#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import traceback
from flask import Blueprint, render_template, redirect, url_for, request,make_response,abort,current_app,flash
from flask.ext.babel import gettext as _
from flask.ext.paginate import Pagination
from flask_login import current_user
from sqlalchemy.orm import subqueryload, aliased
from xiaoli.extensions.upload_set import image_resources
from xiaoli.models import Account, Plan, PlanContent, PlanKeyword, ImageResource, Impress, ImpressContent
from xiaoli.models.session import db_session_cm
from xiaoli.config import setting
from xiaoli.utils.account_util import admin_required
from xiaoli.utils.logs.logger import common_logger
from xiaoli.forms import PlanForm, PlanKeywordsForm, PresetImpressForm

__author__ = 'zouyingjun'

admin_frontend = Blueprint("admin_frontend", __name__, template_folder="templates", static_folder="../static")


@admin_frontend.route('/')
@admin_required
def index():
    u"""管理员首页"""
    return redirect(url_for("admin_frontend.accounts"))


@admin_frontend.route('/accounts')
@admin_required
def accounts():
    u"""用户列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", Account.PER_PAGE, type=int)
    with db_session_cm() as session:
        users_query = session.query(Account)
        pagination = Pagination(page=page, total=users_query.count(), record_name=_(u"用户"), bs_version=3)
        users = users_query.order_by(Account.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "users": users.all(),
            "pagination": pagination
        }
        return render_template("admin/account/index.html", **context)


@admin_frontend.route('/account/<int:account_id>')
@admin_required
def account_show(account_id):
    u"""查看用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/edit/<int:account_id>', methods=["GET", "POST"])
@admin_required
def account_edit(account_id):
    u"""修改用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/delete/<int:account_id>')
@admin_required
def account_delete(account_id):
    u"""删除用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/active/<int:account_id>')
@admin_required
def account_active(account_id):
    u"""激活用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/account/freeze/<int:account_id>')
@admin_required
def account_freeze(account_id):
    u"""冻结用户"""
    return render_template("admin/account/index.html")


@admin_frontend.route('/plans')
@admin_required
def plans():
    u"""方案列表"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", Account.PER_PAGE, type=int)
    with db_session_cm() as session:
        plans_query = session.query(Plan)
        pagination = Pagination(page=page, total=plans_query.count(), record_name=_(u"方案"), bs_version=3)
        plans = plans_query.order_by(Plan.create_time.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "plans": plans.all(),
            "pagination": pagination
        }
        return render_template("admin/plan/index.html", **context)


@admin_frontend.route('/plan/<int:plan_id>')
@admin_required
def plan_show(plan_id):
    u"""查看方案"""
    with db_session_cm() as session:
        plan_alias =aliased(Plan)
        plan = session.query(Plan).options(subqueryload(Plan.content)).join(plan_alias.keywords).filter(Plan.id == plan_id).first()
    return render_template("admin/plan/show.html", plan=plan)


@admin_frontend.route('/plan/new',methods=["GET","POST"])
@admin_required
def plan_new():
    u"""新建方案"""
    try:
        plan_form = PlanForm(request.form)
        plan_form.keywords.choices = PlanKeyword.choices()
        context = {
            'form': plan_form,
        }
        if request.method == 'POST' and plan_form.validate_on_submit():
            title = plan_form.title.data.strip()
            content = plan_form.content.data.strip()
            keywords = plan_form.keywords.data
            with db_session_cm() as session:
                plan = Plan(title)
                plan_content = PlanContent(content=content)
                plan.content = plan_content
                u"""upload image """
                request_file = request.files['image']

                if request_file:
                    filename = image_resources.save(request_file, folder=str(current_user.id))
                    irs = ImageResource(filename, current_user.id)
                    irs.format = request_file.mimetype
                    session.add(irs)
                    session.commit()
                    plan.cover_image_id = irs.id

                if current_user and current_user.is_authenticated:
                    plan.author_id = current_user.get_id()
                if keywords:
                    keywords = session.query(PlanKeyword).filter(PlanKeyword.id.in_(keywords)).all()
                    plan.keywords = keywords
                session.add(plan)
                session.commit()
            flash(_(u"方案添加成功!"), category="success")
            return redirect(url_for('admin_frontend.plans'))
        return render_template("admin/plan/new.html", **context)
    except Exception, e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        abort(500)


@admin_frontend.route('/plan/edit/<int:plan_id>', methods=["GET", "POST"])
@admin_required
def plan_edit(plan_id):
    u"""修改方案"""
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).options(subqueryload(Plan.content)).get(plan_id)
            plan_form = PlanForm(
                title=plan.title,
                content=plan.content and plan.content.content or "",
                keywords=[kw.id for kw in plan.keywords]
            )
            plan_form.keywords.choices = PlanKeyword.choices()
            context = {
                'form': plan_form,
                'plan': plan
            }
        return render_template("admin/plan/edit.html", **context)
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        abort(500)


@admin_frontend.route('/plan/plan_update/<int:plan_id>',methods=["POST"])
@admin_required
def plan_update(plan_id):
    u"""更新方案"""
    try:
        plan_form = PlanForm(request.form)
        plan_form.keywords.choices = PlanKeyword.choices()

        if request.method == 'POST' and plan_form.validate_on_submit():
            with db_session_cm() as session:
                title = plan_form.title.data.strip()
                content = plan_form.content.data.strip()
                keywords = plan_form.keywords.data
                request_file = request.files['image']

                plan_alias = aliased(Plan)
                plan = session.query(Plan).options(subqueryload(Plan.content)).\
                    join(plan_alias.keywords).filter(Plan.id == plan_id).first()
                plan_content = PlanContent(content=content)
                plan.content = plan_content
                plan.title = title
                if current_user and current_user.is_authenticated:
                    plan.author_id = current_user.get_id()
                if request_file:
                    filename = image_resources.save(request_file, folder=str(current_user.id))
                    irs = ImageResource(filename, current_user.id)
                    irs.format = request_file.mimetype
                    session.add(irs)
                    session.commit()
                    session.query(Plan).filter_by(plan_alias.id == plan_id).update({"cover_image_id": irs.id })

                if keywords:
                    keywords = session.query(PlanKeyword).filter(PlanKeyword.id.in_(keywords)).all()
                    plan.keywords = keywords
                session.merge(plan)
                session.commit()
                flash(_(u"方案编辑成功!"), category="success")
                return redirect(url_for('admin_frontend.plan_show', plan_id=plan.id))
    except Exception, e:
        common_logger.error(traceback.format_exc(e))
        return redirect(url_for('admin_frontend.plan_show', plan_id=plan_id))


@admin_frontend.route('/plan/delete/<int:plan_id>', methods=["GET", "POST"])
@admin_required
def plan_delete(plan_id):
    u"""删除方案"""
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            if current_user and current_user.is_authenticated:
                session.delete(plan)
                session.commit()
                flash(_(u"删除成功!"))
            else:
                flash(_(u"没有权限!"))
        return redirect(url_for('admin_frontend.plans'))
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        flash(_(u"删除失败!"))
        return redirect(url_for('admin_frontend.plans'))


@admin_frontend.route('/upload',methods=['GET', 'POST', 'OPTIONS'])
@admin_required
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
    elif action in ('uploadimage', 'uploadfile', 'uploadvideo',):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
        else:
            fieldName = CONFIG.get('fileFieldName')
        if fieldName in request.files:
            try:
                field = request.files[fieldName]
                with db_session_cm() as session:
                    filename = image_resources.save(field, folder=str(current_user.id))
                    irs = ImageResource(filename, current_user.id)
                    irs.format = field.mimetype
                    session.add(irs)
                    session.commit()
                    image = session.query(ImageResource).get(irs.id)
                    if image is None:
                        result['state'] = 'SUCCESS'
                        result['url'] = ''
                    else:
                        url = image_resources.url(image.path)
                        result['state'] = 'SUCCESS'
                        result['url'] = url
                        result['title'] = filename
                        result = json.dumps(result)
                        res = make_response(result)
                        return res
            except Exception, e:
                common_logger.error(traceback.format_exc(e))
                print traceback.format_exc(e)
            else:
                result['state'] = '上传接口出错'

    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res


@admin_frontend.route('/plan/publish/<int:plan_id>')
@admin_required
def plan_publish(plan_id):
    u"""发布方案"""
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            if current_user and current_user.is_authenticated:
                plan.publish()
                session.merge(plan)
                session.commit()
                flash(_(u"发布成功!"), category="info")
            else:
                flash(_(u"没有权限!"), category="warning")
            return redirect(url_for('admin_frontend.plans'))
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        flash(_(u"失败!"), category="danger")
    return redirect(url_for('admin_frontend.plans'))


@admin_frontend.route('/plan/revocation/<int:plan_id>')
@admin_required
def plan_revocation(plan_id):
    u"""撤销方案"""
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).get(plan_id)
            if current_user and current_user.is_authenticated:
                plan.status = Plan.STATUS_UNPUBLISHED
                session.merge(plan)
                session.commit()
                flash(_(u"撤销成功!"))
            else:
                flash(_(u"没有权限!"))
                return redirect(url_for('admin_frontend.plans'))
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
    flash(_(u"失败!"))
    return redirect(url_for('admin_frontend.plans'))


@admin_frontend.route('/keywords')
@admin_required
def keywords():
    u"""关键字"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", PlanKeyword.PER_PAGE, type=int)
    with db_session_cm() as session:
        keywords_query = session.query(PlanKeyword)
        pagination = Pagination(page=page, total=keywords_query.count(), record_name=_(u"关键字"), bs_version=3)
        keywords = keywords_query.order_by(PlanKeyword.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "keywords": keywords.all(),
            "pagination": pagination
        }
        return render_template("admin/keyword/index.html", **context)


@admin_frontend.route('/keyword/new', methods=["GET", "POST"])
@admin_required
def keyword_new():
    u"""新建关键字"""
    try:
        plan_form = PlanKeywordsForm(request.form)
        context = {
            'form': plan_form,
        }
        if request.method == 'POST' and plan_form.validate_on_submit():
            content = plan_form.content.data.strip()
            with db_session_cm() as session:
                plan_keyword = PlanKeyword(content=content)
                plan_keyword.type = PlanKeyword.TYPE_PRESET
                session.add(plan_keyword)
                session.commit()
            flash(_(u"添加成功!"), category="success")
            return redirect(url_for('admin_frontend.keywords'))
        return render_template("admin/keyword/new.html", **context)
    except Exception, e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        abort(500)


@admin_frontend.route('/keyword/edit/<int:keyword_id>',methods=["GET"])
@admin_required
def keyword_edit(keyword_id):
    u"""关键之详情"""
    try:
        with db_session_cm() as session:
            keyword = session.query(PlanKeyword).filter(PlanKeyword.id == keyword_id).first()
            plan_form = PlanKeywordsForm(id=keyword.id,content = keyword.content)
            context = {
                'form': plan_form
            }
        return render_template("admin/keyword/edit.html",**context)
    except Exception , e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        abort(500)


@admin_frontend.route('/keyword/update', methods=["POST"])
@admin_required
def keyword_update():
   u"""keyword Update"""
   try:
        with db_session_cm() as session:
            if request.method == 'POST':
                plan_form = PlanKeywordsForm(request.form)
                keyword_id = plan_form.id.data.strip()
                content = plan_form.content.data.strip()
                session.query(PlanKeyword).filter(PlanKeyword.id == keyword_id).update(dict(content=content))
                session.commit()
        return redirect(url_for('admin_frontend.keywords'))
   except Exception ,e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        abort(500)


@admin_frontend.route('/keyword/del/<int:keyword_id>')
@admin_required
def keyword_delete(keyword_id):
    u"""删除关键字"""
    try:
        with db_session_cm() as session:
            keyword = session.query(PlanKeyword).get(keyword_id)
            if current_user and current_user.is_authenticated:
                session.delete(keyword)
                session.commit()
                flash(_(u"删除成功!"))
            else:
                flash(_(u"没有权限!"))
        return redirect(url_for('admin_frontend.keywords'))
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        print traceback.format_exc(e)
        flash(_(u"删除失败!"))
        return redirect(url_for('admin_frontend.keywords'))


@admin_frontend.route('/impresses')
@admin_required
def impresses():
    u"""印象管理"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", ImpressContent.PER_PAGE, type=int)
    with db_session_cm() as session:
        impresses_query = session.query(ImpressContent)
        pagination = Pagination(page=page, total=impresses_query.count(), record_name=_(u"印象"), bs_version=3)
        impresses_query = impresses_query.order_by(ImpressContent.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "impresses": impresses_query.all(),
            "pagination": pagination
        }
        return render_template("admin/impress/index.html", **context)


@admin_frontend.route('/impress/new', methods=["GET", "POST"])
@admin_required
def impress_new():
    u"""新建印象"""
    try:
        impress_form = PresetImpressForm(request.form)
        context = {
            'form': impress_form,
        }
        if request.method == 'POST' and impress_form.validate_on_submit():
            content = impress_form.content.data.strip()
            with db_session_cm() as session:
                impress_content = ImpressContent(content=content)
                impress_content.type = ImpressContent.TYPE_PRESET
                session.add(impress_content)
                session.commit()
            flash(_(u"添加成功!"), category="success")
            return redirect(url_for('admin_frontend.impresses'))
        return render_template("admin/impress/new.html", **context)
    except Exception, e:
        common_logger.error(traceback.format_exc(e))
        abort(500)


@admin_frontend.route('/impress/<int:impress_id>')
@admin_required
def impress_show(impress_id):
    u"""印象详情"""
    return render_template("admin/impress/show.html")


@admin_frontend.route('/impress/<int:impress_id>')
@admin_required
def impress_delete(impress_id):
    u"""删除印象"""
    return render_template("admin/impress/index.html")


@admin_frontend.route('/comments')
@admin_required
def comments():
    u"""评论管理"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", PlanKeyword.PER_PAGE, type=int)
    with db_session_cm() as session:
        keywords_query = session.query(PlanKeyword)
        pagination = Pagination(page=page, total=keywords_query.count(), record_name=_(u"评论"), bs_version=3)
        keywords = keywords_query.order_by(PlanKeyword.id.desc()).offset((page - 1) * per_page).limit(per_page)
        context = {
            "keywords": keywords.all(),
            "pagination": pagination
        }
        return render_template("admin/comment/index.html", **context)


@admin_frontend.route('/comment/<int:comment_id>')
@admin_required
def comment_show(comment_id):
    u"""评论详情"""
    return render_template("admin/comment/show.html")


@admin_frontend.route('/comment/<int:comment_id>')
@admin_required
def comment_delete(comment_id):
    u"""删除评论"""
    return render_template("admin/comment/index.html")