# coding: utf-8

import os
import sys
import math


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    childs = []
    unit = n / 10
    fifo_path = "/tmp/fifo_pi"
    os.mkfifo(fifo_path)  # 创建named pipe
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            with open(fifo_path, "w") as ff:
                ff.write(str(s) + "\n")
            sys.exit(0)  # 子进程结束
    sums = []
    while True:
        with open(fifo_path, "r") as ff:
            # 子进程关闭写端，读进程会收到eof
            # 所以必须循环打开，多次读取
            # 读够数量了就可以结束循环了
            sums.extend([float(x) for x in ff.read(1024).strip().split("\n")])
            if len(sums) == len(childs):
                break
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    os.unlink(fifo_path)  # 移除named pipe
    return math.sqrt(sum(sums) * 8)


print pi(10000000)

# output
# (.venv) Franks-Mac:inter-process-communication frank$ python named_pipe_fifo.py
# 3.14159262176
