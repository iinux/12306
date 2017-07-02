# coding=utf8
import json
import urllib2
import time
import sys
import datetime
import my_mail
import my_helper
import my_config
import train
# sys.path.append('a.py所在的路径')


reload(sys)
sys.setdefaultencoding('utf-8')


##############################
# ticket info
##############################


def want_ticket():
    train_ticket('北京', '厦门', ['2017-07-20', '2017-07-21', '2017-02-22'], ['硬卧'], email_notify=True,
                 start_time_limit=['16:00', '16:05'], to_time_limit=['00:00', '23:59'])
##############################


def train_ticket(from_station, to_station, date, seat, no_GD=False, email_notify=False, night_query=False,
                 not_like=[], like=[], start_time_limit=[], to_time_limit=[]):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    local_time = time.localtime()
    if not night_query and (local_time[3] >= 23 or local_time[3] < 5):
        my_helper.output(u'23：00到次日6：00无法订票，所以23：00到5：00不作查询。若此期间有退票，会在5：00后提醒。')
        return


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

    for date_var in date:
        if current_date > date_var:
            my_helper.output(u'旧日期，跳过')
            continue

        my_helper.output(u'正在查询 ' + date_var + ' 的车票...')
        train_info_request = train.TrainInfoRequest()
        all_train_info = train_info_request.get_result(date_var, from_station, to_station)
        for train_info in all_train_info:
            train_info.show()
            continue
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
                my_helper.output(info)
                if train_data[seat_code[seat_var]] == '无':
                    continue
                if email_notify:
                    my_mail.send(info + ' ' + date_var + '从' + from_station + '到' + to_station)
                #while True:
                my_helper.sound_system_exclamation()
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
    except urllib2.HTTPError:
        my_helper.error_output('urllib2.HTTPError')
        pass
    except urllib2.URLError:
        my_helper.error_output('urllib2.URLError')
        pass
    except Exception, e:
        my_helper.error_output(str(Exception) + ' ' + str(e))
        pass
    time.sleep(my_config.internal_second)
