#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 15:16
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : test_database.py
@Describe: 测试环境的数据库配置
@License : myself learn
"""
from config import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''数据库url固定写法'''
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+testUserName+":"+testPassWord+"@"+str(testHost)+":"+str(testPort)+"/"+testDB
'''创建引擎'''
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True)
'''创建数据库会话'''
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
'''声明基类'''
Base = declarative_base()
