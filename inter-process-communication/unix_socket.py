# coding: utf-8

import os
import sys
import math
import socket


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    server_address = "/tmp/pi_sock"  # 套接字对应的文件名
    childs = []
    unit = n / 10
    servsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  # 注意AF_UNIX表示「域套接字」
    servsock.bind(server_address)  # 监听的文件
    servsock.listen(10)  # 监听子进程连接请求
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            servsock.close()  # 子进程要关闭servsock引用
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(server_address)  # 连接父进程套接字
            s = slice(mink, maxk)  # 子进程开始计算
            sock.sendall(str(s))
            sock.close()  # 关闭连接
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in childs:
        conn, _ = servsock.accept()  # 接收子进程连接
        sums.append(float(conn.recv(1024)))
        conn.close()  # 关闭连接
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    servsock.close()  # 关闭套接字
    os.unlink(server_address)  # 移除套接字文件
    return math.sqrt(sum(sums) * 8)


print pi(10000000)

# output
# (.venv) Franks-Mac:inter-process-communication frank$ python unix_socket.py
# 3.14159262176