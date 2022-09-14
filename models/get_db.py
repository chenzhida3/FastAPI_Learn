#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 16:26
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : get_db.py
@Describe: 链接数据库
@License : myself learn
"""
from models import TestingSessionLocal, ProdSessionLocal
from config import EVENT


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_prod_db():
    db = ProdSessionLocal()
    try:
        yield db
    finally:
        db.close()


if EVENT == "test":
    get_db = get_test_db
else:
    get_db = get_prod_db
