#!/usr/bin/env python
# -*- coding:utf-8 -*-
from xiaoli.models.relationships import account_friends_rel_table, \
    plan_keyword_rel_table, account_plan_vote_rel_table, account_plan_favorite_rel_table
from xiaoli.models.account import Account, Avatar, Score, Comment, Impress, ImpressContent
from xiaoli.models.feedback import Feedback
from xiaoli.models.image import ImageResource
from xiaoli.models.notice import Notice
from xiaoli.models.plan import Plan, PlanContent, PlanKeyword
from xiaoli.models.token import Token
from xiaoli.models.sms import Sms
from xiaoli.models.uploader import Uploader

__author__ = 'zouyingjun'
