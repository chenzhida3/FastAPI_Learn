#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 17:10
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : filepath.py
@Describe: 文件路径统一管理
@License : myself learn
"""
import os
import time

pro_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前项目目录

'''一级目录'''
common_path = os.path.join(pro_path, 'common')  # 通用文件目录
log_path = os.path.join(pro_path, 'logs')    # 日志文件


def get_filePath(file_path, file_type):
    """
    :param file_path: 文件路径
    :param file_type: 文件类型
    :return:
    """
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%H_%M_%S', time.localtime(time.time()))
    filePaht = os.path.join(file_path, day)
    if not os.path.exists(filePaht):
        os.mkdir(filePaht)
    file_name = os.path.join(filePaht, now+file_type)
    return file_name

if __name__ == '__main__':
    print(get_filePath(log_path, '12.log'))