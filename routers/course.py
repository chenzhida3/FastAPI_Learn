#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2023/5/30 17:27
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : course.py
@Describe: 课程接口
@License : myself learn
"""
from fastapi import APIRouter, Depends, Request
from models.crud import *
from models.get_db import get_db
from common.jwtTool import *
from common.jsontools import *
from fastapi.encoders import jsonable_encoder
from common.configLog import Logger
from config import *
logger = Logger('routers.courese').getLog()

courseRouter = APIRouter()

@courseRouter.post(path="/create")
async def create(course: Courses, db: Session = Depends(get_db), user: UsernameRole=Depends(JWT_tool.get_cure_user)):
    """创建课程接口"""
    user_ = get_user_username(db=db, username=user.username)
    user_role = get_role_name(db=db, id=user_.role)
    if not user_role or user_role.name == '学生':
        return resp_200(code=101004, message="只有老师才能创建课程", data={})
    if len(course.name) < 2 or len(course.name)>51:
        return resp_200(code=101005, message='课程长度应该在2-50', data={})
    # 创建的课程名字不能重复=
    courese_name = db_get_courese_name(db=db, name=course.name)
    if courese_name:
        return resp_200(code=101002, message="课程名称不能重复", data={})
    couse = db_create_course(db=db, course=course, user=user_.id)
    return resp_200(code=200, message="创建成功", data=jsonable_encoder(couse))

@courseRouter.get(path='/detail/{id}')
async def detail(id: int, db: Session = Depends(get_db)):
    """课程详情接口"""
    course = db_get_course_id(db=db, id=id)
    if course:
        # 如果有课程详情，拼接课程评论
        course_detail = CousesDetail(id=course.id,
                                    name=course.name,
                                    icon=course.icon, desc=course.desc, catalog=course.catalog,
                                    onsale=course.onsale, owner=get_user(db, course.owner).username,
                                    likenum=course.likenum)
        comment = db_get_coursecomment_id(db=db, course_id=course.id)
        all = []
        if len(comment)>0:
            for item in comment:
                detailcomment = Coursescomment(id=item.id,top=item.top,
                                               user=get_user(db, item.users).username,
                                               pid=item.id, addtime=str(item.addtime),
                                               context=item.context)
                all.append(detailcomment)
        course_detail.commonet = all
        return resp_200(code=200, message="success", data=jsonable_encoder(course_detail))    
    return resp_200(code=200, message="success", data={})

@courseRouter.put(path='/edit')
async def edit(course: CoursesEdit, db: Session = Depends(get_db), user: UsernameRole = Depends(JWT_tool.get_cure_user)):
    """编辑课程接口"""
    users = get_user_username(db=db, username=user.username)
    courses_is = db_get_course_id(db=db, id=course.id)
    if not courses_is:
        # 如果课程不存在
        return resp_200(code=101201, message='success', data={"msg":"课程不存在"})
    course_name = db_get_courese_name(db=db, name=course.name)
    if course_name:
        # 课程名称重复
        return resp_200(code=101203, message='success', data={"msg":"无法编辑重复名称"})
    if courses_is.owner == users.id:
        courses_is.catalog = course.catalog
        courses_is.desc = course.desc
        courses_is.icon = course.icon
        courses_is.name = course.name
        db.commit()
        db.refresh(courses_is)
        return resp_200(code=200, message="success", data=jsonable_encoder(courses_is))
    return resp_200(code=101202, message='success', data={"msg":"权限不足"})

@courseRouter.get(path="/viewcomment/{id}")
async def viewcomment(id: int, db: Session=Depends(get_db)):
    """课程评论接口"""
    course = db_get_course_id(db=db, id=id)
    if course:
        comment = db_get_coursecomment_id(db=db, course_id=course.id)
        all = []
        if len(comment)>0:
            for item in comment:
               detailcomment = Coursescomment(id=item.id,top=item.top,
                                               user=get_user(db, item.users).username,
                                               pid=item.id, addtime=str(item.addtime),
                                               context=item.context)
               all.append(detailcomment)
            return resp_200(code=200, message="success", data=jsonable_encoder(all))
    return resp_200(code=101301, message="success", data={"msg":"课程不存在"})

@courseRouter.post(path="/comments")
async def comments(comment: Coursecomment, user: UsernameRole = Depends(JWT_tool.get_cure_user), 
                   db: Session = Depends(get_db)):
    """添加评论接口"""
    if comment.comments == '':
        return resp_200(code=101402, message="success", data={"msg":"评论内容不能为空"})
    users = get_user_username(db, user.username)
    courses = db_get_course_id(db, comment.id)
    if courses:
        if courses.owner == users.id:
            return resp_200(code=101404, message="success", data={"msg":"自己不能评论自己的课程"})
        if comment.pid is not None:
            pid_course = get_cousecomments(db, comment.pid)
            if pid_course:
                createcomments(db=db, cousecoment=comment, user=users.id)
                return resp_200(code=101405, message="success", data={"msg":"success"})
            return resp_200(code=101405, message="success", data={"msg":"回复的评论不存在"})
        createcomments(db=db, cousecoment=comment, user=users.id)
        return resp_200(code=101405, message="success", data={"msg":"success"})
    return resp_200(code=101401, message="success", data={"msg":"课程id不存在"})

@courseRouter.post(path='/add/{id}')
async def add(id: int, db: Session = Depends(get_db), user: UsernameRole = Depends(JWT_tool.get_cure_user)):
    """添加学生课程接口"""
    users = get_user_username(db=db, username=user.username)
    if user.role == '教师':
        return resp_200(code=101503, message='success', data={'msg':"老师不能加入课程"})
    couses = db_get_course_id(db=db, id=id)
    if not couses:
        return resp_200(code=101501, message='success', data={'msg':"课程id不存在"})
    student = get_student(db=db, couese=id, user=users.id)
    if student:
        return resp_200(code=101502, message='success', data={'msg':"课程不能重复加入"})
    res = add_student_course(db=db, couese=couses.id, user=users.id)
    return resp_200(code=200, message='success', data={'msg':"添加成功",
                                                       "data":jsonable_encoder(res)})

@courseRouter.post(path='/quit/{id}')
async def quit(id: int, db: Session = Depends(get_db), user: UsernameRole = Depends(JWT_tool.get_cure_user)):
    """退出学生课程接口"""
    users = get_user_username(db=db, username=user.username)
    if user.role == '教师':
        return resp_200(code=101603, message='success', data={'msg':"老师不能退出课程"})
    couses = db_get_course_id(db=db, id=id)
    if not couses:
        return resp_200(code=101601, message='success', data={'msg':"课程id不存在"})
    student = get_student(db=db, couese=id, user=users.id)
    if student:
        student.status = True
        db.commit()
        db.refresh(student)
        return resp_200(code=200, message='success', data={'msg':"退出课程成功"})
    return resp_200(code=101602, message='success', data={'msg':"课程不在自己的列表"})

@courseRouter.get("/list")
async def courselist(db:Session=Depends(get_db)):
    """返回所有课程接口""" 
    all_course = get_course_all(db=db)
    allCourse = []
    if len(all_course) > 0:
        for item in all_course:
            coursedetail = CousesDetail(id=item.id,
                                        name=item.name,
                                        icon=item.icon, desc=item.desc, catalog=item.catalog,
                                        onsale=item.onsale, owner=get_user(db, item.owner).username,
                                        likenum=item.likenum)
            allCourse.append(coursedetail)
        return resp_200(code=200, message='success', data=jsonable_encoder(allCourse))
    return resp_200(code=101701, message='success', data={'msg':"无课程信息"})

@courseRouter.get(path='/student/course_list')
async def studentCourseList(db: Session = Depends(get_db), user: UsernameRole = Depends(JWT_tool.get_cure_user)):
    """返回学生参加的所有课程"""
    users = get_user_username(db=db, username=user.username)
    if user.role == '教师':
        return resp_200(code=101803, message='success', data={'msg':"老师不能参加课程"})
    student_all = get_student_all(db=db, student=users.id)
    all = []
    if len(student_all)> 0:
        for item in student_all:
            course = db_get_course_id(db, item.course)
            coursedetail = CousesDetail(id=course.id,
                                        name=course.name,
                                        icon=course.icon, desc=course.desc, catalog=course.catalog,
                                        onsale=course.onsale, owner=get_user(db, course.owner).username,
                                        likenum=course.likenum)
            all.append(coursedetail)
        return resp_200(code=200, message='success', data=jsonable_encoder(all))
    return resp_200(code=101801, message='success', data={'msg':"无学生课程信息"})

@courseRouter.post(path='/like/{id}')
async def like(request: Request, id: int, db: Session = Depends(get_db), user: UsernameRole = Depends(JWT_tool.get_cure_user)):
    """点赞课程"""
    course = db_get_course_id(db=db, id=id)
    if not course:
        return resp_200(code=102001, message='success', data={'msg':"课程不存在"})
    result = await request.app.state.redis.hgetall(str(course.id)+"_like")
    if user.username in result.keys():
        return resp_200(code=102002, message='success', data={'msg':"已经点赞，不能重复点赞"})
    username ={user.username:1}
    await request.app.state.redis.hmset(str(course.id)+"_like", username)
    course.likenum += 1
    db.commit()
    db.refresh(course)
    return resp_200(code=200, message='success', data=jsonable_encoder(course))


@courseRouter.post(path='/onsale')
async def onsale(sale: onsaleModel, user: UsernameRole = Depends(JWT_tool.get_cure_user), db: Session = Depends(get_db)):
    """课程上下架"""
    users = get_user_username(db, user.username)
    if user.role != '教师':
        return resp_200(code=102104, message='success', data={'msg':"学生没有权限"})
    course = db_get_course_id(db=db, id=sale.id)
    if not course:
        return resp_200(code=102103, message='success', data={'msg':"课程不存在"})
    if course.onsale is sale.onsale:
        return resp_200(code=102102, message='success', data={'msg':"课程的onsale已是"+str(sale.onsale)})
    if course.owner != users.id:
        return resp_200(code=102103, message='success', data={'msg':"只能操作自己的课程"})
    course.onsale = sale.onsale
    db.commit()
    db.refresh(course)
    return resp_200(code=200, message='success', data=jsonable_encoder(course))