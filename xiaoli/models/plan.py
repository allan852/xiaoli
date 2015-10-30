#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from flask import url_for
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from xiaoli.extensions.upload_set import image_resources
from xiaoli.models import ImageResource
from xiaoli.models.base import Base
from xiaoli.models.session import db_session_cm
from xiaoli.utils.date_util import format_date

__author__ = 'zouyingjun'


class Plan(Base):
    __tablename__ = "plans"

    #
    STATUS_UNPUBLISHED = "unpublished"
    STATUS_PUBLISH = "publish"
    STATUS_UNSHELVE = "unshelve"
    STATUS_DELETE = "unshelve"
    STATUS_CHOICES = (
        (STATUS_UNPUBLISHED, u"未发布"),
        (STATUS_PUBLISH, u"已经发布"),
        (STATUS_UNSHELVE, u"已下架"),
        (STATUS_DELETE, u"删除"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 方案名称
    title = Column(String(1024), nullable=False)
    # 方案状态
    status = Column(String(64), nullable=False)
    # 发布日期
    publish_date = Column(DateTime)
    # 作者id
    author_id = Column(Integer, ForeignKey("accounts.id"))
    # 封面图片id
    cover_image_id = Column(Integer, ForeignKey("image_resources.id"))
    # 阅读次数
    view_count = Column(BigInteger, default=0)
    # 分享次数
    share_count = Column(BigInteger, default=0)

    content = relationship("PlanContent", uselist=False,backref='plan',cascade="all, delete-orphan")
    keywords = relationship("PlanKeyword", backref='plan', secondary="plan_keyword_rel")

    def __init__(self, title):
        self.title = title
        self.status = Plan.STATUS_UNPUBLISHED
        self.view_count = 0
        self.share_count = 0

    @property
    def screen_status(self):
        for sign, text in Plan.STATUS_CHOICES:
            if sign == self.status:
                return text

    @property
    def screen_publish_time(self):
        return format_date(self.publish_date) if self.publish_date else ""

    def publish(self):
        self.status = Plan.STATUS_PUBLISH
        if not self.publish_date:
            self.publish_date = datetime.datetime.now()

    @property
    def cover_image(self):
        with db_session_cm() as session:
            if self.cover_image_id:
                image = session.query(ImageResource).get(self.cover_image_id)
                if image is None:
                    return ""
                else:
                    url = image_resources.url(image.path)
                    return url
            else:
                return ""

    @property
    def is_published(self):
        return self.status == Plan.STATUS_PUBLISH

    def to_dict(self, content=False):
        d = {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "publish_date": self.publish_date or "",
            "author_id": self.author_id,
            "cover_image_id": self.cover_image_id or "",
            "cover_image_url": self.cover_image or "",
            "view_count": self.view_count,
            "share_count": self.share_count,
            "content": self.content.content if content else "",
            "keywords": [ word.content for word in self.keywords],
            "share_detail_url": url_for("plan.share_detail", plan_id=self.id, _external=True)
        }
        return d


class PlanContent(Base):
    __tablename__ = "plan_contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 方案id， 外键
    plan_id = Column(Integer, ForeignKey("plans.id"))
    # 方案内容
    content = Column(Text, nullable=False)


class PlanKeyword(Base):
    __tablename__ = "plan_keywords"

    PER_PAGE = 10

    TYPE_PRESET = "preset"
    TYPE_USERADD = "useradd"
    TYPE_CHOICES = (
        (TYPE_PRESET, u"系统预设"),
        (TYPE_USERADD, u"用户添加"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 关键字内容
    content = Column(String(128), nullable=False)
    # 关键字类型
    type = Column(String(64), nullable=False, default=TYPE_USERADD)

    @property
    def screen_type(self):
        u"""用户类型显示名称"""
        for sign, text in PlanKeyword.TYPE_CHOICES:
            if sign == self.type:
                return text

    @property
    def is_preset(self):
        return self.type == PlanKeyword.TYPE_PRESET

    @classmethod
    def choices(cls):
        options = []
        with db_session_cm() as session:
            keywords = session.query(PlanKeyword).all()
            for kw in keywords:
                options.append((kw.id, kw.content))
        return options

    def to_dict(self):
        d = {
            "id": self.id,
            "type": self.type,
            "content": self.content,
        }
        return d
