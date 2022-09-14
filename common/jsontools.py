#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 17:14
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : jsontools.py
@Describe: json统一处理工具
@License : myself learn
"""
from fastapi import status
from fastapi.responses import Response, JSONResponse
from typing import Union


def resp_200(*, code=200, data: Union[list, dict, str], message="Success") -> Response:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            'code': code,
                            'message': message,
                            'data': data
                        })


def resp_400(*, data: str = None, message: str = "Bad Request") -> Response:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            'code': 400,
                            'message': message,
                            'data': data
                        })