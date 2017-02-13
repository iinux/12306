# coding=utf8
import json
import urllib2
import smtplib
import email
import time
import sys
import os
import platform
import datetime


reload(sys)
sys.setdefaultencoding('utf-8')

if platform.system() == 'Windows':
    isWindows = True
else:
    isWindows = False

if isWindows:
    import winsound

local_time = time.localtime()
now_time = time.strftime('%Y-%m-%d %X', local_time)

##############################
# config
##############################
daemon_mode = False
internal_second = 60
debug = False
error_notification_trigger_number = 10
##############################


def dd(var):
    print var
    sys.exit(0)


def output(var):
    print now_time + ' ' + var

error_buffer = ''
error_count = 0


def error_output(var):
    global error_buffer, error_count
    error_buffer += '|' + var
    error_count += 1
    if error_count == error_notification_trigger_number:
        send_mail('error buffer:' + error_buffer)
        error_buffer = ''
        error_count = 0
    print now_time + ' ' + var


def train_ticket(from_station, to_station, date, seat, no_GD=False, email_notify=False, night_query=False,
                 not_like=[], like=[], start_time_limit=[], to_time_limit=[]):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    if not night_query and (local_time[3] >= 23 or local_time[3] < 5):
        output(u'23：00到次日6：00无法订票，所以23：00到5：00不作查询。若此期间有退票，会在5：00后提醒。')
        return

    station_code = {
        '北京': 'BJP',
        '福州': 'FZS',
        '三明北': 'SHS',
        '莆田': 'PTS',
        '邢台': 'XTP',
        '石家庄': 'SJP',
        '厦门': 'XMS',
    }
    seat_code = {
        # '硬座': 'gg_num',
        '高级软卧': 'gr_num',
        '其它': 'qt_num',
        '软卧': 'rw_num',
        '软座': 'rz_num',
        '商务座': 'swz_num',
        '特等座': 'tz_num',
        '无座': 'wz_num',
        # '硬座': 'yb_num',
        '硬卧': 'yw_num',
        '硬座': 'yz_num',
        '二等座': 'ze_num',
        '一等座': 'zy_num',
    }

    http_request_headers = {
        'Host': 'kyfw.12306.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 '
                      'Safari/537.36 2345Explorer/6.3.0.9753',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    for date_var in date:
        if current_date > date_var:
            output(u'旧日期，跳过')
            continue

        output(u'正在查询 ' + date_var + ' 的车票...')
        # old url
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=' + date_var + \
              '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'
        # 2016-05-23 update the url
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date_var + \
              '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'
        # 2016-12-24 update the url
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=' + date_var + \
              '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'
        # 2017-2-2 update the url
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + date_var + \
              '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'
        # 2017-2-13 update the url
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=' + date_var + \
              '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'

        request = urllib2.Request(url, headers=http_request_headers)
        response = urllib2.urlopen(request)
        html = response.read()
        response_header = response.info()
        decode_json = json.loads(html)
        all_train_info = decode_json['data']
        for train_info in all_train_info:
            train_data = train_info['queryLeftNewDTO']
            if train_data['station_train_code'] in not_like:
                continue
            if no_GD and train_data['station_train_code'].startswith('G'):
                continue
            if no_GD and train_data['station_train_code'].startswith('D'):
                continue
            if like != [] and not train_data['station_train_code'] in like:
                continue

            if start_time_limit:
                if start_time_limit[0] < start_time_limit[1]:
                    if train_data['start_time'] < start_time_limit[0] or train_data['start_time'] > start_time_limit[1]:
                        continue
                else:
                    if start_time_limit[1] < train_data['start_time'] < start_time_limit[0]:
                        continue

            if to_time_limit:
                if to_time_limit[0] < to_time_limit[1]:
                    if train_data['arrive_time'] < to_time_limit[0] or train_data['arrive_time'] > to_time_limit[1]:
                        continue
                else:
                    if to_time_limit[1] < train_data['arrive_time'] < to_time_limit[0]:
                        continue

            for seat_var in seat:
                if train_data[seat_code[seat_var]] == '--':
                    continue
                info = train_data['station_train_code'] + '有 ' + train_data[seat_code[seat_var]] + ' 个' + seat_var + '从' + train_data['start_time'] + '到' + train_data['arrive_time'] + '历时' + train_data['lishi']
                output(info)
                if train_data[seat_code[seat_var]] == '无':
                    continue
                if email_notify:
                    send_mail(info + ' ' + date_var + '从' + from_station + '到' + to_station)
                #while True:
                sound_system_exclamation()
    output(u'本次查询结束，等待下一次查询，' + str(internal_second) + '秒之后')


def send_mail(content):
    if debug:
        return
    my_email = smtplib.SMTP('smtp.139.com', 25)
    my_email.login('iinux@139.com', 'leuwai')

    msg = email.Message.Message()
    # msg = email.mime.text.MIMEText(content,_subtype='plain')
    msg['to'] = 'iinux@139.com'
    msg['from'] = 'iinux@139.com'
    msg['subject'] = content  # '有票通知'

    my_email.sendmail('iinux@139.com', ['iinux@139.com'], msg.as_string())
    my_email.quit()


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
            sys.exit(0)   # 父进程退出
    except OSError, e:
        error_output('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    # 从母体环境脱离
    # chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.chdir('/')
    os.umask(0)  # 调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()    # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

    # 执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)   # 第二个父进程退出
    except OSError, e:
        error_output('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    # 进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr:
        f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())    # dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if daemon_mode:
    to_daemon('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')


def sound_system_exclamation():
    if isWindows:
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
    else:
        output('SystemExclamation')
        time.sleep(1)
send_mail('开始查询')

while True:
    try:
        train_ticket('北京', '厦门', ['2017-01-20', '2017-02-21', '2017-02-22'], ['硬卧'], email_notify=True,
                     start_time_limit=['16:00', '16:05'], to_time_limit=['00:00', '23:59'])
    except KeyboardInterrupt:
        error_output('KeyboardInterrupt - EXIT')
        exit()
    except urllib2.HTTPError:
        error_output('urllib2.HTTPError')
        pass
    except urllib2.URLError:
        error_output('urllib2.URLError')
        pass
    except Exception, e:
        error_output(str(Exception) + ' ' + str(e))
        pass
    time.sleep(internal_second)
