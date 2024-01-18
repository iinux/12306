#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask
from flask import request, render_template
import MySQLdb
import config
import sys
import beijing_parse
import requests

sys.path.append('../')
import my_helper

if not my_helper.PY3:
    reload(sys)
    sys.setdefaultencoding('utf8')

app = flask.Flask(__name__, static_folder='bower_components')
beijing_parse_instance = beijing_parse.Parse()

url = 'http://www.8989iot.com/api/Card/loginCard'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/105.0.0.0 ' \
             'Safari/536.36 '


@app.route("/")
def index():
    db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
    db.set_character_set('utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    query_update_at = request.args.get('update_at')

    cursor.execute("select distinct(update_at) from bj_metro_real_data order by update_at desc limit 100")
    # 使用 fetchone() 方法获取一条数据库。
    all_update_at = cursor.fetchall()
    newest_time = all_update_at[0][0].strftime('%Y-%m-%d %H:%M')

    return_string = ""
    return_string += newest_time + "<br />"

    if query_update_at:
        cursor.execute("select * from bj_metro_real_data where update_at='%s'" % (query_update_at))
    else:
        cursor.execute("select * from bj_metro_real_data where update_at='%s'" % (newest_time))
    data = cursor.fetchall()

    _all_update_at = []
    for update_at in all_update_at:
        update_at = update_at[0].strftime('%Y-%m-%d %H:%M')
        _all_update_at.append(update_at)

    db.close()

    return render_template('index.html', all_update_at=_all_update_at, data=data,
                           map=beijing_parse_instance.acc_name_map_with_line)


@app.route("/byStation")
def by_station():
    db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
    db.set_character_set('utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    from_name = request.args.get('from_name')
    to_name = request.args.get('to_name')
    limit = request.args.get('limit', 100, type=int)

    cursor.execute("select * from bj_metro_real_data " +
                   "where from_name='%s' and to_name='%s' ORDER by update_at desc limit %d" %
                   (from_name, to_name, limit))
    data = cursor.fetchall()

    db.close()

    return render_template('byStation.html', data=data,
                           map=beijing_parse_instance.acc_name_map_with_line)


@app.route("/traffic_card_query")
def traffic_card_query():
    data_list = []
    for number in config.traffic_card_query_numbers:
        data_list.append(traffic_card_query_req(number))
    return render_template('traffic_card_query.html', data=data_list)


def traffic_card_query_req(number):
    res = requests.post(url, json={
        'number': number
    }, headers={
        'Content-Type': 'application/json',
        'User-Agent': user_agent,
    })

    res_data = res.json()['data']
    res_dict = {}
    res_dict['number'] = number
    res_dict['usage'] = 'usage: %s G / %s G' % (res_data['remainAmount'] / 1024, res_data['totalAmount'] / 1024)
    res_dict['package_name'] = 'packageName: ' + res_data['packageName']
    res_dict['expire_time'] = 'expiretime: ' + res_data['expiretime']
    res_dict['status'] = 'status: ' + res_data['status']
    return res_dict


@app.route("/real_bus_query")
def real_bus_query():
    start = request.args.get('start')
    end = request.args.get('end')
    data_list = []
    tag = 'start'
    previous_line = ''
    with open(config.real_bus_data_file, 'r') as file:
        for line in file:
            columns = line.strip().split(' ')
            last_column = columns[-1]
            if tag != last_column and previous_line != '':
                check_time(data_list, previous_line, start, end)

            tag = last_column
            previous_line = line
    return render_template('real_bus_query.html', data=data_list)


def check_time(data_list, line, start, end):
    line = line.strip()
    columns = line.split(' ')
    arrive_time_str = columns[-4]

    if start <= arrive_time_str <= end:
        data_list.append(columns[0][11:] + ' ' + columns[1][0:8])


if __name__ == "__main__":
    app.debug = config.flask_debug_switch
    app.run(host=config.flask_listen_host)
