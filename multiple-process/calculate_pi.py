# coding: utf-8

import os
import sys
import math
import redis


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    client = redis.StrictRedis(host='127.0.0.1', port=6379, password='your password')
    client.delete("result")  # 保证结果集是干净的
    del client  # 关闭连接
    for i in range(10):  # 分10个子进程
        mink = unit * i  # 每个子进程负责一个区间段的计算
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            client = redis.StrictRedis(host='127.0.0.1', port=6379, password='your password')
            client.rpush("result", str(s))  # 传递子进程结果
            sys.exit(0)  # 子进程结束
    for pid in pids:
        os.waitpid(pid, 0)  # 等待子进程结束
    sum = 0
    client = redis.StrictRedis(password='your password')
    for s in client.lrange("result", 0, -1):
        sum += float(s)  # 收集子进程计算结果
    return math.sqrt(sum * 8)


print pi(10000000)

# output
# (.venv) Franks-Mac:multiple-process frank$ python calculate_pi.py
# 3.14159262176