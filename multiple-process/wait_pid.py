# coding: utf-8

import os
import time
import signal


def create_child():
    pid = os.fork()
    if pid > 0:
        return pid
    elif pid == 0:
        return 0
    else:
        raise


pid = create_child()
if pid == 0:
    while True:  # 子进程死循环打印字符串
        print 'in child process'
        time.sleep(1)
else:
    print 'in father process'
    time.sleep(5)  # 父进程休眠5s再杀死子进程
    # os.kill(pid, signal.SIGTERM)  # (25367, 15)
    os.kill(pid, signal.SIGKILL)  # (25533, 9)
    ret = os.waitpid(pid, 0)  # 收割子进程
    print ret  # 看看到底返回了什么
    time.sleep(5)  # 父进程继续休眠5s观察子进程是否还存在

# output
# (.venv) Franks-Mac:multiple-process frank$ python wait_pid.py
# in father process
# in child process
# in child process
# in child process
# in child process
# in child process
# (25367, 15)
# (.venv) Franks-Mac:multiple-process frank$ ps -ef|grep python
#   501  5275  6197   0 Fri04PM ??        31:06.06 /Users/frank/play/playRPC/.venv/bin/python /Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/pydevconsole.py --mode=client --host=127.0.0.1 --port=60115
#   501  2650 92663   0 Thu09PM ttys011    0:00.05 python play_signal.py
#   501 25371 92663   0  6:49AM ttys011    0:00.01 grep -G python
# (25367, 15)中第二个数字通常的value是一个16位的整数值，前8位表示进程的退出状态，后8位表示导致进程退出的信号的整数值。
# 0000 0000 0000 1111， 15就是SIGTERM信号的整数值。

# 修改 kill signal 为 signal.SIGKILL 之后的输出
# (.venv) Franks-Mac:multiple-process frank$ python wait_pid.py
# in father process
# in child process
# in child process
# in child process
# in child process
# in child process
# in child process
# (25533, 9)