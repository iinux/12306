# coding=utf8
import json
import urllib2
import smtplib
import email
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import platform

if platform.system() == "Windows":
	isWindows = True
else:
	isWindows = False

##############################
# config
##############################
daemonMode = False
internalSecond = 10
##############################

if isWindows:
	import winsound

def trainTicket(from_station,to_station,date=[],seat=[],no_GD=False,email=False,nightQuery=False,not_like=[],like=[],fromTimeLimit=[],toTimeLimit=[]):
	ltime=time.localtime()
	if nightQuery and (ltime[3]>=23 or ltime[3]<6):
		print u'23：00到次日7：00无法订票，所以23：00到6：00不作查询。若此期间有退票，会在6：00后提醒。'
		return
	now_time=time.strftime('%Y-%m-%d %X', ltime)

	stationCode={}
	seatCode={}

	stationCode[u'北京']='BJP'
	stationCode[u'福州']='FZS'
	stationCode[u'三明北']='SHS'
	stationCode[u'莆田']='PTS'
	stationCode[u'邢台']='XTP'
	stationCode[u'石家庄']='SJP'

	#seatCode[u'硬座']='gg_num'
	seatCode[u'高级软卧']='gr_num'
	seatCode[u'其它']='qt_num'
	seatCode[u'软卧']='rw_num'
	seatCode[u'软座']='rz_num'
	seatCode[u'商务座']='swz_num'
	seatCode[u'特等座']='tz_num'
	seatCode[u'无座']='wz_num'
	#seatCode[u'硬座']='yb_num'
	seatCode[u'硬卧']='yw_num'
	seatCode[u'硬座']='yz_num'
	seatCode[u'二等座']='ze_num'
	seatCode[u'一等座']='zy_num'

	send_headers = {
		'Host':'kyfw.12306.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36 2345Explorer/6.3.0.9753',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Connection':'keep-alive',
		'Accept-Language':'zh-CN,zh;q=0.8'
	}
	
	for date_var in date:
		print u"\n\n [ " + now_time + " ] 正在查询 " + date_var + u" 的车票...\n"
		# old url
		url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date='+date_var+'&leftTicketDTO.from_station='+stationCode[from_station]+'&leftTicketDTO.to_station='+stationCode[to_station]+'&purpose_codes=ADULT'
		# 2016-05-23 update the url
		url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date_var+'&leftTicketDTO.from_station='+stationCode[from_station]+'&leftTicketDTO.to_station='+stationCode[to_station]+'&purpose_codes=ADULT'

		req = urllib2.Request(url,headers=send_headers)
		r  = urllib2.urlopen(req)
		html = r.read()
		receive_header = r.info()
		decodejson=json.loads(html)

		alltraininfo=decodejson['data']
		for i in alltraininfo:
			ii=i['queryLeftNewDTO']
			if ii['station_train_code'] in not_like:
				continue
			if no_GD and ii['station_train_code'].startswith('G'):
				continue
			if no_GD and ii['station_train_code'].startswith('D'):
				continue
			if like!=[] and not ii['station_train_code'] in like:
				continue

			if fromTimeLimit!=[]:
				if fromTimeLimit[0]<fromTimeLimit[1]:
					if not (fromTimeLimit[0]<ii['start_time'] and ii['start_time']<fromTimeLimit[1]):
						continue
				else:
					if not (fromTimeLimit[0]<ii['start_time'] or ii['start_time']<fromTimeLimit[1]):
						continue

			if toTimeLimit!=[]:
				if toTimeLimit[0]<toTimeLimit[1]:
					if not (toTimeLimit[0]<ii['arrive_time'] and ii['arrive_time']<toTimeLimit[1]):
						continue
				else:
					if not (toTimeLimit[0]<ii['arrive_time'] or ii['arrive_time']<toTimeLimit[1]):
						continue

			for seat_var in seat:
				if ii[seatCode[seat_var]]=='--':
					continue
				info = ii['station_train_code'] + " [ " + ii['start_time'] + " " + ii['arrive_time'] + " " + ii['lishi'] + " ] " \
					+ u"有 " + ii[seatCode[seat_var]] + u" 个 " + seat_var
				print info
				if ii[seatCode[seat_var]]==u'无':
					continue

				print info
				if email:
					sendmail(info+" "+date_var+u" 从 "+from_station+u" 到 "+to_station)
				if isWindows:
					while True:
						winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
		print u'本次查询结束，等待下一次查询，' + str(internalSecond) + '秒之后'

def sendmail(content):
	myemail=smtplib.SMTP('smtp.139.com',25)
	myemail.login('iinux@139.com','leuwai')

	msg=email.Message.Message()
	#msg = email.mime.text.MIMEText(content,_subtype='plain')
	msg['to']='iinux@139.com'
	msg['from']='iinux@139.com'
	msg['subject']=content #'有票通知'

	myemail.sendmail('iinux@139.com',['iinux@139.com'],msg.as_string())
	myemail.quit()


'''将当前进程fork为一个守护进程
   注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了
   所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有chdir()和umask()了
'''

def daemonize (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
     #重定向标准文件描述符（默认情况下定向到/dev/null）
    try: 
        pid = os.fork() 
          #父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。
        if pid > 0:
            sys.exit(0)   #父进程退出
    except OSError, e: 
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #从母体环境脱离
    os.chdir("/")  #chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录
    os.umask(0)    #调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。
    os.setsid()    #setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。

     #执行第二次fork
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0)   #第二个父进程退出
    except OSError, e: 
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )
        sys.exit(1)

     #进程已经是守护进程了，重定向标准文件描述符

    for f in sys.stdout, sys.stderr: f.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())    #dup2函数原子化关闭和复制文件描述符
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if daemonMode:
	daemonize('/dev/null','/tmp/daemon_stdout.log','/tmp/daemon_error.log')


if isWindows:
	winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
sendmail(u"开始查询")

while(True):
	try:
		ltime = time.localtime()
		now_time = time.strftime('%Y-%m-%d %X', ltime)

		trainTicket(u'北京', u'邢台', ['2016-06-09'], [u'硬座'], email = True, fromTimeLimit = ['08:00', '11:59'], toTimeLimit = ['00:00', '18:00'])
		time.sleep(internalSecond)
	except KeyboardInterrupt:
		sys.stderr.write ( now_time + 'KeyboardInterrupt - EXIT\n\n' )
		exit()
	except urllib2.HTTPError:
		sys.stderr.write ( now_time + ' urllib2.HTTPError' )
		pass
	except urllib2.URLError:
		sys.stderr.write ( now_time + ' urllib2.URLError' )
		pass
	except Exception, e:
		sys.stderr.write ( now_time + " " + str(Exception) + " " + str(e) )
		pass