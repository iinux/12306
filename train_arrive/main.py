#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import time
import urllib
import urllib2
import MySQLdb
import data_parse

http_request_headers = {
    'Host': 'wx.tlbl.winsion.net',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 MicroMessenger/6.5.7 Language/zh_CN',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}

parse_instance = data_parse.Parse()
while True:
    current_datetime = datetime.datetime.now()
    file_name = current_datetime.strftime('%Y-%m-%d-%H-%M')
    print(file_name)

    url = 'http://wx.tlbl.winsion.net/wxservice/getTrainInformationByTrainNumber'
    values = {}
    values['trainNumber'] = ""
    values['type'] = "arrive"
    data = urllib.urlencode(values)  # 使用了urllib库中的urlencode方法
    request = urllib2.Request(url, data, headers=http_request_headers)
    try:
        response = urllib2.urlopen(request)
        response_body = response.read()
        response_header = response.info()
        write_file = open("getTrainInformationByTrainNumber" + file_name, 'wb')
        write_file.write(response_body)
        write_file.close()

        parse_instance.parse_content(response_body)
    except urllib2.HTTPError:
        print('urllib2.HTTPError')
    except urllib2.URLError:
        print('urllib2.URLError')
    except MySQLdb.Error, e:
        print(e)
        parse_instance.reconnect()
    except Exception, e:
        print(e)

    time.sleep(60*30)
