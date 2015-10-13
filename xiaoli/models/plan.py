#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from xiaoli.models.base import Base


__author__ = 'zouyingjun'


class Plan(Base):
    __tablename__ = "plans"

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

    contents = relationship("PlanContent",backref='plan',cascade="all, delete-orphan")
    keywords = relationship("PlanKeyword",backref='plan',secondary="plan_keyword_rel")

    def to_dict(self):
        d = {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "publish_date": self.publish_date,
            "author_id": self.author_id,
            "cover_image_id": self.cover_image_id,
            "cover_image_url": '',
            "view_count": self.view_count,
            "share_count": self.share_count,
            "contents": [content.content for content in self.contents],
            "keywords": [ word.content for word in self.keywords]
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 关键字内容
    content = Column(String(128), nullable=False)
