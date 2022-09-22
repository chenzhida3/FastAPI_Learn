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
from fastapi import FastAPI, Request, Query
from routers.user import usersRouter
import aioredis
import uvicorn
from config import *
app = FastAPI()


async def redis_pool():
    if EVENT == "test":
        redis = aioredis.from_url("redis://:@"+testRedisHost+":"+testRedisPort+"/"+testRedisDB,
                                  encoding="utf-8", decode_responses=True)
    else:
        redis = aioredis.from_url("redis://:@" + prodRedisHost + ":" + prodRedisPort + "/" + prodRedisDB,
                                  encoding="utf-8", decode_responses=True)
    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


app.include_router(usersRouter, prefix="/user", tags=['users'])


if __name__ == '__main__':

    uvicorn.run(app='main:app', host="127.0.0.1", port=8000)