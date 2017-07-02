# coding=utf8
import json
import urllib2
import my_config
import my_helper


class TrainInfoRequest:
    def __init__(self):
        self.http_request_headers = {
            'Host': 'kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 '
                          'Safari/537.36 2345Explorer/6.3.0.9753',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def find_station_code(self, station_name):
        station_name += '|'
        fd = open('station_name.js', 'r')
        line_str = fd.readline()
        index = line_str.find(station_name)
        if index == -1:
            msg = u'车站名有误，请检查'
            my_helper.fatal_error(msg)
        p = code_start = index + station_name.__len__()
        station_code = ''
        while line_str[p] != '|':
            station_code += line_str[p]
            p += 1
        return station_code

    def get_result(self, date_var, from_station, to_station):
        station_code = {
            '北京': 'BJP',
            '福州': 'FZS',
            '三明北': 'SHS',
            '莆田': 'PTS',
            '邢台': 'XTP',
            '石家庄': 'SJP',
            '厦门': 'XMS',
        }

        if not station_code.has_key(from_station):
            station_code[from_station] = self.find_station_code(from_station)
        if not station_code.has_key(to_station):
            station_code[to_station] = self.find_station_code(to_station)
        url = 'https://kyfw.12306.cn/otn/leftTicket/query' + my_config.random_letter + '?leftTicketDTO.train_date=' + \
              date_var + '&leftTicketDTO.from_station=' + station_code[from_station] + '&leftTicketDTO.to_station=' + \
              station_code[to_station] + '&purpose_codes=ADULT'

        request = urllib2.Request(url, headers=self.http_request_headers)
        response = urllib2.urlopen(request)
        html = response.read()
        response_header = response.info()
        decode_json = json.loads(html)
        all_train_info = decode_json['data']['result']
        result = []
        for train_info in all_train_info:
            result.append(TrainInfo(train_info))
        return result


class TrainInfo:
    def __init__(self, data):
        self.data = str.split('|', data)

    def show(self):
        print self.data
