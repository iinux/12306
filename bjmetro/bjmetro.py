import datetime
import time
import urllib2
import real_data_parse
import MySQLdb

'''
http://bjmetro.cc/subwaymap2/public/
http://bjmetro.cc/subwaymap2/public/api/getblocks
http://bjmetro.cc/subwaymap2/public/subwaymap/stations.xml
http://bjmetro.cc/subwaymap2/public/subwaymap/beijing.xml
http://bjmetro.cc/subwaymap2/public/subwaymap/interchange.xml
'''

http_request_headers = {
    'Host': 'map.bjsubway.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 '
                  'Safari/537.36 2345Explorer/6.3.0.9753',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

real_data_parse_instance = real_data_parse.Parse()

while True:
    current_datetime = datetime.datetime.now()
    file_name = current_datetime.strftime('%Y-%m-%d-%H-%M')
    print(file_name)
    current_time = current_datetime.strftime('%H-%M')
    print(current_time)

    if current_time <= '00-34' or current_time >= '04-35':
        url = 'http://119.254.65.180:8080/subwaymap2/public/api/getrealdatas'
        request = urllib2.Request(url, headers=http_request_headers)
        try:
            response = urllib2.urlopen(request)
            response_body = response.read()
            response_header = response.info()
            write_file = open("getrealdatas" + file_name, 'wb')
            write_file.write(response_body)
            write_file.close()

            real_data_parse_instance.parse_content(response_body)
        except urllib2.HTTPError:
            print('urllib2.HTTPError')
        except urllib2.URLError:
            print('urllib2.URLError')
        except MySQLdb.Error, e:
            print(e)
            real_data_parse_instance.reconnect()
        except Exception, e:
            print(e)

    time.sleep(180)
