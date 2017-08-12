import datetime
import time
import urllib2

'''
http://bjmetro.cc/subwaymap2/public/
http://bjmetro.cc/subwaymap2/public/api/getblocks
http://bjmetro.cc/subwaymap2/public/subwaymap/stations.xml
http://bjmetro.cc/subwaymap2/public/subwaymap/beijing.xml
http://bjmetro.cc/subwaymap2/public/subwaymap/interchange.xml
'''

http_request_headers = {
    'Host': 'bjmetro.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 '
                  'Safari/537.36 2345Explorer/6.3.0.9753',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

while True:
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.strftime('%H-%M')
    print(current_time)

    if current_time <= '00-34' or current_time >= '04-35':
        url = 'http://bjmetro.cc/subwaymap2/public/api/getrealdatas'
        request = urllib2.Request(url, headers=http_request_headers)
        response = urllib2.urlopen(request)
        response_body = response.read()
        response_header = response.info()
        write_file = open("getrealdatas" + current_time, 'wb')
        write_file.write(response_body)
        write_file.close()

    time.sleep(60)
