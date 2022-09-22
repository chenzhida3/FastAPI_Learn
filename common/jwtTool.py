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
import traceback

from starlette import status

from models.get_db import get_db
from jose import jwt, JWTError
from models.crud import *
from config import *
from fastapi import Request, Depends, HTTPException, Header
from passlib.context import CryptContext
from common.configLog import Logger
logger = Logger('common.jwtTool').getLog()
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

    @staticmethod
    async def get_cure_user(request: Request, token: Optional[str] = Header(...),
                            db: Session = Depends(get_db)) -> UsernameRole:
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='验证失败')
        credentials_for_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='用户未登录或者登录的token已失效')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise credentials_exception
            user_redis_token = await request.app.state.redis.get(username+"_token")
            if not user_redis_token or user_redis_token != token:
                raise credentials_for_exception
            userRole = get_role_name(db, get_user_username(db, username).role).name
            user = UsernameRole(username=username, role=userRole)
            return user
        except JWTError as e:
            logger.error(e)
            raise credentials_exception

