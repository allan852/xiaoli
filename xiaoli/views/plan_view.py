#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

__author__ = 'zouyingjun'

plan = Blueprint("plan", __name__, template_folder="templates", static_folder="../static")


@plan.route('/')
def index():
    return render_template("plan/index.html")


@plan.route('/<plan_id>')
def show(plan_id):
    pass


@plan.route('/mew', methods=["GET", "POST"])
def new():
    return render_template("plan/index.html")


@plan.route('/edit', methods=["POST"])
def edit():
    return render_template("plan/index.html")