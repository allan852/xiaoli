#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint

__author__ = 'zouyingjun'

api_v1 = Blueprint("api_v1", __name__, template_folder="templates/api_v1", static_folder="../static")
