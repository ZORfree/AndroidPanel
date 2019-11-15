#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   socket.py
@Contact :   haruihi@163.com Zorfree
@License :   (C)Copyright 2017-2019, MIT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/13 20:01   Zorfree      1.0         None
'''
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    REPORT_UPLOAD_PATH = os.path.join(basedir, 'reports')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    QA_SCORE = 70
    QA_CPUAVERAGE = 17
    QA_CPUMAX = 50
    QA_PSSAVERAGE = 62000000
    QA_PSSMAX = 85000000
    QA_DOWNT = None
    QA_UPT = None
    QA_READT = None
    QA_WRITET = None
    CPUAVERAGE_PERCENT = 3.5
    CPUMAX_PERCENT = 3.5
    PSSAVERAGE_PERCENT = 35
    PSSMAX_PERCENT = 14
    DOWNT_PERCENT = 3.5
    UPT_PERCENT = 03.5
    READT_PERCENT = 3.5
    WRITET_PERCENT = 3.5


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'data.db')
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
