# Python inter process communication

## file

refer to [file](file.py)

## 管道pipe

管道是Unix进程间通信最常用的方法之一，它通过在父子进程之间开通读写通道来进行双工交流。
我们通过os.read()和os.write()来对文件描述符进行读写操作，使用os.close()关闭描述符。

```
os.pipe()
Create a pipe. Return a pair of file descriptors (r, w) usable for reading and writing, respectively.

Availability: Unix, Windows.


os.read(fd, n)
Read at most n bytes from file descriptor fd. Return a string containing the bytes read. If the end of the file referred to by fd has been reached, an empty string is returned.

Availability: Unix, Windows.


os.write(fd, str)
Write the string str to file descriptor fd. Return the number of bytes actually written.

Availability: Unix, Windows.

注解 该功能适用于低级 I/O 操作，必须用于 os.open() 或 pipe() 返回的文件描述符。若要写入由内建函数 open()、popen()、fdopen()、sys.stdout 或 sys.stderr 返回的 “文件对象”，则应使用其相应的 write() 方法。
```

## 以太网套接字

套接字无疑是通信使用最为广泛的方式了，它不但能跨进程还能跨网络。

今天英特网能发达成这样，全拜套接字所赐。不过作为同一个机器的多进程通信还是挺浪费的。暂不讨论这个，还是先看看它如何使用吧。

```python

# Wrapper around platform socket objects. This implements
# a platform-independent dup() functionality. The
# implementation currently relies on reference counting
# to close the underlying socket object.
class _socketobject(object):
    __doc__ = _realsocket.__doc__

    __slots__ = ["_sock", "__weakref__"] + list(_delegate_methods)

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, _sock=None):
        if _sock is None:
            _sock = _realsocket(family, type, proto)
        self._sock = _sock
        for method in _delegate_methods:
            setattr(self, method, getattr(_sock, method))

    def close(self, _closedsocket=_closedsocket,
              _delegate_methods=_delegate_methods, setattr=setattr):
        # This function should not reference any globals. See issue #808164.
        self._sock = _closedsocket()
        dummy = self._sock._dummy
        for method in _delegate_methods:
            setattr(self, method, dummy)

    close.__doc__ = _realsocket.close.__doc__

    def accept(self):
        sock, addr = self._sock.accept()
        return _socketobject(_sock=sock), addr

    accept.__doc__ = _realsocket.accept.__doc__

    def dup(self):
        """dup() -> socket object

        Return a new socket object connected to the same system resource."""
        return _socketobject(_sock=self._sock)

    def makefile(self, mode='r', bufsize=-1):
        """makefile([mode[, bufsize]]) -> file object

        Return a regular file object corresponding to the socket.  The mode
        and bufsize arguments are as for the built-in open() function."""
        return _fileobject(self._sock, mode, bufsize)

    family = property(lambda self: self._sock.family, doc="the socket family")
    type = property(lambda self: self._sock.type, doc="the socket type")
    proto = property(lambda self: self._sock.proto, doc="the socket protocol")

```

