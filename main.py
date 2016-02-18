# coding=utf8
import json
import urllib2
import smtplib
import email
import time
import sys
import os
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
		print u"\n\n正在查询 "+date_var+u" 的车票...\n"
		url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date='+date_var+'&leftTicketDTO.from_station='+stationCode[from_station]+'&leftTicketDTO.to_station='+stationCode[to_station]+'&purpose_codes=ADULT'

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
				info=ii['station_train_code']+" [ "+ii['start_time']+" "+ii['arrive_time']+" "+ii['lishi']+" ] "+u"有 "+ii[seatCode[seat_var]]+u" 个 "+seat_var
				#print info
				if ii[seatCode[seat_var]]==u'无':
					continue

				print info
				if email:
					sendmail(date_var+u" 从 "+from_station+u" 到 "+to_station+" "+info)
				while True:
					winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
		print u'查询无车票，等待下一次查询'

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

winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
while(True):
	try:
		trainTicket(u'石家庄',u'北京',['2016-02-13'],[u'二等座',u'硬座',u'硬卧'],email=False,fromTimeLimit=['12:00','23:59'],toTimeLimit=['00:00','22:00'])
		time.sleep(10)
	except KeyboardInterrupt:
		print 'EXIT'
		exit()
	except urllib2.HTTPError:
		pass