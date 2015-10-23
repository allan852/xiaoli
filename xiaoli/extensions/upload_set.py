#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask.ext.uploads import UploadSet, IMAGES

__author__ = 'zouyingjun'


image_resources = UploadSet('images', IMAGES)