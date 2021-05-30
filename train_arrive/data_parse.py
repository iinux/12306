#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from sys import argv
import MySQLdb
import config
import datetime
import time


class Parse:
    db = None
    cursor = None

    def __init__(self):
        self.connect()

    def connect(self):
        # 打开数据库连接
        self.db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
        self.db.set_character_set('utf8')

        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def reconnect(self):
        self.close()
        self.connect()

    def parse_content(self, content, date=None):
        print("start parse data")
        now = datetime.datetime.now()
        if date is None:
            date = now.strftime('%Y-%m-%d')
        current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
        decode_json = json.loads(content)
        for train in decode_json['data']:
            exit_entrances = ''
            for entrance in train['exitEntrances']:
                exit_entrances += entrance['name']
            station_platforms = ''
            for platform in train['stationPlatforms']:
                station_platforms += platform['name']
            arrive_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(train['arriveTime'] / 1000))

            # 使用execute方法执行SQL语句
            self.cursor.execute("SELECT * from arrive_data where date=%s and train_number=%s",
                                (date, train['trainNumber']))

            # 使用 fetchone() 方法获取一条数据库。
            data = self.cursor.fetchone()
            print(train['departStationName'])
            try:
                if data is None:
                    print("run insert")
                    # 执行sql语句
                    self.cursor.execute(
                        """INSERT INTO arrive_data(date,train_number,delay,depart_station_name,arrive_time,exit_entrances,station_platforms,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (date, train['trainNumber'], train['delay'], train['departStationName'], arrive_time,
                         exit_entrances,
                         station_platforms, current_datetime, current_datetime))
                elif data[3] != train['delay'] or data[7] != station_platforms:
                    print("run update")
                    self.cursor.execute(
                        """update arrive_data set delay=%s,depart_station_name=%s,arrive_time=%s,exit_entrances=%s,station_platforms=%s,updated_at=%s where id=%s""",
                        (train['delay'], train['departStationName'], arrive_time, exit_entrances, station_platforms,
                         current_datetime, data[0]))
                # 提交到数据库执行
                self.db.commit()
            except Exception as e:
                # 发生错误时回滚
                self.db.rollback()

    def close(self):
        # 关闭数据库连接
        self.db.close()

    def parse_file(self, filename):
        file_description = open(filename)
        content = file_description.read()
        print ("processing %s" % filename)
        date = filename[32:42]
        self.parse_content(content, date)
        print ("processed %s" % filename)


if __name__ == "__main__":
    argv_len = argv.__len__()
    i = 1
    parse_instance = Parse()

    while i < argv_len:
        filename = argv[i]
        i += 1
        parse_instance.parse_file(filename)

    parse_instance.close()
