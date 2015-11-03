#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, object_session
from werkzeug.security import generate_password_hash, check_password_hash
from xiaoli.config import setting
from xiaoli.extensions.upload_set import image_resources
from xiaoli.models.base import Base
from xiaoli.models.relationships import account_plan_favorite_rel_table, \
    account_plan_vote_rel_table
from xiaoli.models.session import db_session_cm
from xiaoli.utils.date_util import format_date
from xiaoli.utils.logs.logger import common_logger

__author__ = 'zouyingjun'


class Account(Base, UserMixin):
    __tablename__ = 'accounts'
    PER_PAGE = 10

    BIRTHDAY_FORMAT = "%Y-%m-%d"

    HOROSCOPE_CHOICES = (
        ("Aries", u"牡羊座"),
        ("Taurus", u"金牛座"),
        ("Gemini", u"雙子座"),
        ("Cancer", u"巨蟹座"),
        ("Leo", u"獅子座"),
        ("Virgo", u"處女座"),
        ("Libra", u"天秤座"),
        ("Scorpio", u"天蠍座"),
        ("Sagittarius", u"射手座"),
        ("Capricorn", u"魔羯座"),
        ("Aquarius", u"水瓶座"),
        ("Pisces", u"雙魚座"),
    )

    STATUS_UNREGISTERED = "unregistered"
    STATUS_ACTIVE = "active"
    STATUS_FREEZE = "freeze"
    STATUS_CHOICES = (
        (STATUS_UNREGISTERED, u"未注册"),
        (STATUS_ACTIVE, u"激活"),
        (STATUS_FREEZE, u"冻结"),
    )

    TYPE_USER = "user"
    TYPE_ADMIN = "admin"
    TYPE_CHOICES = (
        (TYPE_USER, u"普通用户"),
        (TYPE_ADMIN, u"系统管理员")
    )

    SEX_MALE = "male"
    SEX_FEMALE = "female"
    SEX_CHOICES = (
        (SEX_MALE, "男"),
        (SEX_FEMALE, "女"),
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
    to_friends = association_proxy("friend_to_relations", "to_account")
    from_friends = association_proxy("friend_from_relations", "from_account")

    favorite_plans = relationship("Plan", secondary=account_plan_favorite_rel_table, lazy="dynamic")
    vote_plans = relationship("Plan", secondary=account_plan_vote_rel_table, lazy="dynamic")
    plans = relationship("Plan", backref="account", foreign_keys="[Plan.author_id]")

    def __init__(self, phone, password):
        self.cellphone = phone
        self.password = password

    def __repr__(self):
        return "<%s object with cellphone=%s>" % (self.__class__.__name__, self.cellphone)

    @property
    def is_admin(self):
        return self.type == Account.TYPE_ADMIN

    @property
    def is_active(self):
        return self.status == Account.STATUS_ACTIVE

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = generate_password_hash(pw, salt_length=16)

    @property
    def has_registered(self):
        u"""是否注册过，导入的好友不算注册"""
        return self.status != Account.STATUS_UNREGISTERED

    @property
    def screen_type(self):
        u"""用户类型显示名称"""
        for sign, text in Account.TYPE_CHOICES:
            if sign == self.type:
                return text

    @property
    def screen_status(self):
        u"""用户状态现实名称"""
        for sign, text in Account.STATUS_CHOICES:
            if sign == self.status:
                return text

    def check_password(self, pw):
        u"""检测密码"""
        return check_password_hash(self._password, pw)

    def update_info(self, **kwargs):
        u"""更新用户信息"""
        if kwargs.has_key("current_password"):
            new_password = kwargs.get("new_password")
            self.password = new_password

        # 日期格式 值更新
        if kwargs.has_key("birthday"):
            birthday = kwargs.get("birthday")
            self.birthday = datetime.datetime.strptime(birthday, Account.BIRTHDAY_FORMAT)

        # 字符串 值更新
        for key in ["sex", "horoscope", "nickname"]:
            if kwargs.has_key(key):
                value = kwargs.get(key)
                setattr(self, key, value)

        # bool 值更新
        for key in ["allow_notice", "allow_score"]:
            if kwargs.has_key(key):
                value = int(kwargs.get(key))
                print value, key, type(value), bool(value)
                setattr(self, key, bool(value))

    @classmethod
    def import_friends(cls, session, account_id, contacts):
        u"""导入联系人
        :param session: A DB session instance
        :param account_id: 需要添加朋友的账户id
        :param contacts: A list with dict content. format:
            contacts = [
                {
                    "phone": "15333333331",
                    "name": "小芳",
                    "email": "xiaofang@123.com"
                },
                {
                    "phone": "15333333332",
                    "name": "小明",
                    "email": "xiaofang@123.com"
                }
            ]
        the "phone" and "name" is required, "email" is optional.

        导入原则：
        1. "phone": 已经存在的，检查是否是朋友关系，如不是，添加成朋友;
        2. "phone": 不存在直接写入;
        3. "name" 重名的，采用重新修改"name"为 "name" + "phone";
        """
        account = session.query(Account).get(account_id)
        for contact in contacts:
            phone = contact.get("phone")
            name = contact.get("name")
            email = contact.get("email")
            friend = session.query(Account).filter(Account.cellphone == phone).first()
            if not friend:
                # 朋友不存在, 创建
                new_friend = Account(phone, phone[5:11])
                # 设置成未注册
                new_friend.status = Account.STATUS_UNREGISTERED
                if email:
                    new_friend.email = email
                common_logger.debug(account.to_friends)
                af = AccountFriend()
                af.from_account = account
                af.to_account = new_friend
                af.nickname = name
                session.add(new_friend)
                session.add(af)
            else:
                # 存在， 检测是否已经是朋友关系
                common_logger.debug(friend)
                af_query = session.query(AccountFriend).\
                    filter(AccountFriend.from_account == account).\
                    filter(AccountFriend.to_account == friend)
                common_logger.debug(af_query)
                exists_af = af_query.first()
                common_logger.debug(exists_af)
                if not exists_af:
                    # 不是朋友关系则添加成朋友关系
                    af = AccountFriend()
                    af.from_account = account
                    af.to_account = friend
                    af.nickname = name
                    session.add(af)

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
            "nickname": self.nickname or "",
            "cellphone": self.cellphone,
            "email": self.email or "",
            "sex": self.sex or "",
            "birthday": self.birthday or "",
            "horoscope": self.horoscope or "",
            "status": self.status,
            "type": self.type,
            "score": 0,
            "avatar_url": self.avatar and self.avatar.url or "",
            "allow_notice": self.allow_notice,
            "allow_score": self.allow_score
        }
        return d


