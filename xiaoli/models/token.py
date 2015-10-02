#!/usr/bin/env python
# -*- coding:utf-8 -*-
import uuid
import datetime
from sqlalchemy import Column, ForeignKey, String, Boolean, Text, DateTime
from sqlalchemy import Integer
from xiaoli.models import Base, db_session_cm
from xiaoli.utils.date_util import get_next_n_days

__author__ = 'zouyingjun'


def token_expire_date():
    return get_next_n_days(Token.DEFAULT_EXPIRE_DAYS)


def get_token_code():
    return uuid.uuid1().hex


class Token(Base):
    __tablename__ = "tokens"

    DEFAULT_EXPIRE_DAYS = 7

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 通知接受者id, 外键
    account_id = Column(Integer, ForeignKey("accounts.id"), unique=True)
    # token
    code = Column(String(32), nullable=False, unique=True)
    # expire date
    expire_date = Column(DateTime, default=token_expire_date)

    @property
    def is_expire(self):
        u"""是否过期"""
        return self.expire_date < datetime.datetime.now()

    @classmethod
    def get_token(cls, account_id, force_update=False):
        u"""获得用户对应的token
        :param account_id: 用户id
        :param force_update: 时候强制更新，当用户的token存在时起作用，不论用户token 是否过期强制更新为7天后
        """
        with db_session_cm as session:
            query = session.query(Token).filter(Token.account_id == account_id)
            if query.exists():
                token = query.one()
                if force_update:
                    token.expire_date = token_expire_date()
                    session.add(token)
                    session.commit()
                return token
            else:
                token = Token()
                token.account_id = account_id
                token.code = get_token_code()
                session.add(token)
                session.commit()
                return token
