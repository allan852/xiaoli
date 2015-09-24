#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

__author__ = 'zouyingjun'

admin_frontend = Blueprint("admin_frontend", __name__, template_folder="templates", static_folder="../static")


@admin_frontend.route('/')
def index():
    return render_template("admin/frontend/index.html")