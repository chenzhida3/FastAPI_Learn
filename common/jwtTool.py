#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/15 18:12
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : jwtTool.py
@Describe: 生成JWT token
@License : myself learn
"""
from jose import jwt
from config import *

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWT_tool:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """密码哈希"""
        return pwd_context.hash(password)