#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
__author__ = 'zouyingjun'


def format_date(date, format="%Y-%m-%d"):
    if not isinstance(date, datetime):
        raise "date params must a datetime object"
    return date.strftime(format)


def get_previous_month():
    u"""
    获取上月第一天开始时间
    """

    date = datetime.now()
    if is_first_day_in_month(date):
        year = date.year - 1
        month = 12
    else:
        year = date.year
        month = date.month - 1
    ret_date = datetime.replace(date, year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    return ret_date


def get_next_month():
    u"""
    获取下月第一天的开始时间
    """
    date = datetime.now()
    if is_last_month_in_year(date):
        year = date.year + 1
        month = 1
    else:
        year = date.year
        month = date.month + 1

    ret_date = datetime.replace(date, year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    return ret_date


def get_next_of_one_month(date):
    u"""
    获取某个月下月第一天的开始时间
    """
    if is_last_month_in_year(date):
        year = date.year + 1
        month = 1
    else:
        year = date.year
        month = date.month + 1

    ret_date = datetime.replace(date, year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    return ret_date


def is_first_day_in_month(date):
    u"""给定的时间是不是一个中第一天"""
    if date.month == 1:
        return True
    return False


def is_last_month_in_year(date):
    u"""给定的时间是不是一年中最后一个月"""
    if date.month == 12:
        return True
    return False


def is_current_month(date):
    u"""是不是当月"""
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    check_year = date.year
    check_month = date.month

    return current_year == check_year and current_month == check_month


def get_latest_week():
    """
    最近一周的时间点
    """
    date = datetime.now()
    ret_date = datetime.replace(date, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=-7)

    return ret_date


def get_latest_month():
    """
    最近一月的时间点
    """
    date = datetime.now()
    ret_date = datetime.replace(date, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=-30)

    return ret_date


def get_latest_n_days(n):
    """
    最近n天的时间点
    """
    date = datetime.now()
    ret_date = datetime.replace(date, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=-n)

    return ret_date


def get_next_n_days(n):
    """
    接下来的第n天
    """
    date = datetime.now()
    ret_date = datetime.replace(date, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=n)

    return ret_date

if __name__ == "__main__":
    print get_previous_month()

    print is_current_month(datetime.now().replace(year=2013))

    print get_next_n_days(7)