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
from fastapi import APIRouter, Request, Depends, HTTPException, Header, Body
from fastapi.encoders import jsonable_encoder
from models.get_db import get_db
from common.jsontools import *
from models.crud import *
from common.jwtTool import JWT_tool
from common.configLog import Logger
from config import *
logger = Logger('routers.user').getLog()

usersRouter = APIRouter()


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
        user.password = JWT_tool.get_password_hash(user.password)
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


# 登录接口
@usersRouter.post("/login")
async def user_login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    get_db_user = get_user_username(db, user.username)
    if not get_db_user:
        logger.info('登录的用户不存在')
        return resp_200(code=100205, message='用户不存在', data="")
    verifypassowrd = JWT_tool.verify_password(user.password, get_db_user.password)
    if verifypassowrd:  # 如果密码校验通过
        user_redis_token = await request.app.state.redis.get(user.username+'_token')
        if not user_redis_token:
            try:
                token = JWT_tool.create_access_token(data={"sub": user.username})
            except Exception as e:
                logger.exception(e)
                return resp_200(code=100203, message='产生token失败', data={})
            await request.app.state.redis.set(user.username+'_token', token)
            await request.app.state.redis.expire(user.username+'_token', ACCESS_TOKEN_EXPIRE_SECOND)
            return resp_200(code=200, message='成功', data={"username": user.username, "token": token})
        return resp_200(code=100202, message='成功', data={"username": user.username, "token": user_redis_token})
    else:
        result = await request.app.state.redis.hgetall(user.username+"_password")
        if not result:
            time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            res = {"num": "0", "time": time}
            await request.app.state.redis.hmset(user.username+"_password", res)
        else:
            errornum = int(result['num'])
            numtime = (datetime.now() - datetime.strptime(result['time'], '%Y-%m-%d %H:%M:%S')).seconds / 60
            if errornum<5 and numtime<30:
                # 更新错误次数
                errornum += 1
                await request.app.state.redis.hset(user.username+"_password", key='num', value=errornum)
                if errornum < 5:
                    return resp_200(code=100206, message='密码错误', data={'message': f'您还有{5-errornum}次机会，超过将锁定账号30分钟'})
                else:
                    return resp_200(code=100204, message='密码错误', data={'message': '输入密码错误次数过多，账号暂时锁定，请30min再来登录'})
            elif errornum<5 and numtime>30:
                # 次数置1，时间设置现在时间
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                res = {"num": errornum, "time": times}
                await request.app.state.redis.hmset(user.username + "_password", res)
                return resp_200(code=100206, data={'message': f'您还有{5-errornum}次机会，超过将锁定账号30分钟'}, message='密码错误')
            elif errornum >= 5 and numtime < 30:
                # 次数设置成最大，返回
                errornum += 1
                await request.app.state.redis.hset(user.username + "_password", key='num', value=errornum)
                return resp_200(code=100204, message='密码错误', data={'message': '输入密码错误次数过多，账号暂时锁定，请30min再来登录'})
            else:
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                res = {"num": errornum, "time": times}
                await request.app.state.redis.hmset(user.username + "_password", res)
                return resp_200(code=100206, data={'message': f'您还有{5-errornum}次机会，超过将锁定账号30分钟'}, message='密码错误')


# 获取个人信息接口
@usersRouter.get('/info', response_model=UserBase)
async def userInfo(user: UsernameRole = Depends(JWT_tool.get_cure_user), db: Session = Depends(get_db)):
    user_name = get_user_username(db, username=user.username)
    data = {'username': user_name.username, 'sex': user_name.sex, 'age': user_name.age}
    user_role = get_role_name(db, user_name.role)
    if user_role.name == '学生':
        data['studentnum'] = user_name.studentnum
    else:
        data['jobnum'] = user_name.jobnum
    return resp_200(code=200, message='成功', data=data)


# 修改密码接口
@usersRouter.post('/changePwd')
async def changePassword(request: Request, userChangePwd: UserChangePassword,
                         user: UsernameRole = Depends(JWT_tool.get_cure_user), db: Session = Depends(get_db)):
    if userChangePwd.password == userChangePwd.newPassword:
        return resp_200(code=100304, message='新旧密码不能一样', data={})
    if len(userChangePwd.newPassword)<6 or len(userChangePwd.newPassword)>16:
        return resp_200(code=100303, message='新密码长度不匹配', data={})
    username = user.username
    user_name_db = get_user_username(db, username)
    verify = JWT_tool.verify_password(userChangePwd.password, user_name_db.password)
    if verify:
        # 旧密码校验通过
        hashpassword = JWT_tool.get_password_hash(userChangePwd.newPassword)
        user_name_db.password = hashpassword
        try:
            db.commit()
            db.refresh(user_name_db)
        except Exception as e:
            logger.exception(e)
            return resp_200(code=100302, message='密码保存失败', data={})
        # 删除旧redis数据
        await request.app.state.redis.delete(user.username+"_password")
        await request.app.state.redis.delete(user.username+"_token")
        return resp_200(code=200, message="成功", data={"username": user.username, "message": "修改密码成功"})
    return resp_200(code=100301, message='旧密码校验失败', data={})


# 添加留言接口
@usersRouter.post(path='/addMsg')
async def addMessage(message: MessageConnect, user: UsernameRole = Depends(JWT_tool.get_cure_user),
                     db: Session = Depends(get_db)):
    if len(message.connect)>300 or len(message.connect)<5:
        return resp_200(code=100502, message='留言文案长度在5-300个字符', data={})
    user_name = get_user_username(db, user.username)
    rev_user = get_user(db, message.userId)
    if not rev_user:
        return resp_200(code=100503, message='留言的用户不存在', data={})
    if rev_user.id == user_name.id:
        return resp_200(code=100501, message='不能给自己留言', data={})
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    connect = Message(senduser=user_name.id, acceptusers=rev_user.id,
                      context=message.connect, sendtime=times, addtime=times, read=False)
    db.add(connect)
    db.commit()
    db.refresh(connect)
    return resp_200(code=200, message='成功', data={})


