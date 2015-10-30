#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, url_for, request, render_template, session
from flask.ext.babel import Babel
from flask.ext.cdn import CDN
from flask.ext.uploads import configure_uploads, patch_request_class
from flask.ext.wtf.i18n import Translations

from xiaoli.config import setting
from xiaoli import views
from xiaoli.utils import login_manager
from xiaoli import filters
from xiaoli import helpers
from flask.ext.login import current_user
# from xiaoli.utils.extensions.memcache_session import MemcachedSessionInterface

import os
import logging

__author__ = 'zouyingjun'


default_blueprints = (
    (views.frontend, ''),
    (views.api_v1, '/api/v1'),
    (views.plan, '/plan'),

    # for admin
    (views.admin_frontend, '/admin'),
)


def configure_blueprints(app, blueprints):
    if blueprints:
        for view, url_prefix in blueprints:
            app.register_blueprint(view, url_prefix=url_prefix)


def configure_i18n(app):
    app.config['BABEL_DEFAULT_LOCALE'] = setting.DEFAULT_INIT_LOCALE

    def ugettext(self, message):
        missing = object()
        tmsg = self._catalog.get(unicode(message), missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.ugettext(message)
            return unicode(message)
        return tmsg

    Translations.ugettext = ugettext

    babel = Babel(app)

    # @babel.localeselector
    # def get_locale():
    #     if not current_user.is_authenticated:
    #         return session.get('user_locale') or setting.DEFAULT_INIT_LOCALE
    #     else:
    #         return current_user.locale


def configure_url_for_with_timestamp(app):
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        import os
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                if os.path.exists(file_path):
                    values['v'] = int(os.path.getmtime(file_path))
                else:
                    values['v'] = setting.VERSION

        return url_for(endpoint, **values)


def configure_login_manager(app):
    login_manager.init_app(app)


def configure_jinja_globals(app):
    app.jinja_env.globals['url_for_other_page'] = helpers.url_for_other_page


def configure_logger(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s: %(lineno)d]'
    )
    if not app.debug:
        log_file = os.path.join(setting.LOG_FILE_PATH, "%s.log" % app.config["APP_NAME"])
        youli_handler = logging.FileHandler(log_file)
        youli_handler.setFormatter(formatter)
        youli_handler.setLevel(logging.WARNING)
        app.logger.addHandler(youli_handler)


# def configure_memcache_session_interface(app):
#     '''store session with memcache'''
#     client = memcache.Client(app.config['MEMCACHED_MACHINES'])
#     app.session_interface = MemcachedSessionInterface(client)


def configure_filter(app):
    @app.template_filter()
    def strim(value, exp):
        return filters.strim(value, exp)

    @app.template_filter()
    def dateformat(value, format='%Y-%m-%d'):
        return filters.dateformat(value, format)

    @app.template_filter()
    def datetimeformat(value, format='%Y-%m-%d %H:%M'):
        return value and value.strftime(format) or ''


def configure_url(app):
    pass


def configure_error_handler(app):
    @app.errorhandler(404)
    def not_found(error):
        if request.is_xhr:
            return error
        return render_template("404.html", error=error), 404


def configure_context_processor(app):
    # @app.context_processor
    # def get_user_locale():
    #     if not current_user.is_authenticated:
    #         user_locale = session.get('user_locale') or setting.DEFAULT_INIT_LOCALE
    #         return {'user_locale': user_locale.replace('_', '-')}
    #     else:
    #         return {'user_locale': current_user.locale.replace('_', '-')}
    pass


def configure_cdn_url_for(app):
    u"""是的url_for智能使用cdn地址"""
    cdn = CDN()
    cdn.init_app(app)


def configure_upload_sets(app):
    u"""设置 Upload Sets"""
    from xiaoli.extensions.upload_set import image_resources
    configure_uploads(app, (image_resources,))
    patch_request_class(app, app.config["DEFAULT_UPLOAD_IMAGE_SIZE"])


def create_app(config=None):
    print setting
    app = Flask(setting.APP_NAME)

    if config:
        app.config.from_object(config)

    configure_i18n(app)

    configure_blueprints(app, default_blueprints)

    configure_logger(app)

    configure_jinja_globals(app)

    configure_filter(app)

    # configure_memcache_session_interface(app)

    # configure_url_for_with_timestamp(app)

    configure_login_manager(app)

    configure_url(app)

    # configure_error_handler(app)

    configure_context_processor(app)

    configure_cdn_url_for(app)

    configure_upload_sets(app)

    return app

if __name__ == "__main__":
    app = create_app(config=setting)
    print app
    app.run()
