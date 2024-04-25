# Python multiple process

## 杀死子进程
os.kill执行完之后，我们通过ps -ef|grep python快速观察进程的状态，可以发现子进程有一个奇怪的显示<defunct>（僵尸进程）
```
root        12     1  0 11:22 pts/0    00:00:00 python kill.py
root        13    12  0 11:22 pts/0    00:00:00 [python] <defunct>
```
子进程结束后，会立即成为僵尸进程，僵尸进程占用的操作系统资源并不会立即释放

run [kill by signal](kill_by_signal.py)

通过 signal.SIGKILL 信号杀死的 子进程 会变成僵尸进程，但是在 MacOS 上并没有发现。
```
(.venv) Franks-Mac:multiple-process frank$ python kill_by_signal.py 
in father process
in child process
in child process
in child process
in child process
in child process
(.venv) Franks-Mac:multiple-process frank$ ps -ef|grep python
  501  5275  6197   0 Fri04PM ??        30:59.08 /Users/frank/play/playRPC/.venv/bin/python /Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pydev/pydevconsole.py --mode=client --host=127.0.0.1 --port=60115
  501  2650 92663   0 Thu09PM ttys011    0:00.05 python play_signal.py
  501 25261 92663   0  6:36AM ttys011    0:00.01 grep -G python

```

## 收割子进程
收割子进程使用os.waitpid(pid, options)系统调用，
- 可以提供具体 pid 来收割指定子进程，
- 也可以通过参数 pid=-1 来收割任意子进程。
- options 如果是 0，就表示阻塞等待子进程结束才会返回，
- options 如果是 WNOHANG 就表示非阻塞，有,就返回指定进程的 pid，没有,就返回 0。
- 如果指定 pid 进程不存在或者没有子进程可以收割，就会抛出 OSError(errno.ECHILD)
- 如果 waitpid 被其它信号打断，就会抛出 OSError(errno.EINTR)，这个时候可以选择重试。

refer to 
- [juejin_rpc_py chapter 16](../juejin_rpc_py/chapter16/readme.md)
- [juejin_rpc_py chapter 17](../juejin_rpc_py/chapter17/readme.md)

## 捕获信号
子进程捕获父进程发送的信号 `signal.signal(signal.SIGTERM, signal.SIG_IGN)`

```python
def signal(sig, action): # real signature unknown; restored from __doc__
    """
    signal(sig, action) -> action
    
    Set the action for the given signal.  The action can be SIG_DFL,
    SIG_IGN, or a callable Python object.  The previous action is
    returned.  See getsignal() for possible return values.
    
    *** IMPORTANT NOTICE ***
    A signal handler function is called with two arguments:
    the first is the signal number, the second is the interrupted stack frame.
    """
    pass
```

SIG_IGN -- if the signal is being ignored 表示忽略信号
SIG_DFL -- if the default action for the signal is in effect


信号处理函数有两个参数，
- 第一个sig_num表示被捕获信号的整数值，
- 第二个frame不太好理解，一般也很少用。它表示被信号打断时，Python的运行的栈帧对象信息。
```python
def i_will_die(sig_num, frame):  # 自定义信号处理函数
    print "child will die"
    sys.exit(0)
```
以上例子中虽然两个参数都没有在函数中使用，但是还是需要声明。

refer to [catch signal](catch_signal.py)

## 计算圆周率的例子
需要安装 redis 依赖， 并启动 redis server 服务器
```
pip install redis

(.venv) Franks-Mac:multiple-process frank$ docker ps
CONTAINER ID   IMAGE       COMMAND                  CREATED       STATUS          PORTS                               NAMES
4046247e947c   redis       "docker-entrypoint.s…"   3 years ago   Up 34 minutes   0.0.0.0:6579->6379/tcp              redis3
f85301ab9ff1   redis       "docker-entrypoint.s…"   3 years ago   Up 34 minutes   0.0.0.0:6479->6379/tcp              redis2
a362c448e96a   mysql:5.7   "docker-entrypoint.s…"   4 years ago   Up 34 minutes   33060/tcp, 0.0.0.0:3305->3306/tcp   mysql5.7
b56b98880ad0   mariadb     "docker-entrypoint.s…"   4 years ago   Up 34 minutes   0.0.0.0:3307->3306/tcp              mariadb
06c6b54c3f86   redis       "docker-entrypoint.s…"   4 years ago   Up 34 minutes   0.0.0.0:6379->6379/tcp              redis

```
refer to [calculate pi](calculate_pi.py)

- 将级数之和的计算拆分成10个子进程计算，每个子进程负责1/10的计算量，
- 并将计算的中间结果扔到redis的队列中，
- 然后父进程等待所有子进程结束，再将队列中的数据全部汇总起来计算最终结果。

## Reference
- [Python多进程编程基础——图文版](https://juejin.cn/post/6844903613353951240)