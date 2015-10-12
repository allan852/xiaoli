#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, send_file

__author__ = 'zouyingjun'

frontend = Blueprint("frontend", __name__, template_folder="templates", static_folder="../static")


@frontend.route('/')
def index():
    return render_template("frontend/index.html")


@frontend.route('/login')
def login():
    pass


@frontend.route('/favicon.ico')
def favicon():
    return send_file("static/favicon.ico")