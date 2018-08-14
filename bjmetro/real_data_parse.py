#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from sys import argv
from sys import path
import MySQLdb
import beijing_parse
import config

path.append('../')
import my_helper

class Parse:
    db = None
    cursor = None

    def __init__(self):
        self.beijing_parse_instance = beijing_parse.Parse()
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

    def parse_content(self, content):
        print ("start parse real data")
        decode_json = json.loads(content)
        for seg in decode_json['r']:
            from_name = self.beijing_parse_instance.acc_name_map[seg['fs']]
            to_name = self.beijing_parse_instance.acc_name_map[seg['ts']]
            seg['update_at'] = my_helper.fix_update_at(seg['update_at'])
            print from_name, to_name, seg['color'], seg['update_at']
            # 使用execute方法执行SQL语句
            self.cursor.execute("SELECT * from bj_metro_real_data where fs=%s and ts=%s and update_at=%s",
                                (seg['fs'], seg['ts'], seg['update_at']))

            # 使用 fetchone() 方法获取一条数据库。
            data = self.cursor.fetchone()
            if data is None:
                try:
                    # 执行sql语句
                    self.cursor.execute(
                        """INSERT INTO bj_metro_real_data(id,fs,ts,color,update_at,from_name,to_name) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        (seg['id'], seg['fs'], seg['ts'], seg['color'], seg['update_at'], from_name, to_name))
                    # 提交到数据库执行
                    self.db.commit()
                except Exception, e:
                    print(e)
                    # 发生错误时回滚
                    self.db.rollback()

    def close(self):
        # 关闭数据库连接
        self.db.close()

    def parse_file(self, filename):
        file_description = open(filename)
        content = file_description.read()
        print ("processing %s" % filename)
        self.parse_content(content)
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
