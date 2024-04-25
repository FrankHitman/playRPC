# coding: utf-8
# kill.py

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
    os.kill(pid, signal.SIGKILL)
    time.sleep(5)  # 父进程继续休眠5s观察子进程是否还有输出

# output
# (.venv) Franks-Mac:multiple-process frank$ python kill_by_signal.py
# in father process
# in child process
# in child process
# in child process
# in child process
# in child process
# (.venv) Franks-Mac:multiple-process frank$ ps -ef|grep python
#   501  5275  6197   0 Fri04PM ??        30:59.08 /Users/frank/play/playRPC/.venv/bin/python /Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/pydevconsole.py --mode=client --host=127.0.0.1 --port=60115
#   501  2650 92663   0 Thu09PM ttys011    0:00.05 python play_signal.py
#   501 25261 92663   0  6:36AM ttys011    0:00.01 grep -G python