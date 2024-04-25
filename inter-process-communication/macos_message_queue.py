# coding: utf-8

import os
import sys
import math
import sysv_ipc
from sysv_ipc import MessageQueue as Queue


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    q = Queue(key=None, flags=sysv_ipc.IPC_CREX)
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            q.send(str(s))  # 把结果发送到消息队列里面，不需要加锁
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        sums.append(float(q.receive()[0]))
        os.waitpid(pid, 0)  # 等待子进程结束
    q.remove()  # 销毁消息队列
    return math.sqrt(sum(sums) * 8)


print pi(10000000)

# 从上面可以看出消息队列是进程读写安全的，不需要额外加锁
# output
# (.venv) Franks-Mac:inter-process-communication frank$ python macos_message_queue.py
# 3.14159262176
