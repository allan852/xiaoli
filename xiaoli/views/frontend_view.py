#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, send_file

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
    pass


@frontend.route('/logout', methods=["POST"])
def logout():
    u"""登出"""
    pass


@frontend.route('/favicon.ico')
def favicon():
    return send_file("static/favicon.ico")