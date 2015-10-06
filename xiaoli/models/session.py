#!/usr/bin/env python
# -*- coding:utf-8 -*-
import contextlib
from sqlalchemy.orm import sessionmaker
from xiaoli.models.base import engine

__author__ = 'zouyingjun'

Session = sessionmaker(bind=engine)


@contextlib.contextmanager
def db_session_cm():
    session = Session()
    try:
        yield session
    except Exception, e:
        # logger.warn(traceback.format_exc())
        raise e
    finally:
        session.close()