# coding: utf-8

import os
import sys
import math
import struct
import posix_ipc
from posix_ipc import Semaphore
from posix_ipc import SharedMemory as Memory


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    pids = []
    unit = n / 10
    sem_lock = Semaphore("/pi_sem_lock", flags=posix_ipc.O_CREX, initial_value=1)  # 使用一个信号量控制多个进程互斥访问共享内存
    memory = Memory("/pi_rw", size=8, flags=posix_ipc.O_CREX)
    os.lseek(memory.fd, 0, os.SEEK_SET)  # 初始化和为0.0的double值
    os.write(memory.fd, struct.pack('d', 0.0))
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            sem_lock.acquire()
            try:
                os.lseek(memory.fd, 0, os.SEEK_SET)
                bs = os.read(memory.fd, 8)  # 从共享内存读出来当前值
                cur_val, = struct.unpack('d', bs)  # 反序列化，逗号不能少
                cur_val += s  # 加上当前进程的计算结果
                bs = struct.pack('d', cur_val)  # 序列化
                os.lseek(memory.fd, 0, os.SEEK_SET)
                os.write(memory.fd, bs)  # 写进共享内存
                memory.close_fd()
            finally:
                sem_lock.release()
            sys.exit(0)  # 子进程结束
    sums = []
    for pid in pids:
        os.waitpid(pid, 0)  # 等待子进程结束
    os.lseek(memory.fd, 0, os.SEEK_SET)
    bs = os.read(memory.fd, 8)  # 读出最终这结果
    sums, = struct.unpack('d', bs)  # 反序列化
    memory.close_fd()  # 关闭共享内存
    memory.unlink()  # 销毁共享内存
    sem_lock.unlink()  # 销毁信号量
    return math.sqrt(sums * 8)


print pi(10000000)

# output for macOS, should be run on Linux
# (.venv) Franks-Mac:inter-process-communication frank$ python shared_memory.py
# Traceback (most recent call last):
#   File "shared_memory.py", line 59, in <module>
#     print pi(10000000)
#   File "shared_memory.py", line 24, in pi
#     os.lseek(memory.fd, 0, os.SEEK_SET)  # 初始化和为0.0的double值
# OSError: [Errno 29] Illegal seek