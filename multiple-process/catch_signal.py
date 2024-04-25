# coding: utf-8

import os
import time
import signal
import sys


def create_child():
    pid = os.fork()
    if pid > 0:
        return pid
    elif pid == 0:
        return 0
    else:
        raise

def i_will_die(sig_num, frame):  # 自定义信号处理函数
    print "child will die"
    sys.exit(0)


pid = create_child()
if pid == 0:
    # signal.signal(signal.SIGTERM, signal.SIG_IGN)  # SIG_IGN表示忽略信号，捕获退出信号并忽略
    signal.signal(signal.SIGTERM, i_will_die)
    while True:  # 子进程死循环打印字符串
        print 'in child process'
        time.sleep(1)
else:
    print 'in father process'
    time.sleep(5)  # 父进程休眠5s再杀死子进程
    os.kill(pid, signal.SIGTERM)  # 发一个SIGTERM信号
    time.sleep(5)  # 父进程继续休眠5s观察子进程是否还存在
    os.kill(pid, signal.SIGKILL)  # 发一个SIGKILL信号
    time.sleep(5)  # 父进程继续休眠5s观察子进程是否还存在

# output
# (.venv) Franks-Mac:multiple-process frank$ python catch_signal.py
# in father process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process

# output for i_will_die handler
# (.venv) Franks-Mac:multiple-process frank$ python catch_signal.py
# in father process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# child will die