class AccountFriend(Base):
    u"""Association Object for Account Friends"""
    __tablename__ = "account_friends"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    nickname = Column(String(64), index=True)
    note = Column(String(1024))

    from_account = relationship(Account, backref="friend_to_relations", primaryjoin=(from_account_id == Account.id))
    to_account = relationship(Account, backref="friend_from_relations", primaryjoin=(to_account_id == Account.id))


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 头像所有者id，外键
    account_id = Column(Integer, ForeignKey("accounts.id"))
    # 头像存储路径
    path = Column(String(1024))
    # 头像格式，即图片后缀名
    format = Column(String(16))

    def __init__(self, account_id, path=None, ):
        self.account_id = account_id
        if path:
            self.path = path

    @property
    def url(self):
        return image_resources.url(self.path)


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

    PER_PAGE = 10

    TYPE_PRESET = "preset"
    TYPE_USERADDED = "useradded"
    TYPE_CHOICES = (
        (TYPE_PRESET, u"系统预设"),
        (TYPE_USERADDED, u"用户添加"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 印象内容类型
    type = Column(String(16), nullable=False, default=TYPE_USERADDED)
    # 印象内容
    content = Column(String(10), nullable=False, index=True)

    def __init__(self, content):
        self.content = content

    @property
    def screen_type(self):
        u"""用户类型显示名称"""
        for sign, text in ImpressContent.TYPE_CHOICES:
            if sign == self.type:
                return text

    @property
    def is_preset(self):
        return self.type == ImpressContent.TYPE_PRESET

    @classmethod
    def get_or_create(cls, session, content):
        impress_content = session.query(ImpressContent).filter(ImpressContent.content==content).first()
        if impress_content:
            return impress_content
        new_impress_content = cls(content)
        return new_impress_content

    def to_dict(self):
        d = {
            "id": self.id,
            "content": self.content
        }
        return d


class Impress(Base):
    __tablename__ = "impresses"

    PER_PAGE = 10

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



