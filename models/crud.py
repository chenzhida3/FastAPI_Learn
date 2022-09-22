#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 17:46
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : crud.py
@Describe: 数据库操作
@License : myself learn
"""
from sqlalchemy.orm import Session
from models.schemas import *
from models.model import *


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.status == False).first()


def db_create_user(db: Session, user: UserCreate):
    """新建用户"""
    roles = db.query(Role).filter(Role.id == user.role).first()
    db_user = User(**user.dict())
    db_user.role = roles.id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # 刷新
    return db_user


def get_user_username(db: Session, username: str):
    return db.query(User).filter(User.username == username, User.status == False).first()


def get_role_name(db: Session, id: id):
    return db.query(Role).filter(Role.id == id).first()