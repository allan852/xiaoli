#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

__author__ = 'zouyingjun'

admin_frontend = Blueprint("admin_frontend", __name__, template_folder="templates", static_folder="../static")


@admin_frontend.route('/')
def index():
    u"""管理员首页"""
    return render_template("admin/frontend/index.html")


@admin_frontend.route('/accounts')
def accounts():
    u"""用户列表"""
    return render_template("admin/account/index.html")


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
    return render_template("admin/plan/index.html")


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


@admin_frontend.route('/plan/publish/<int:plan_id>')
def plan_publish(plan_id):
    u"""发布方案"""
    return render_template("admin/plan/index.html")


@admin_frontend.route('/plan/revocation/<int:plan_id>')
def plan_revocation(plan_id):
    u"""撤销方案"""
    return render_template("admin/plan/index.html")
