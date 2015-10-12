#! -*- coding=utf-8 -*-
from flask import g


def strim(value, exp=' '):
    return value.strip(exp)


def dateformat(value, format='%Y-%m-%d'):
    return value.strftime(format)


def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)


def add_workspace_id_for_url(app, endpoint, values):
    if 'workspace_id' in values or not g.workspace_id:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'workspace_id'):
        values['workspace_id'] = str(g.workspace_id)