#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 15:50
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : prod_database.py
@Describe: 生产服数据库链接配置
@License : myself learn
"""
from config import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''数据库url固定写法'''
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+prodUserName+":"+prodPassWord+"@"+str(prodHost)+":"+str(prodPort)+"/"+prodDB
'''创建引擎'''
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True)
'''创建数据库会话'''
ProdSessionLocal = sessionmaker(autoflush=False, bind=engine)
'''声明基类'''
Base = declarative_base()