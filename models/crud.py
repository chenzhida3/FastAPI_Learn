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

def db_get_course_id(db: Session, id: int):
    """根据id查找课程详情"""
    return db.query(Course).filter(Course.id == id, Course.status == False).first()

def db_get_coursecomment_id(db:Session, course_id: int):
    """根据课程id获取所有评论"""
    return db.query(Commentcourse).filter(Commentcourse.course == course_id, Commentcourse.status == False).all()

def createcomments(db: Session, cousecoment: Coursecomment, user: id):
    """添加评论"""
    comment = Commentcourse(**cousecoment.dict())
    comment.users = user
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_cousecomments(db: Session, id: int):
    """根据课程id获取评论"""
    return db.query(Commentcourse).filter(Commentcourse.id == id, Commentcourse.status == False).all()

def get_student(db: Session, couese: int, user:int):
    """根据课程id和学生id获取数据"""
    return db.query(Studentcourse).filter(Studentcourse.course == couese, Studentcourse.students == user, Studentcourse.status==False).first()

def add_student_course(db: Session, couese: int, user:int):
    """添加学生课程信息"""
    studentcourse = Studentcourse(students=user, course=couese)
    db.add(studentcourse)
    db.commit()
    db.refresh(studentcourse)
    return studentcourse

def get_student_all(db: Session, student:int):
    """返回指定学生的所有课程"""
    return db.query(Studentcourse).filter(Studentcourse.students == student, Studentcourse.status == False).all()

def get_course_all(db:Session):
    """返回所有课程"""
    return db.query(Course).filter(Course.status==False).all()