#! -*- coding=utf-8 -*-
import traceback
from flask import g, current_app, abort
from bson.objectid import ObjectId


def strim(value, exp=' '):
    return value.strip(exp)


def dateformat(value, format='%Y-%m-%d'):
    return value.strftime(format)


def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)


def pull_workspace_id(endpoint, values):
    g.workspace_id = ObjectId(values.pop('workspace_id')) if values and values.get('workspace_id') else None


def add_workspace_id_for_url(app, endpoint, values):
    if 'workspace_id' in values or not g.workspace_id:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'workspace_id'):
        values['workspace_id'] = str(g.workspace_id)