import datetime
import time
from urllib.request import urlopen
import real_data_parse
import MySQLdb
import ssl

'''
http://bjmetro.cc/subwaymap2/public/
http://bjmetro.cc/subwaymap2/public/api/getblocks
http://bjmetro.cc/subwaymap2/public/subwaymap/stations.xml
xxx http://bjmetro.cc/subwaymap2/public/subwaymap/beijing.xml
https://bjsubway.com/
https://bjsubway.com/subwaymap/beijing.xml?v=2
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
        # url = 'http://119.254.65.180:8080/subwaymap2/public/api/getrealdatas'
        # url = 'https://map.bjsubway.com/api/getrealdatas'
        url = 'https://map.bjsubway.com/getrealdatas'
        try:
            response = urlopen(url)
            response_body = response.read()
            response_header = response.info()
            write_file = open("getrealdatas/" + file_name, 'wb')
            write_file.write(response_body)
            write_file.close()

            real_data_parse_instance.parse_content(response_body)
        except MySQLdb.Error as e:
            print(e)
            real_data_parse_instance.reconnect()
        except KeyError as e:
            print(e)

        except Exception as e:
            print(e)

    time.sleep(180)
