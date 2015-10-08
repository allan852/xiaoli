#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, object_session
from werkzeug.security import generate_password_hash, check_password_hash
from xiaoli.config import setting
from xiaoli.models.base import Base
from xiaoli.models.relationships import account_plan_favorite_rel_table, \
    account_plan_vote_rel_table, account_friends_rel_table
from xiaoli.models.session import db_session_cm
from xiaoli.utils.date_util import format_date

__author__ = 'zouyingjun'


class Account(Base, UserMixin):
    __tablename__ = 'accounts'

    HOROSCOPE_CHOICES = (
        ("Aries", "牡羊座"),
        ("Taurus", "金牛座"),
        ("Gemini", "雙子座"),
        ("Cancer", "巨蟹座"),
        ("Leo", "獅子座"),
        ("Virgo", "處女座"),
        ("Libra", "天秤座"),
        ("Scorpio", "天蠍座"),
        ("Sagittarius", "射手座"),
        ("Capricorn", "魔羯座"),
        ("Aquarius", "水瓶座"),
        ("Pisces", "雙魚座"),
    )

    STATUS_UNREGISTERED = "unregistered"
    STATUS_ACTIVE = "active"
    STATUS_FREEZE = "freeze"
    STATUS_CHOICES = (
        (STATUS_UNREGISTERED, "未注册"),
        (STATUS_ACTIVE, "激活"),
        (STATUS_FREEZE, "冻结"),
    )

    TYPE_USER = "user"
    TYPE_ADMIN = "admin"
    TYPE_CHOICES = (
        (TYPE_USER, "普通用户"),
        (TYPE_ADMIN, "系统管理员")
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 昵称
    nickname = Column(String(64), unique=True, index=True)
    # 手机号
    cellphone = Column(String(32), unique=True, nullable=False, index=True)
    # email
    email = Column(String(128))
    # password, 加密后信息
    _password = Column(String(128), nullable=False)
    # 性别
    sex = Column(String(16))
    # 生日
    birthday = Column(DateTime)
    # 星座
    horoscope = Column(String(16))
    # 账户状态
    status = Column(String(64), default=STATUS_ACTIVE)
    # 账户类型
    type = Column(String(64), default=TYPE_USER)
    # 是否接受系统通知
    allow_notice = Column(Boolean, default=True)
    # 是否允许别人给自己打分
    allow_score = Column(Boolean, default=True)

    # relationship
    avatar = relationship("Avatar", backref="account", uselist=False)
    scores = relationship("Score", backref="account", foreign_keys="[Score.target_id]")
    added_scores = relationship("Score", backref="account1", foreign_keys="[Score.operator_id]")
    impresses = relationship("Impress", backref="target", foreign_keys="[Impress.target_id]")
    added_impresses = relationship("Impress", backref="operator", foreign_keys="[Impress.operator_id]")
    comments = relationship("Comment", backref="target", foreign_keys="[Comment.target_id]",
                            order_by="Comment.create_time.desc()", lazy="dynamic")
    added_comments = relationship("Comment", backref="operator", foreign_keys="[Comment.operator_id]",
                                  order_by="Comment.create_time.desc()", lazy="dynamic")
    friends = relationship("Account",
                           secondary=account_friends_rel_table,
                           primaryjoin=id==account_friends_rel_table.c.account_id,
                           secondaryjoin=id==account_friends_rel_table.c.friend_account_id,
                           backref="account")

    favorite_plans = relationship("Plan", secondary=account_plan_favorite_rel_table, lazy="dynamic")
    vote_plans = relationship("Plan", secondary=account_plan_vote_rel_table, lazy="dynamic")

    def __init__(self, phone, password):
        self.cellphone = phone
        self.password = password

    @property
    def is_admin(self):
        return self.type == Account.TYPE_ADMIN

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = generate_password_hash(pw, salt_length=16)

    def check_password(self, pw):
        return check_password_hash(self._password, pw)

    @classmethod
    def exists_phone(cls, phone):
        with db_session_cm() as session:
            account = session.query(Account).filter(Account.cellphone == phone).first()
            if account:
                return True
            return False

    def impresses_with_group(self):
        u"""按照印象内容分组获得印象个数量"""
        session = object_session(self)
        query = session.query(Account, ImpressContent.c.content, func.count(Impress.c.id).label("total"))\
            .join(Account.impresses, Impress.content).group_by(Impress.content_id)

        res = query.all()

        return res

    def to_dict(self):
        d = {
            "id": self.id,
            "nickname": self.nickname,
            "cellphone": self.cellphone,
            "email": self.email,
            "sex": self.sex,
            "birthday": self.birthday,
            "horoscope": self.horoscope,
            "status": self.status,
            "type": self.type,
            "score": 0,
            "avatar_url": ""
        }
        return d


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 头像所有者id，外键
    account_id = Column(Integer, ForeignKey("accounts.id"))
    # 头像存储路径
    path = Column(String(1024))
    # 头像格式，即图片后缀名
    format = Column(String(16))


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被打分人id，外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 打分人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 分数
    score = Column(Integer, default=0)


class Comment(Base):
    __tablename__ = "comments"

    PER_PAGE = setting.PER_PAGE

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被评论人id， 外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 评论人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 评论内容
    content = Column(String(1024), nullable=False)

    def to_dict(self):
        d = {
            "id": self.id,
            "operator_id": self.operator.id,
            "operator_name": self.operator.nickname,
            "content": self.content,
            "create_time": format_date(self.create_time)
        }

        return d


class ImpressContent(Base):
    __tablename__ = "impress_contents"

    TYPE_PRESET = "preset"
    TYPE_USERADDED = "useradded"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 印象内容类型
    type = Column(String(16), nullable=False, default=TYPE_USERADDED)
    # 印象内容
    content = Column(String(10), nullable=False, index=True)

    def __init__(self, content):
        self.content = content

    @classmethod
    def get_or_create(cls, session, content):
        impress_content = session.query(ImpressContent).filter(ImpressContent.content==content).first()
        if impress_content:
            return impress_content
        new_impress_content = cls(content)
        return new_impress_content


class Impress(Base):
    __tablename__ = "impresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被添加影响人id， 外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 添加人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 印象内容id
    content_id = Column(Integer, ForeignKey("impress_contents.id"))

    # relationship
    content = relationship("ImpressContent", backref="impress", uselist=False)
    preset_contents = relationship("ImpressContent",
                                   backref="impress1",
                                   primaryjoin="and_(Impress.content_id==ImpressContent.id, "
                                               "ImpressContent.type=='%s')" % ImpressContent.TYPE_PRESET)

    def to_dict(self):
        d = {
            "id": self.id,
            "target": self.target.to_dict(),
            "operator": self.operator.to_dict(),
            "content": self.content.content,
            "type": self.content.type,
            "create_time": format_date(self.create_time),
            "count": 1
        }

        return d



