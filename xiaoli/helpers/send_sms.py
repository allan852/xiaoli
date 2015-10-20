#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'roc'

import httplib,urllib, random
from xiaoli.config import setting

class SendSms(object):
    @staticmethod
    def send(phone,content):
        httpClient = None
        try:
            username = setting.SMS["username"]
            password = setting.SMS["password"]
            api_key = setting.SMS["apikey"]
            content = content.decode('gbk','ignore')
            if phone and content:
                params = urllib.urlencode({'username':username,'password':password,'apikey':api_key,'mobile':phone,'content':content})
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                httpClient = httplib.HTTPConnection("m.5c.com.cn", 80, timeout=30)
                httpClient.request("POST", "/api/send/index.php", params, headers)
                response = httpClient.getresponse()
                # print response.status
                # print response.reason
                return response.read()
            else:
                return 403
        except Exception, e:
            print e
            return 500
        finally:
            if httpClient:
                httpClient.close()
    @staticmethod
    def rand_code():
        return int(random.random() * 100000)