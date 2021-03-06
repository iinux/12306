# coding=utf8

from __future__ import print_function
import json
import time
import sys
import datetime
import my_mail
import my_helper
import my_config
import train
import argparse

if my_helper.PY3:
    import urllib.request, urllib.error, urllib.parse
else:
    import urllib2
    reload(sys)
    sys.setdefaultencoding('utf-8')

# sys.path.append('a.py所在的路径')

parser = argparse.ArgumentParser("python main.py")
parser.add_argument("-m", help="use wechat mobile site data", action="store_true", default=False)
args = parser.parse_args()


##############################
# ticket info
##############################


def want_ticket():
    train_ticket('北京', '厦门', ['2018-02-10', '2018-02-11', '2018-02-12'], ['硬卧'], email_notify=True,
                 start_time_limit=['16:00', '16:05'], to_time_limit=['00:00', '23:59'])
##############################


def train_ticket(from_station, to_station, date, seat, no_GD=False, email_notify=False, night_query=False,
                 not_like=[], like=[], start_time_limit=[], to_time_limit=[], atLeast=1, lessNotify=0):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    local_time = time.localtime()
    if not night_query and (local_time[3] >= 23 or local_time[3] < 5 or (local_time[3] == 5 and local_time[4] < 30)):
        my_helper.output(u'23：00到次日6：00无法订票，所以23：00到5：30不作查询。若此期间有退票，会在5：30后提醒。')
        time.sleep(my_config.internal_second)
        return

    for date_var in date:
        if current_date > date_var:
            my_helper.output(u'旧日期，跳过')
            continue

        my_helper.output(u'正在查询 ' + from_station + ' 到 ' + to_station + ' ' + date_var + ' 的车票...')
        train_info_request = train.TrainInfoRequest()
        if args.m:
            all_train_info = train_info_request.get_result(date_var, from_station, to_station, train.DATA_ADAPTER_MOBILE)
        else:
            all_train_info = train_info_request.get_result(date_var, from_station, to_station)
        for train_info in all_train_info:
            station_train_code = train_info.get_station_train_code()
            if station_train_code in not_like:
                continue
            if no_GD and station_train_code.startswith('G'):
                continue
            if no_GD and station_train_code.startswith('D'):
                continue
            if like != [] and not station_train_code in like:
                continue

            start_time = train_info.get_start_time()
            arrive_time = train_info.get_arrive_time()
            if start_time_limit:
                if start_time_limit[0] < start_time_limit[1]:
                    if start_time < start_time_limit[0] or start_time > start_time_limit[1]:
                        continue
                else:
                    if start_time_limit[1] < start_time < start_time_limit[0]:
                        continue

            if to_time_limit:
                if to_time_limit[0] < to_time_limit[1]:
                    if arrive_time < to_time_limit[0] or arrive_time > to_time_limit[1]:
                        continue
                else:
                    if to_time_limit[1] < arrive_time < to_time_limit[0]:
                        continue

            for seat_var in seat:
                seat_number = train_info.get_seat_number(seat_var)
                if seat_number == '--' or seat_number == '':
                    continue
                take_time = train_info.get_take_time()
                info = station_train_code + '有 ' + seat_number + ' 个' + seat_var + '从' + start_time + '到' + arrive_time + '历时' + take_time
                my_helper.output(info)
                if seat_number == '无':
                    continue
                if lessNotify > 0 and (seat_number == '有' or int(seat_number) > lessNotify):
                    continue
                if atLeast > 1 and seat_number != '有' and int(seat_number) < atLeast:
                    continue
                if email_notify:
                    my_mail.send(info + ' ' + date_var + '从' + from_station + '到' + to_station)
                # while True:
                my_helper.sound_system_exclamation()
        time.sleep(my_config.internal_second)
    my_helper.output(u'本次查询结束，等待下一次查询，' + str(my_config.internal_second) + '秒之后')


if my_config.daemon_mode:
    my_helper.to_daemon('/dev/null', '/tmp/daemon_stdout.log', '/tmp/daemon_error.log')


my_mail.send('开始查询')

while True:
    try:
        want_ticket()
    except KeyboardInterrupt:
        my_helper.error_output('KeyboardInterrupt - EXIT')
        exit()
    except (Exception) as e:
        my_helper.error_output(str(type(e)) + ' ' + str(e))
        time.sleep(my_config.internal_second)
        pass
