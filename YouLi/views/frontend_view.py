#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

__author__ = 'zouyingjun'

frontend = Blueprint("frontend", __name__, template_folder="templates", static_folder="../static")


@frontend.route('/')
def index():
    return render_template("frontend/index.html")


@frontend.route('/login')
def login():
    pass