```
socket.AF_UNIX
socket.AF_INET
socket.AF_INET6
These constants represent the address (and protocol) families, used for the first argument to socket(). 
If the AF_UNIX constant is not defined then this protocol is unsupported.

socket.SOCK_STREAM
socket.SOCK_DGRAM
socket.SOCK_RAW
socket.SOCK_RDM
socket.SOCK_SEQPACKET
These constants represent the socket types, used for the second argument to socket(). 
(Only SOCK_STREAM and SOCK_DGRAM appear to be generally useful.)


socket.socket([family[, type[, proto]]])
Create a new socket using the given address family, socket type and protocol number. 
The address family should be AF_INET (the default), AF_INET6 or AF_UNIX. 
The socket type should be SOCK_STREAM (the default), SOCK_DGRAM or perhaps one of the other SOCK_ constants. 
The protocol number is usually zero and may be omitted in that case.


socket.accept()
接受一个连接。此 scoket 必须绑定到一个地址上并且监听连接。
返回值是一个 (conn, address) 对，其中 conn 是一个 新 的套接字对象，用于在此连接上收发数据，address 是连接另一端的套接字所绑定的地址。


socket.bind(address)
将套接字绑定到 address。套接字必须尚未绑定。


socket.connect(address)
连接到 address 处的远程套接字。


socket.listen(backlog)
Listen for connections made to the socket. 
The backlog argument specifies the maximum number of queued connections and should be at least 0; 
the maximum value is system-dependent (usually 5), the minimum value is forced to 0.


socket.recv(bufsize[, flags])
Receive data from the socket. The return value is a string representing the data received. 
The maximum amount of data to be received at once is specified by bufsize. 
See the Unix manual page recv(2) for the meaning of the optional argument flags; it defaults to zero.


socket.send(string[, flags])
Send data to the socket. The socket must be connected to a remote socket. 
The optional flags argument has the same meaning as for recv() above. 
Returns the number of bytes sent. 
Applications are responsible for checking that all data has been sent; 
if only some of the data was transmitted, the application needs to attempt delivery of the remaining data.


socket.sendall(string[, flags])
Send data to the socket. The socket must be connected to a remote socket. 
The optional flags argument has the same meaning as for recv() above. 
Unlike send(), this method continues to send data from string until either all data has been sent or an error occurs. 
None is returned on success. 
On error, an exception is raised, and there is no way to determine how much data, if any, was successfully sent.


```

## Unix域套接字
当同一个机器的多个进程使用普通套接字进行通信时，需要经过网络协议栈，这非常浪费，因为同一个机器根本没有必要走网络。
所以Unix提供了一个套接字的特殊版本，它使用和套接字一摸一样的api，但是地址不再是网络端口，而是文件。
相当于我们通过某个特殊文件来进行套接字通信。

- socket.AF_UNIX
- server_address = "/tmp/pi_sock"  # 套接字对应的文件名

类似的章节：refer to [../juejin_rpc_py/chapter14](../juejin_rpc_py/chapter14/readme.md)

## 无名套接字socketpair
我们知道跨网络通信免不了要通过套接字进行通信，但是本例的多进程是在同一个机器上，用不着跨网络，使用普通套接字进行通信有点浪费。

为了解决这个问题，Unix系统提供了无名套接字socketpair，不需要端口也可以创建套接字，父子进程通过socketpair来进行全双工通信。

socketpair返回两个套接字对象，一个用于读一个用于写，它有点类似于pipe，只不过pipe返回的是两个文件描述符，都是整数。所以写起代码形式上跟pipe几乎没有什么区别


类似的章节：refer to [../juejin_rpc_py/chapter14](../juejin_rpc_py/chapter14/readme.md)

```
socket.socketpair([family[, type[, proto]]])
Build a pair of connected socket objects using the given address family, socket type, and protocol number. 
Address family, socket type, and protocol number are as for the socket() function above. 
The default family is AF_UNIX if defined on the platform; otherwise, the default is AF_INET. 
Availability: Unix.
```
默认就是 AF_UNIX

```python
def socketpair(family=None, type=None, proto=None): # real signature unknown; restored from __doc__
    """
    socketpair([family[, type[, proto]]]) -> (socket object, socket object)
    
    Create a pair of socket objects from the sockets returned by the platform
    socketpair() function.
    The arguments are the same as for socket() except the default family is
    AF_UNIX if defined on the platform; otherwise, the default is AF_INET.
    """
    pass

```

## 有名管道fifo
相对于管道只能用于父子进程之间通信，Unix还提供了有名管道可以让任意进程进行通信。
有名管道又称fifo，它会将自己注册到文件系统里一个文件，参数通信的进程通过读写这个文件进行通信。
fifo要求读写双方必须同时打开才可以继续进行读写操作，否则打开操作会堵塞直到对方也打开。

