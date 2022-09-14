#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 17:09
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : configLog.py
@Describe: 配置log
@License : myself learn
"""
import logging
import filepath  # 存放各类文件的位置


class Logger:
    def __init__(self, logger):
        # 创建一个logger，并设置日志级别
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        log_name = filepath.get_filePath(filepath.log_path, '.log')
        fh = logging.FileHandler(log_name, encoding='utf-8')
        fh.setLevel(logging.INFO)
        #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志，解决重复打印的问题
        if not self.logger.handlers:
            # 创建一个handler,用于输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)

            # 定义handler的输出格式
            formatter = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(name)s - %(funcName)s:%(lineno)d => %(message)s')
            fh.setFormatter(formatter)
            sh.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(sh)

    def getLog(self):
        return self.logger
