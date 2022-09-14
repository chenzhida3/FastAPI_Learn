#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 15:04
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : main.py
@Describe:
@License : myself learn
"""
from fastapi import FastAPI
from routers.user import usersRouter
app = FastAPI()
app.include_router(usersRouter, prefix="/user", tags=['users'])


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)