```python
def mkfifo(filename, mode=0666): # real signature unknown; restored from __doc__
    """
    mkfifo(filename [, mode=0666])
    
    Create a FIFO (a POSIX named pipe).
    """
    pass

def unlink(path): # real signature unknown; restored from __doc__
    """
    unlink(path)
    
    Remove a file (same as remove(path)).
    """
    pass
```

```
os.mkfifo(path[, mode])
Create a FIFO (a named pipe) named path with numeric mode mode. 
The default mode is 0666 (octal). The current umask value is first masked out from the mode.

Availability: Unix.

FIFO 是可以像常规文件一样访问的管道。FIFO 如果没有被删除（如使用 os.unlink()），会一直存在。
通常，FIFO 用作“客户端”和“服务器”进程之间的汇合点：服务器打开 FIFO 进行读取，而客户端打开 FIFO 进行写入。
请注意，mkfifo() 不会打开 FIFO — 它只是创建汇合点。


os.unlink(path)
Remove (delete) the file path. This is the same function as remove(); 
the unlink() name is its traditional Unix name.

Availability: Unix, Windows.


os.remove(path)
Remove (delete) the file path. If path is a directory, OSError is raised; see rmdir() below to remove a directory. This is identical to the unlink() function documented below. On Windows, attempting to remove a file that is in use causes an exception to be raised; on Unix, the directory entry is removed but the storage allocated to the file is not made available until the original file is no longer in use.

Availability: Unix, Windows.
```

## OS Message Queue
操作系统也提供了跨进程的消息队列对象可以让我们直接使用，只不过python没有默认提供包装好的api来直接使用。
我们必须使用第三方扩展来完成OS消息队列通信。

- 一种是posix消息队列，Linux
- 另一种是systemv消息队列，macOS

