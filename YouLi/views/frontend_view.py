#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

__author__ = 'zouyingjun'

frontend = Blueprint("frontend", __name__, template_folder="templates/api_v1", static_folder="../static")


@frontend.route('/')
def index():
    return "Hello youli"


@frontend.route('/login')
def login():
    pass
