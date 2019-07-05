# coding=utf8

from __future__ import print_function
import os
import platform
import time
import sys
import my_mail
import datetime

if sys.version > '3':
    PY3 = True
else:
    PY3 = False


def dd(var):
    print(var)
    sys.exit(0)


def output(var):
    print(now_time() + ' ' + var)


def now_time():
    local_time = time.localtime()
    return time.strftime('%Y-%m-%d %X', local_time)


error_buffer = ''
error_count = 0
error_notification_trigger_number = 1000


def error_output(var):
    global error_buffer, error_count
    error_buffer += '|' + var
    error_count += 1
    if error_count == error_notification_trigger_number:
        my_mail.send('error buffer', error_buffer)
        error_buffer = ''
        error_count = 0
    print(now_time() + ' ' + var)


def fatal_error(msg):
    error_output(msg)
    my_mail.send(msg)
    sys.exit(-1)


'''将当前进程fork为一个守护进程
   注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了
   所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有chdir()和umask()了
'''


def to_daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    if isWindows:
        return
    # 重定向标准文件描述符（默认情况下定向到/dev/null）
    try:
        pid = os.fork()
        # 父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)  # 父进程退出
    except (OSError) as e:
        error_output('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    # 从母体环境脱离
    # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.chdir('/')
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()  # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # 第二个父进程退出
    except (OSError) as e:
        error_output('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())  # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if platform.system() == 'Windows':
    isWindows = True
    import winsound
else:
    isWindows = False


def sound_system_exclamation():
    if isWindows:
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
    else:
        output('SystemExclamation')
        time.sleep(1)


def fix_update_at(origin):
    current_datetime = datetime.datetime.now()
    origin_datetime = datetime.datetime.strptime(origin, "%Y-%m-%d %X")
    if current_datetime - origin_datetime > datetime.timedelta(days=6):
        return origin_datetime.replace(current_datetime.year, current_datetime.month, current_datetime.day)
    else:
        return origin