### MacOS
根据[文档](https://semanchuk.com/philip/sysv_ipc/history.html)，最新版本（1.1.0）不支持 Python 2 版本。

Current – 1.1.0 (17 Jan 2021) – Drop support for Python 2, 
also for Python 3.4 and 3.5.
```commandline
pip install sysv_ipc==1.0.1
```

systemv的消息队列是以整数key作为名称，如果不指定，它就创建一个唯一的未占用的整数key。
它还提供消息类型的整数参数，但是不支持消息优先级。

```python
class MessageQueue(object):
    """ System V message queue object """
    def receive(self, *args, **kwargs): # real signature unknown
        """ Receive a message from the queue """
        pass

    def remove(self, *args, **kwargs): # real signature unknown
        """ Removes (deletes) the queue from the system """
        pass

    def send(self, *args, **kwargs): # real signature unknown
        """ Place a message on the queue """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    cgid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The GID of the queue's creator. Read only."""

    cuid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The UID of the queue's creator. Read only."""

    current_messages = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The number of messages currently in the queue"""

    gid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The queue's GID."""

    id = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Message queue id"""

    key = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The key passed to the constructor."""

    last_change_time = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A Unix timestamp representing the last time the queue was changed."""

    last_receive_pid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The id of the last process which received from the queue"""

    last_receive_time = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A Unix timestamp representing the last time a message was received."""

    last_send_pid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The id of the last process which sent via the queue"""

    last_send_time = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """A Unix timestamp representing the last time a message was sent."""

    max_size = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The maximum size of the queue (in bytes). Read-write if you have sufficient privileges."""

    mode = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Permissions"""

    uid = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The queue's UID."""

```

### Linux
posix消息队列
- posix消息队列需要提供一个唯一的名称，它必须是/开头。
- close()方法仅仅是减少内核消息队列对象的引用，而不是彻底关闭它。unlink()方法才能彻底销毁它。
- O_CREAT选项表示如果不存在就创建。
- 向队列里塞消息使用send方法，
- 收取消息使用receive方法，receive方法返回一个tuple，
  - tuple的第一个值是消息的内容，
  - 第二个值是消息的优先级。之所以有优先级，是因为posix消息队列支持消息的排序，
- 在send 方法的第二个参数可以提供优先级整数值，默认为0，越大优先级越高。

```commandline
pip install posix_ipc==1.0.5
# 不支持导入MessageQueue  from posix_ipc import MessageQueue
```
最新版本 1.1.1 不支持 Python 2。
[release history](https://pypi.org/project/posix-ipc/#history)

## 共享内存
共享内存也是非常常见的多进程通信方式，操作系统负责将同一份物理地址的内存映射到多个进程的不同的虚拟地址空间中。
进而每个进程都可以操作这份内存。
考虑到物理内存的唯一性，它属于临界区资源，需要在进程访问时搞好并发控制，比如使用信号量。
我们通过一个信号量来控制所有子进程的顺序读写共享内存。
- 我们分配一个8字节double类型的共享内存用来存储极限的和，
- 每次从共享内存中读出来时，要使用struct进行反序列化(unpack)，
- 将新的值写进去之前也要使用struct进行序列化(pack)。
- 每次读写操作都需要将读写指针移动到内存开头位置(lseek)。

Semaphore 臂板信号，旗语。使用一个信号量控制多个进程互斥访问共享内存
```python
class Semaphore(object):
    """ POSIX semaphore object """
    def acquire(self, *args, **kwargs): # real signature unknown
        """ Acquire (grab) the semaphore, waiting if necessary """
        pass

    def close(self, *args, **kwargs): # real signature unknown
        """ Close the semaphore for this process. """
        pass

    def release(self, *args, **kwargs): # real signature unknown
        """ Release the semaphore """
        pass

    def unlink(self, *args, **kwargs): # real signature unknown
        """ Unlink (remove) the semaphore. """
        pass

    def __enter__(self, *args, **kwargs): # real signature unknown
        pass

    def __exit__(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    mode = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The mode specified in the constructor"""

    name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name specified in the constructor"""

```

SharedMemory
```python
class SharedMemory(object):
    """ POSIX shared memory object """
    def close_fd(self, *args, **kwargs): # real signature unknown
        """ Closes the file descriptor associated with the shared memory. """
        pass

    def unlink(self, *args, **kwargs): # real signature unknown
        """ Unlink (remove) the shared memory. """
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(S, *more): # real signature unknown; restored from __doc__
        """ T.__new__(S, ...) -> a new object with type S, a subtype of T """
        pass

    def __repr__(self): # real signature unknown; restored from __doc__
        """ x.__repr__() <==> repr(x) """
        pass

    def __str__(self): # real signature unknown; restored from __doc__
        """ x.__str__() <==> str(x) """
        pass

    fd = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Shared memory segment file descriptor"""

    mode = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The mode specified in the constructor"""

    name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name specified in the constructor"""

    size = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """size"""

```

```python
def lseek(fd, pos, how): # real signature unknown; restored from __doc__
    """
    lseek(fd, pos, how) -> newpos
    
    Set the current position of a file descriptor.
    Return the new cursor position in bytes, starting from the beginning.
    """
    pass

def write(fd, string): # real signature unknown; restored from __doc__
    """
    write(fd, string) -> byteswritten
    
    Write a string to a file descriptor.
    """
    pass

def read(fd, buffersize): # real signature unknown; restored from __doc__
    """
    read(fd, buffersize) -> string
    
    Read a file descriptor.
    """
    return ""
```

## Reference

- [深入Python进程间通信原理--图文版](https://juejin.cn/post/6844903613425270797)
- [Python os doc](https://docs.python.org/zh-cn/2.7/library/os.html?highlight=os#module-os)
- [Python socket doc](https://docs.python.org/zh-cn/2.7/library/socket.html?highlight=socket#module-socket)
- [Python socket howto](https://docs.python.org/zh-cn/2.7/howto/sockets.html#socket-howto)



