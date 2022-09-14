#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 18:27
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : user.py
@Describe: 用户接口
@License : myself learn
"""
from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from models.get_db import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import *
from common.jsontools import *
from models.crud import *
from common.configLog import Logger
logger = Logger('routers.user').getLog()

usersRouter = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# 新建用户
@usersRouter.post("/create", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("创建用户")
    if len(user.username) < 2 or len(user.username) > 16:
        return resp_200(code=100106, message="用户名长度应该是2-16位", data="")
    if user.age < 18:
        return resp_200(code=100103, message="年纪大小不符合", data="")
    if (user.role == 1 and user.studentnum is None) or (user.role == 2 and user.jobnum is None) or (
            user.role not in [1, 2]):
        return resp_200(code=100102, message="身份和对应号不匹配", data="")
    db_crest = get_user_username(db, user.username)
    if db_crest:
        return resp_200(code=100104, message="用户名重复", data="")
    try:
        user.password = get_password_hash(user.password)
    except Exception as e:
        logger.exception(e)
        return resp_200(code=100105, data="", message="密码加密失败")
    try:
        user = db_create_user(db=db, user=user)
        logger.info("创建用户成功")
        return resp_200(code=200, data={'user': user.username}, message="success")
    except Exception as e:
        logger.exception(e)
        return resp_200(code=100101, data="", message="注册失败")
