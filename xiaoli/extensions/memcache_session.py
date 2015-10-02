# encoding = utf-8
"""
A flask session memcached store
"""
from datetime import timedelta, datetime
from uuid import uuid4

__author__ = 'zou'
import memcache
import pickle
from flask.sessions import SessionMixin, SessionInterface
from werkzeug.datastructures import CallbackDict


class MemcachedSession(CallbackDict, SessionMixin):
    """"""
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class MemcachedSessionInterface(SessionInterface):
    serializer = pickle
    session_class = MemcachedSession

    def generate_sid(self):
        return str(uuid4())

    def get_memcache_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=8)

    def __init__(self, client=None, prefix="session:"):
        if client is None:
            client = memcache.Client()
        self.client = client
        self.prefix = prefix

    def open_session(self, app, request):
        sid = request.args.get("sessionid", None) or request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.client.get(str(self.prefix + sid))
        if val is not None:
            data = self.serializer.loads(val)
            self.client.set(self.prefix + str(sid), val, int(timedelta(days=8).total_seconds()))
            return self.session_class(data, sid=sid)
        new_sid = self.generate_sid()
        return self.session_class(sid=new_sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.client.delete(str(self.prefix + session.sid))
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        memcache_exp = self.get_memcache_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.client.set(self.prefix + str(session.sid), val, int(memcache_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid, expires=cookie_exp, httponly=True, domain=domain, max_age= 7*24*60*60)

    def set_cas_ticket_to_session_mapping(self, app, session, ticket):
        memcache_exp = self.get_memcache_expiration_time(app, session)
        val = str(session.sid)
        self.client.set(str(ticket), val, int(memcache_exp.total_seconds()))

    def del_ticket_session_mapping(self, ticket):
        session_sid = self.client.get(str(ticket))
        if session_sid:
            r = self.client.delete(self.prefix + str(session_sid))
#            if r == 1:
#                print 'already delete session id= ' + session_sid
        r = self.client.delete(str(ticket))
#        if r == 1:
#            print 'already delete ticket = ' + ticket
