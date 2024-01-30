# coding=utf8

from __future__ import print_function
import json
import my_helper
import my_config
import time

if my_helper.PY3:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    import urllib.parse
else:
    from urllib2 import Request, urlopen, HTTPError, URLError

import chardet
import os
import sys

DATA_ADAPTER_NORMAL = 0
DATA_ADAPTER_MOBILE = 1


class TrainInfoRequest:
    def __init__(self):
        self.station_name_code_map = None
        self.init_station_code_name_map()
        self.http_request_headers = {
            'Host': 'kyfw.12306.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Sec-Fetch-User': '1',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'deflate, br',
        }

        self.http_request_cookies = {
            'JSESSIONID': '6287C53D5CAB8BFC03C55DF07D8DB944',
            'BIGipServerotn': '585629962.64545.0000',
            'RAIL_EXPIRATION': '1579667343088',
            'RAIL_DEVICEID': 'UOMY_J5PsrufMPeltK1azWB--gz0WyYO3qa3FPTrh4-vX5gt4jzm9v3K7E0cM5gtj8Ccqsn35nOS4Z7kLcFsYdc8LvZ2pGVDKcI2sLTasQB27QsYYeff8tKJa9gU4i6lojGaMH2jqjINBgvkMZ2x_b4-Cx2G0ZN7',
            'BIGipServerpassport': '1005060362.50215.0000',
            'route': '9036359bb8a8a461c164a04f8f50b252',
            '_jc_save_fromStation': '%u5317%u4EAC%2CBJP',
            '_jc_save_toStation': '%u4E0A%u6D77%2CSHH',
            '_jc_save_fromDate': '2020-01-18',
            '_jc_save_toDate': '2020-01-18',
            '_jc_save_wfdc_flag': 'dc',
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

    def init_station_code_name_map(self):
        fd = open('station_name_320130.js', 'r')
        line_str = fd.readline()
        ls = line_str.split('@')
        ls_len = len(ls)
        t_map = {}
        for i in range(1, ls_len):
            ls2 = ls[i].split('|')
            t_map[ls2[1]] = ls2[2]
        # print(t_map)
        self.station_name_code_map = t_map

    def find_station_code_2(self, station_name):
        code = self.station_name_code_map[station_name]
        if code is None:
            msg = u'车站名有误，请检查'
            my_helper.fatal_error(msg)
        return code

    def get_result(self, date_var, from_station, to_station, data_adapter=DATA_ADAPTER_NORMAL):
        station_code = {
            '北京': 'BJP',
            '福州': 'FZS',
            '三明北': 'SHS',
            '莆田': 'PTS',
            '邢台': 'XTP',
            '石家庄': 'SJP',
            '厦门': 'XMS',
            '上海': 'SHH',
            '聊城': 'UCK',
        }

        if not from_station in station_code:
            station_code[from_station] = self.find_station_code_2(from_station)
        if not to_station in station_code:
            station_code[to_station] = self.find_station_code_2(to_station)

        cookies = []
        for i in self.http_request_cookies:
            cookies.append(i + '=' + self.http_request_cookies[i])

        self.http_request_headers['Cookie'] = ';'.join(cookies)

        if data_adapter == DATA_ADAPTER_NORMAL:
            url = 'https://kyfw.12306.cn/otn/leftTicket/query' + my_config.random_letter + '?leftTicketDTO.train_date=' + \
                  date_var + '&leftTicketDTO.from_station=' + station_code[
                      from_station] + '&leftTicketDTO.to_station=' + \
                  station_code[to_station] + '&purpose_codes=ADULT'
        elif data_adapter == DATA_ADAPTER_MOBILE:
            url = 'http://mobile.12306.cn/weixin/leftTicket/query?leftTicketDTO.train_date=' + date_var + \
                  '&leftTicketDTO.from_station=' + station_code[from_station] + \
                  '&leftTicketDTO.to_station=' + station_code[to_station] + '&purpose_codes=ADULT'
            self.http_request_headers['Host'] = 'mobile.12306.cn'
        else:
            return

        print(url)
        request = Request(url, headers=self.http_request_headers)
        while True:
            try:
                response = urlopen(request)
                html = response.read()
                response_header = response.info()
                decode_json = json.loads(html)
                break
            except (HTTPError, URLError, ValueError) as e:
                my_helper.error_output(str(type(e)) + ' ' + str(e))
                time.sleep(my_config.internal_second / 2)
                pass

        if data_adapter == DATA_ADAPTER_NORMAL:
            all_train_info = decode_json['data']['result']
            result = []
            for train_info in all_train_info:
                result.append(TrainInfo(train_info))
            return result
        elif data_adapter == DATA_ADAPTER_MOBILE:
            all_train_info = decode_json['data']
            result = []
            for train_info in all_train_info:
                result.append(TrainInfoMobile(train_info))

            return result

    def query_by_train_no(self, train_no, from_station_telecode, to_station_telecode, depart_date):
        url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&' \
              'to_station_telecode=%s&depart_date=%s' % (train_no, from_station_telecode, to_station_telecode,
                                                         depart_date)
        request = Request(url, headers=self.http_request_headers)
        response = urlopen(request)
        html = response.read()
        response_header = response.info()
        decode_json = json.loads(html)
        station_list = []
        for item in decode_json['data']['data']:
            station_list.append(item['station_name'])

        return station_list


class TrainInfo:
    def __init__(self, data):
        self.data = data.split('|')
        # print(self.data)

    def show(self):
        print(self.data)

    def get_train_no(self):
        return self.data[2]

    def get_station_train_code(self):
        return self.data[3]

    def get_start_time(self):
        return self.data[8]

    def get_arrive_time(self):
        return self.data[9]

    def get_seat_number(self, seat_var):
        seat_code = {
            '高级软卧': 'gr_num',
            '其它': 'qt_num',
            '软卧': 23,
            '软座': 'rz_num',
            '商务座': 32,
            '特等座': 32,
            '无座': 26,
            '硬卧': 28,
            '硬座': 29,
            '二等座': 30,
            '一等座': 31,
        }
        return self.data[seat_code[seat_var]]

    def get_take_time(self):
        return self.data[10]

    def get_origin_area(self):
        return self.data[4]

    def get_terminal_area(self):
        return self.data[5]

    def get_from_station(self):
        return self.data[6]

    def get_to_station(self):
        return self.data[7]

    def get_departure_date(self):
        return self.data[13]

    def is_stop_run(self):
        return self.data[19]


class TrainInfoMobile:
    def __init__(self, data):
        self.data = data

    def show(self):
        print(self.data)

    def get_station_train_code(self):
        return self.data['station_train_code']

    def get_start_time(self):
        return self.data['start_time']

    def get_arrive_time(self):
        return self.data['arrive_time']

    def get_seat_number(self, seat_var):
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
        return self.data[seat_code[seat_var]]

    def get_take_time(self):
        return self.data['lishi']

    def get_origin_area(self):
        return self.data['start_station_name']

    def get_terminal_area(self):
        return self.data['end_station_name']

    def get_from_station(self):
        return self.data['from_station_name']

    def get_to_station(self):
        return self.data['to_station_name']

    def get_departure_date(self):
        return self.data['start_train_date']
