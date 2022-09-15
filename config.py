#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 15:04
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : config.py
@Describe: 配置文件
@License : myself learn
"""
"""存储 JWT 信息"""
SECRET_KEY = "fa297b07fec5840c07ed5361b22cadca02e5180a360f8f293ddbd8087a874c06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


"""存储数据库环境字段"""
EVENT = "test"


"""测试服链接数据库的字段"""
# *************mysql***********
testHost = "127.0.0.1"
testPort = 3306
testUserName = "root"
testPassWord = "123456"
testDB = 'fastLearn'

# *************redis***********
testRedisHost='127.0.0.1'  #redis配置
testRedisPort='6379'#redis端口
testRedisDB='0'

"""生产服链接数据库的字段"""
# *************mysql***********
prodHost = "127.0.0.1"
prodPort = 3306
prodUserName = "root"
prodPassWord = ""
prodDB = ''

# *************redis***********
prodRedisHost='127.0.0.1'  #redis配置
prodRedisPort='6379'#redis端口
prodRedisDB='0'