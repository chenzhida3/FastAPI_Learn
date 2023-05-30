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
from sqlalchemy import and_, or_
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


def get_message(db: Session, id: int):
    return db.query(Message).filter(Message.id == id, Message.status == False).first()


def get_pid_message(db: Session, message: int):
    return db.query(Message).filter(and_(Message.id != message, Message.pid == message, Message.status == False)).all()


def get_message_list(db: Session, userId: int):
    return db.query(Message).filter(or_(Message.senduser == userId, Message.acceptusers == userId,
                                        Message.status == 0)).all()


def db_create_rebackMessage(db: Session, reback: RebackMessageConnet, sendUser: int):
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    reback = Message(pid=reback.userId, context=reback.connect)
    reback.sendtime = times
    reback.senduser = sendUser
    db.add(reback)
    db.commit()
    db.refresh(reback)
    return reback

def db_create_course(db: Session, course: Courses, user:int):
    """创建课程"""
    course = Course(**course.dict())
    course.owner = user
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def db_get_courese_name(db: Session, name:str):
    """根据课程名称查找数据库"""
    return db.query(Course).filter(Course.name == name, Course.status == False).first()

