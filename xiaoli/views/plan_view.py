#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from flask import Blueprint, render_template, abort
from sqlalchemy.orm.exc import NoResultFound
from xiaoli.models import Plan
from xiaoli.models.session import db_session_cm
from xiaoli.utils.logs.logger import common_logger

__author__ = 'zouyingjun'

plan = Blueprint("plan", __name__, template_folder="templates", static_folder="../static")


@plan.route('/')
def index():
    return render_template("plan/index.html")


@plan.route('/<plan_id>')
def show(plan_id):
    return render_template("plan/index.html")


@plan.route('/share_detail/<plan_id>')
def share_detail(plan_id):
    try:
        with db_session_cm() as session:
            plan = session.query(Plan).outerjoin(Plan.keywords).outerjoin(Plan.content).\
                filter(Plan.status == Plan.STATUS_PUBLISH).filter(Plan.id == plan_id).one()
            return render_template("plan/share_detail.html", plan=plan)
    except NoResultFound:
        common_logger.warn("view not exists or unpublished plan = %s" % plan_id)
        abort(404)
    except Exception as e:
        common_logger.error(traceback.format_exc(e))
        abort(500)


@plan.route('/mew', methods=["GET", "POST"])
def new():
    return render_template("plan/index.html")


@plan.route('/edit', methods=["POST"])
def edit():
    return render_template("plan/index.html")