# 查看留言接口
@usersRouter.get(path='/msg')
async def viewMessage(id: int, user: UsernameRole=Depends(JWT_tool.get_cure_user), db: Session=Depends(get_db)):
    useris = get_user_username(db, user.username)
    message =get_message(db, id)
    if not message:
        return resp_200(code=100601, message='留言不存在', data={})
    if message.acceptusers != useris.id and message.senduser != useris.id:
        return resp_200(code=100602, message='权限不足,无法查看与自己无关的留言', data={})
    message.read = True
    db.commit()
    db.refresh(message)

    all_pid = get_pid_message(db, message.id)
    messageone = MessageOne(id=message.id,
                            senduser=get_user(db, message.senduser).username,
                            acceptusers=get_user(db, message.acceptusers).username,
                            read=message.read,
                            sendtime=message.sendtime,
                            addtime=str(message.addtime),
                            context=message.context)
    if len(all_pid)>0:
        allPid_list = []
        for item in all_pid:
            message = MessagePid(id=message.id,
                                 senduser=get_user(db, item.senduser).username,
                                 acceptusers=get_user(db, item.acceptusers).username,
                                 read=item.read,
                                 sendtime=item.sendtime,
                                 addtime=str(item.addtime),
                                 context=item.context, pid=item.pid)
            allPid_list.append(message)
        message.pid = allPid_list
    return resp_200(code=200, message='成功', data=jsonable_encoder(messageone))


# 留言列表接口
@usersRouter.get(path='/msg_list')
async def message_list(user: UsernameRole = Depends(JWT_tool.get_cure_user), db: Session = Depends(get_db)):
    users = get_user_username(db, user.username)
    msgList = get_message_list(db, users.id)
    msg_list = []
    mainMsg = []
    if len(msgList) > 0:
        for item in msgList:
            if not item.pid:
                messageOne = Message(id=item.id,
                                     senduser=get_user(db, item.senduser).username,
                                     acceptusers=get_user(db, item.acceptusers).username,
                                     read=item.read,
                                     sendtime=item.sendtime,
                                     addtime=str(item.addtime),
                                     context=item.context)
                mainMsg.append(messageOne.id)
                all_pid = get_pid_message(db, item.id)
                if len(all_pid) > 0:
                    all_pid_list = []
                    for items in all_pid:
                        message = MessagePid(id=items.id,
                                             senduser=get_user(db, items.senduser).username,
                                             acceptusers=get_user(db, items.acceptusers).username,
                                             read=items.read,
                                             sendtime=items.sendtime,
                                             addtime=str(items.addtime),
                                             context=items.context,
                                             pid=items.pid)
                        all_pid_list.append(message)
                    messageOne.pid = all_pid_list
                msg_list.append(messageOne)
            else:
                if item.pid not in mainMsg:
                    message = get_message(db, item.pid)
                    if message:
                        all_pid = get_pid_message(db, message.id)
                        messageone = MessageOne(id=message.id,
                                                senduser=get_user(db, message.senduser).username,
                                                acceptusers=get_user(db, message.acceptusers).username,
                                                read=message.read,
                                                sendtime=message.sendtime,
                                                addtime=str(message.addtime),
                                                context=message.context)
                        if len(all_pid) > 0:
                            allpidlist = []
                            for item in all_pid:
                                messagepid = MessagePid(id=message.id,
                                                        senduser=get_user(db, item.senduser).username,
                                                        acceptusers=get_user(db, item.acceptusers).username,
                                                        read=item.read,
                                                        sendtime=item.sendtime,
                                                        addtime=str(item.addtime),
                                                        context=item.context, pid=item.pid)
                                allpidlist.append(messagepid)
                            messageone.pid = allpidlist
                        msg_list.append(messageone)
    return resp_200(code=200, message='成功', data=jsonable_encoder(msg_list))

# 回复留言接口
@usersRouter.post(path='/rebackmessage')
async def rebackmessage(rebackmessage: RebackMessageConnet, user: UsernameRole=Depends(JWT_tool.get_cure_user),
                        db: Session = Depends(get_db)):
    if rebackmessage.connect == '':
        return resp_200(code=100802, message='回复留言内容不能为空', data={"msg": '回复留言内容不能为空'})
    if len(rebackmessage.connect) > 500 or len(rebackmessage.connect) < 5:
        return resp_200(code=100803, message='回复内容应该在5', data={"msg": '回复内容应该在5'})
    users = get_user_username(db, user.username)
    message = get_message(db, rebackmessage.rebackId)
    if not message:
        return resp_200(code=100804, message='回复留言id不存在', data={"msg": '回复留言id不存在'})
    db_create_rebackMessage(db, rebackmessage, users.id)
    return resp_200(code=1000, message='成功', data={"msg": '成功'})

# 删除留言接口
@usersRouter.post(path='/deletemessage/{id}')
async def deletemessage(id: int, user: UsernameRole = Depends(JWT_tool.get_cure_user), db: Session = Depends(get_db)):
    message = get_message(db=db, id=id)
    if not message:
        return resp_200(code=100901, message='删除的留言不存在',data={})
    useris = get_user_username(db=db, username=user.username)
    if useris.id != message.acceptusers and useris.id != message.senduser:
        return resp_200(code=100902, message='权限不足', data={})
    message.status = 1
    db.commit()
    db.refresh(message)
    return resp_200(code=200, message='success', data={"message":'success'})













